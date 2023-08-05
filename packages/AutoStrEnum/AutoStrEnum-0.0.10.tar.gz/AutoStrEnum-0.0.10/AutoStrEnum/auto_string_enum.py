import json
from enum import EnumMeta, Enum
from typing import Any


class _MetaData:

    def __init__(self, parent: str, data: str):
        self.parent = str(parent)
        self.data = str(data)

    def __str__(self):
        return self.data

    def __repr__(self):
        return self.data

    def __eq__(self, other):
        if not isinstance(other, _MetaData):
            return False
        if self.parent != other.parent:
            return False
        if self.data != other.data:
            return False
        return True

    def __hash__(self):
        return hash(f'{self.parent}{self.data}')


class _MagicMeta(EnumMeta):

    def __contains__(self, other):
        if not isinstance(other, str):
            return False
        return other in self.__dict__['_member_names_']

    def __instancecheck__(self, instance):
        if not isinstance(instance, str):
            return False
        return instance in self.__dict__['_member_names_']

    def __str__(self):
        return str(self.__name__)

    def __repr__(self):
        return str(self.__name__)


generated: dict = {}


class AutoStrEnum(Enum, metaclass=_MagicMeta):
    def __get__(self, instance, owner):
        global generated

        tuple_key = (str(owner), self.name)
        if tuple_key in generated:
            return generated[tuple_key].data

        generated[tuple_key] = _MetaData(parent=str(owner), data=self.name)

        return generated[tuple_key].data


def is_auto_string_enum_type(obj: Any) -> bool:
    return isinstance(obj, (_MagicMeta, _MetaData, AutoStrEnum))


def convert_obj_to_json(obj: Any) -> Any:
    if isinstance(obj, (tuple, list)):
        return [convert_obj_to_json(o) for o in obj]

    if isinstance(obj, dict):
        for key, value in obj.copy().items():
            if not is_auto_string_enum_type(key):
                continue
            if is_auto_string_enum_type(value):
                value = str(value)
            obj[str(key)] = convert_obj_to_json(value)
            obj.pop(key)

    return obj


class AutoJsonEncoder(json.JSONEncoder):

    def default(self, obj):
        if is_auto_string_enum_type(obj):
            return str(obj)
        return super().default(obj)

    def encode(self, obj) -> str:
        # logging.debug(f'into AutoJsonEncoder', {inspect.stack()[0][3]})
        convert_obj_to_json(obj)
        return super().encode(obj)
