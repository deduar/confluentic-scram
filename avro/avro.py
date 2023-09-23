import enum
import typing
import dataclasses

from dataclasses_avroschema import AvroModel


class FavoriteColor(enum.Enum):
    BLUE = "Blue"
    YELLOW = "Yellow"
    GREEN = "Green"


@dataclasses.dataclass
class User(AvroModel):
    "An User"
    name: str
    age: int
    pets: typing.List[str]
    accounts: typing.Dict[str, int]
    favorite_color: FavoriteColor
    country: str = "Argentina"
    address: str = None

    class Meta:
        namespace = "User.v1"
        aliases = ["user-v1", "super user"]


print(User.avro_schema())

# '{
#     "type": "record",
#     "name": "User",
#     "doc": "An User",
#     "namespace": "User.v1",
#     "aliases": ["user-v1", "super user"],
#     "fields": [
#         {"name": "name", "type": "string"},
#         {"name": "age", "type": "long"},
#         {"name": "pets", "type": "array", "items": "string"},
#         {"name": "accounts", "type": "map", "values": "long"},
#         {"name": "favorite_color", "type": {"type": "enum", "name": "FavoriteColor", "symbols": ["Blue", "Yellow", "Green"]}}
#         {"name": "country", "type": "string", "default": "Argentina"},
#         {"name": "address", "type": ["null", "string"], "default": null}
#     ]
# }'

print("---------")
print(User.avro_schema_to_python())

{
    "type": "record",
    "name": "User",
    "doc": "An User",
    "namespace": "User.v1",
    "aliases": ["user-v1", "super user"],
    "fields": [
        {"name": "name", "type": "string"},
        {"name": "age", "type": "long"},
        {"name": "pets", "type": {"type": "array", "items": "string", "name": "pet"}},
        {"name": "accounts", "type": {"type": "map", "values": "long", "name": "account"}},
        {"name": "favorite_color", "type": {"type": "enum", "name": "FavoriteColor", "symbols": ["BLUE", "YELLOW", "GREEN"]}},
        {"name": "country", "type": "string", "default": "Argentina"},
        {"name": "address", "type": ["null", "string"], "default": None}
    ],
}