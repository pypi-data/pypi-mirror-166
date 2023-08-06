__author__ = 'foyou'
__version__ = '0.0.3'

import json
import sys
from dataclasses import dataclass, is_dataclass
from typing import Union, Dict

from case_convert import snake_case, pascal_case
from typing_extensions import ClassVar, get_type_hints, get_args, get_origin


@dataclass
class DatClass:
    _DEBUG: bool = True
    _HINTS: ClassVar[dict] = {}

    def __init__(self, *args, **kwargs):
        pass

    @staticmethod
    def _format_attr_name(key):
        return snake_case(key)

    @classmethod
    def _get_hints(cls) -> dict:
        hints = cls._HINTS.get(cls)
        if hints:
            return hints
        hints = get_type_hints(cls)
        cls._HINTS[cls] = hints
        return hints

    @staticmethod
    def _null_list(cls, may_null):
        if may_null:
            if isinstance(may_null[0], dict):
                return [cls.fill_dataclass(item) for item in may_null]
            else:
                return may_null
        else:
            return []

    @staticmethod
    def _null_dict(cls, may_null):
        if may_null is None:
            return None
        if isinstance(may_null, dict):
            return cls.fill_dataclass(may_null)
        return may_null

    @classmethod
    def fill_dataclass(cls, obj):
        hints = cls._get_hints()
        params = {}
        for key, value in obj.items():
            if key in hints:
                params[DatClass._format_attr_name(key)] = value
            elif DatClass._DEBUG:
                print(f'MISSING_ATTRS. {cls.__module__}.{cls.__name__}'
                      f'({key} : {type(value).__name__} = {repr(value)[:100]})')
        return cls(**params)

    def __post_init__(self):
        """自动 post_init"""
        hints = self._get_hints()
        for attr_name, type_class in hints.items():
            origin = get_origin(type_class)
            if origin is None:
                if is_dataclass(type_class):
                    setattr(self, attr_name, DatClass._null_dict(type_class, getattr(self, attr_name)))
                    continue
            for hint_type in get_args(type_class):
                if is_dataclass(hint_type):
                    if origin is list:
                        setattr(self, attr_name, DatClass._null_list(hint_type, getattr(self, attr_name)))
                    break


class GenDatClass:

    @staticmethod
    def get_sub_class(key_name):
        return key_name[0].upper() + key_name[1:]

    def __init__(self, data: Union[str, Dict], cls_name: str):
        if isinstance(data, str):
            data = json.loads(data)
        self._data = data

        self._result = []
        self._result.append('@dataclass')
        self._result.append(f'class {cls_name}(DatClass):')

        self._gen_class()

    def _gen_class(self):
        for k, v in self._data.items():
            if v is None:
                v_type = 'str'
            else:
                v_type = type(v).__name__

            if v_type == 'dict':
                v_type = 'Dict'

            if v_type == 'list':
                v_type = 'List'

            self._result.append(f'    {DatClass._format_attr_name(k)}: {v_type} = None')

    def print(self):
        for i in self._result:
            print(i)


def main():
    print('请粘贴 JSON 字符串：CTRL + C 结束')
    print('-' * 100)
    data = []
    try:
        while True:
            data.append(input())
    except KeyboardInterrupt:
        print('-' * 100)
        gc = GenDatClass('\n'.join(data), 'Object' if len(sys.argv) == 1 else pascal_case(sys.argv[1]))
        gc.print()
        print('-' * 100)


if __name__ == '__main__':
    main()
