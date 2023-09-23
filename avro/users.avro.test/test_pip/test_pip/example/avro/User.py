# -*- coding: utf-8 -*-

""" avro python class for file: User """

import json
from test_pip.helpers import default_json_serialize, todict
from typing import Union


class User(object):

    schema = """
    {
        "namespace": "example.avro",
        "type": "record",
        "name": "User",
        "fields": [
            {
                "name": "name",
                "type": "string"
            },
            {
                "name": "favorite_number",
                "type": [
                    "int",
                    "null"
                ]
            },
            {
                "name": "favorite_color",
                "type": [
                    "string",
                    "null"
                ]
            }
        ]
    }
    """

    def __init__(self, obj: Union[str, dict, 'User']) -> None:
        if isinstance(obj, str):
            obj = json.loads(obj)

        elif isinstance(obj, type(self)):
            obj = obj.__dict__

        elif not isinstance(obj, dict):
            raise TypeError(
                f"{type(obj)} is not in ('str', 'dict', 'User')"
            )

        self.set_name(obj.get('name', None))

        self.set_favorite_number(obj.get('favorite_number', None))

        self.set_favorite_color(obj.get('favorite_color', None))

    def dict(self):
        return todict(self)

    def set_name(self, value: str) -> None:

        if isinstance(value, str):
            self.name = value
        else:
            raise TypeError("field 'name' should be type str")

    def get_name(self) -> str:

        return self.name

    def set_favorite_number(self, value: Union[int, None]) -> None:
        if isinstance(value, int):
            self.favorite_number = int(value)

        elif isinstance(value, type(None)):
            self.favorite_number = None
        else:
            raise TypeError("field 'favorite_number' should be in (int, None)")

    def get_favorite_number(self) -> Union[int, None]:
        return self.favorite_number

    def set_favorite_color(self, value: Union[str, None]) -> None:
        if isinstance(value, str):
            self.favorite_color = str(value)

        elif isinstance(value, type(None)):
            self.favorite_color = None
        else:
            raise TypeError("field 'favorite_color' should be in (str, None)")

    def get_favorite_color(self) -> Union[str, None]:
        return self.favorite_color

    def serialize(self) -> None:
        return json.dumps(self, default=default_json_serialize)
