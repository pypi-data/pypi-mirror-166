"""Model (dataclass) writer
"""
import re
import uuid
import csv
import os
import logging
from dataclasses import asdict
from typing import Dict, Iterable, Sequence, TextIO, Type

logger = logging.getLogger(__name__)


def get_fieldnames(dclass: Type) -> Sequence[str]:
    """Get fieldnames for a specified dataclass type"""
    if not hasattr(dclass, "__dataclass_fields__"):
        raise ValueError(f"{dclass.__name__} is not a dataclass")
    blacklist = getattr(dclass, "__blacklist__", [])
    return [
        field for field in dclass.__dataclass_fields__.keys() if not field.startswith("__") and field not in blacklist
    ]


# pylint: disable=too-few-public-methods
class ModelWriter:
    """A model (dataclass) writer

    This class allows you to create a proxy to multiple csv files at once. By calling
    writerow(<dataclass-instance>) ModelWriter will automatically find out
    what output file to choose and will serialize the dataclass instance into
    a valid csv line.
    """

    def __init__(self, output_path: str, models: Sequence[Type]):
        if not all((hasattr(dclass, "__filename__") for dclass in models)):
            raise TypeError("Only models with __filename__ are supported")
        self.models = models
        self.output_path = output_path
        self.handles: Dict[Type, TextIO] = {}
        self.writers: Dict[Type, csv.DictWriter] = {}

    def __enter__(self):
        """Enter context manager"""
        logger.info("Initiating dataclass writer")
        for dclass in self.models:
            path = os.path.join(self.output_path, dclass.__filename__)
            self.handles[dclass] = open(path, "w", encoding="utf-8", newline="")
            self.writers[dclass] = csv.DictWriter(
                self.handles[dclass], fieldnames=get_fieldnames(dclass), dialect=csv.unix_dialect
            )
            self.writers[dclass].writeheader()
            logger.info("Preparing %s for writing dataclass '%s'", path, getattr(dclass, "__name__", str(dclass)))
        return self

    def __exit__(self, *args):
        """Exit context manager"""
        for handle in self.handles.values():
            handle.close()
        logger.info("All files closed")

    def writerow(self, model):
        """Write line using writer associated with dclass"""
        if not self.writers:
            raise TypeError("Context manager was not entered")
        self.writers[model.__class__].writerow(asdict(model))

    def writerows(self, models: Iterable):
        """Writer rows using writer associated with dclass"""
        if not self.writers:
            raise TypeError("Context manager was not entered")
        for item in models:
            self.writerow(item)


def write_nested_dict_generator_to_csvs(
        generator: Iterable[dict],
        first_file_name: str,
        output_folder: str,
        primary_keys: Iterable[str] = (),
        default_primary_key_name: str = "__uuid",
        foreign_key_prefix: str = "__parent",
        recursion_limit: int = 10,
        case: str = "keep",
        extras_action: str = "raise",
        missing_action: str = "raise"
):
    """
    Recursively write nested dictionaries and lists to csv files.

    Parameters:
    -----------
    generator: Iterable[dict]
        An iterable of dictionaries to write to csv files.
    first_file_name: str
        The name of the first csv file to write to.
    output_folder: str
        The folder to write the csv files to.
    primary_keys: Iterable[str] = ()
        The keys to use as primary keys. If not specified, default_primary_key_name may be used if necessary.
         For example in dictionary: {"id": 1, "property: {"id": 1, "property": {"id": 1}}}
         To mark the first id as primary key primary_keys=["id"]
         To mark the second id as primary key primary_keys=["property_id"]
         To mark the third id as primary key primary_keys=["property_property_id"]
         To mark all as primary_keys=["id", "property_id", "property_property_id"]
         If multiple keys specified the nearest parent primary key will be used.
    default_primary_key_name: str = "__uid"
        The name of the primary key to use if no primary_keys is specified. Also used if some part of dictionary
        has no primary key and needs some.
    foreign_key_prefix: str = "__parent"
        The prefix to use for foreign keys/ parent keys.
    recursion_limit: int = 10
        The maximum number of levels to recurse into nested dictionaries and lists.
    case: accepts values "keep", "lower" and "snake".
        "keep" for keep case
        "snake" for snake_case
        "lower" for lower case
    extras_action: str = "raise"
        Accept values "raise" and "ignore".
        Action to take if fist dictionary is missing keys that are in later dictionaries. Raise will raise errors.
    missing_action: str = "raise"
        Accept values "raise" and "ignore".
        Action to take if fist dictionary has more keys than later dictionaries. Raise will raise errors.
    """
    with nested_dict_generator_writer(
            output_folder=output_folder,
            primary_keys=primary_keys,
            default_primary_key_name=default_primary_key_name,
            foreign_key_prefix=foreign_key_prefix,
            recursion_limit=recursion_limit,
            case=case,
            extras_action=extras_action,
            missing_action=missing_action
    ) as writer:
        writer.writerows(generator=generator, first_file_name=first_file_name)


class nested_dict_generator_writer:
    def __init__(
            self,
            output_folder: str,
            primary_keys: Iterable,
            default_primary_key_name: str,
            foreign_key_prefix: str,
            recursion_limit: int,
            case: str,
            extras_action: str,
            missing_action: str
    ):
        self._output_folder = output_folder
        self._primary_keys = set(primary_keys)
        self._default_primary_key_name = default_primary_key_name
        self._foreign_key_prefix = foreign_key_prefix
        self._recursion_limit = recursion_limit
        self._writers = {}
        self._case = case
        self._change_string_case = None
        self._set_change_string_case(case)
        self.extras_action = extras_action
        self.missing_action = missing_action

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        for writer in self._writers.values():
            writer.close()

    def writerows(self, generator: Iterable, first_file_name: str):
        for row in generator:
            self._walk_object(row, file_name_base=first_file_name, base_level=True)

    def _walk_object(
            self,
            object_,
            file_name_base: str,
            column_prefix: str = "",
            primary_key_identification_prefix: str = "",
            primitive_type_column_name: str = "",
            base_column_name: str = "",
            foreign_key_dict: dict = None,
            recursion_level: int = 0,
            base_level: bool = False,
            parent_type: str = None,
    ):
        """
        Recursively walk an object and write it to csv files.

        This function will recursively walk an object and write it to csv files.

        param object_: The object to walk.
        param file_name_base: The name of the first file to write to. Recursively used as potential new file name.
        param column_prefix: Prefixes columns. Recursively used in nested dictionaries.
        param primary_key_identification_prefix: Recursively used for primary key identification.
        param primitive_type_column_name: String of nested keys used to name columns of primitive type values.
        param base_column_name: Used for sending column name from dictionary to list. Is the same dict key.
        param foreign_key_dict: Used for sending foreign key derived from existing primary key to lists
        param recursion_level: Used for controlling recursion depth
        param base_level: Set true at base/root level. In recursion is False
        param parent_type: Used to identify lists in lists
        """

        if recursion_level >= self._recursion_limit:
            raise ValueError(f"Recursion limit reached at {recursion_level}")
        to_return = {}
        object_type = type(object_)
        if object_type == dict:
            dict_ = self._change_dictionary_keys_case(object_)
            if self._primary_keys:
                foreign_key_dict = (
                        self._get_foreign_key_dict_from_existing_primary_key(
                            dict_, primary_key_identification_prefix, column_prefix
                        )
                        or foreign_key_dict
                )
            for key, value in dict_.items():
                returned_from_recursion = self._walk_object(
                    object_=value,
                    file_name_base="_".join([file_name_base, key]),
                    primitive_type_column_name="".join([column_prefix, key]),
                    base_column_name=key,
                    column_prefix="".join([column_prefix, key, "_"]),
                    foreign_key_dict=foreign_key_dict,
                    recursion_level=recursion_level + 1,
                    parent_type=object_type,
                    primary_key_identification_prefix="".join([primary_key_identification_prefix, key, "_"]),
                )
                to_return |= returned_from_recursion
                foreign_key_dict = (
                        self._get_foreign_key_dict_from_generated_primary_key(returned_from_recursion)
                        or foreign_key_dict
                )
            if base_level:
                self._get_writer(file_name_base).writerow(to_return)
            else:
                return to_return
        elif object_type == list:
            if parent_type == list:
                raise TypeError(
                    """List of lists is not supported. 
Table is list of list, when the fist list contains column names.
But I do not know if this interpretation is generally correct.
"""
                )
            if not foreign_key_dict:
                primary_key_dict, foreign_key_dict = self._get_new_keys()
                to_return = primary_key_dict
            writer = self._get_writer(file_name_base)
            for item in object_:
                to_write = foreign_key_dict | self._walk_object(
                    object_=item,
                    file_name_base=file_name_base,
                    primitive_type_column_name=base_column_name,
                    base_column_name=base_column_name,
                    column_prefix="",
                    foreign_key_dict=foreign_key_dict,
                    recursion_level=recursion_level + 1,
                    parent_type=object_type,
                    primary_key_identification_prefix=primary_key_identification_prefix,
                )
                writer.writerow(to_write)
            return to_return
        else:
            return {primitive_type_column_name: object_}

    def _change_dictionary_keys_case(self, dictionary: dict):
        return {self._change_string_case(key): value for key, value in dictionary.items()}

    def _set_change_string_case(self, case: str):
        case_transformations = {"keep": self._keep_case,
                                "snake": self._make_snake_case,
                                "lower": self._make_lower_case}
        self._change_string_case = case_transformations.get(case)
        if not self._change_string_case:
            raise ValueError(f"Unknown string case transformation: {case}")

    def _get_foreign_key_dict_from_existing_primary_key(
            self, dict_: dict, primary_key_identification_prefix: str, column_prefix: str
    ) -> dict:
        prefixed_column_names = ("".join([primary_key_identification_prefix, key]) for key in dict_.keys())
        intersection_keys = self._primary_keys.intersection(prefixed_column_names)
        if len(intersection_keys) == 0:
            return {}
        elif len(intersection_keys) == 1:
            primary_key_identificator = intersection_keys.pop()
            original_key = primary_key_identificator[len(primary_key_identification_prefix):]
            return {"".join([self._foreign_key_prefix, column_prefix, original_key]): dict_[original_key]}
        else:
            raise ValueError(
                f"""More than one primary key found in intersection of primary keys and dict keys.
                 intersection_keys={intersection_keys},
                 dict_.keys()={dict_.keys()},
                 self.primary_keys={self._primary_keys}"""
            )

    def _get_foreign_key_dict_from_generated_primary_key(self, returned_from_recursion: dict):
        primary_key_value = returned_from_recursion.get(self._default_primary_key_name)
        if primary_key_value:
            return {"".join([self._foreign_key_prefix, self._default_primary_key_name]): primary_key_value}
        else:
            return None

    def _get_new_keys(self):
        foreign_key_name = "".join([self._foreign_key_prefix, self._default_primary_key_name])
        value = uuid.uuid4()
        # self.primary_keys.add(primary_key_identification_prefix, self.default_primary_key_name)  #
        # the above is not doing anything now, but it may be semantically correct
        return {self._default_primary_key_name: value}, {foreign_key_name: value}

    def _get_writer(self, base_file_name: str):
        try:
            return self._writers[base_file_name]
        except KeyError:
            self._writers[base_file_name] = lazy_dict_writer(self._output_folder, base_file_name, self.extras_action,
                                                             self.missing_action)
            return self._writers[base_file_name]

    @staticmethod
    def _make_lower_case(string: str):
        return string.lower()

    @staticmethod
    def _make_snake_case(string: str):
        return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()

    @staticmethod
    def _keep_case(string: str):
        return string


class lazy_dict_writer:
    def __init__(self, output_folder: str,
                 file_basename: str,
                 extras_action: str = "raise",
                 missing_action: str = "raise"):
        self.filepath = os.path.join(output_folder, f"{file_basename}.csv")
        self.file = None
        self.inner_writer = None
        self.columns = None
        self.extras_action = extras_action
        self.missing_action_function = self.get_missing_action_function(missing_action)

    def get_missing_action_function(self, missing_action):
        if missing_action == "raise":
            return self._check_keys
        else:
            return self._do_nothing

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def writerow(self, row: dict):
        try:
            self.inner_writer.writerow(row)
        except AttributeError:
            logger.info(f"Opening file {self.filepath}")
            self.file = open(self.filepath, "w")
            self.inner_writer = csv.DictWriter(self.file,
                                               dialect=csv.unix_dialect,
                                               fieldnames=row.keys(),
                                               extrasaction=self.extras_action)
            self.inner_writer.writeheader()
            self.inner_writer.writerow(row)
            self.columns = set(row.keys())
        self.missing_action_function(row)

    def _check_keys(self, row: dict):
        missing = self.columns - row.keys()
        if missing:
            raise ValueError(f"Last dictionary written to {self.filepath} was missing keys {missing}")

    def close(self):
        if self.file:
            self.file.close()
            logger.info(f"Closed file {self.filepath}")

    @staticmethod
    def _do_nothing(_):
        pass
