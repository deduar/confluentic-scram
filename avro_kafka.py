import enum
import random
from dataclasses import dataclass

from dotenv import load_dotenv

from service.kafka_consumer import KAFKA_CONSUMER
from service.kafka_producer import KAFKA_PRODUCER

from dataclasses_avroschema import AvroModel


class FavoriteColor(enum.Enum):
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    GREEN = "GREEN"

@dataclass
class UserModel(AvroModel):
    "An User"
    name: str
    age: int
    favorite_colors: FavoriteColor = FavoriteColor.BLUE
    country: str = "Argentina"
    address: str = None

    class Meta:
        namespace = "User.v1"
        aliases = ["user-v1", "super user"]


def consume():
    load_dotenv()
    consumer = KAFKA_CONSUMER().consumer()

    for msg in consumer:
        print(f"Message received: {msg.value}")
        # user = UserModel.deserialize(msg.value)
        # print(f"Message deserialized: {user}")

    print("Stoping consumer...")


def send(total_events=3):
    producer = KAFKA_PRODUCER().producer()

    for event_number in range(1, total_events + 1):
        # Produce message
        print(f"Sending event number {event_number}")

        # create an instance of User v1
        user = UserModel(
            name=random.choice(
                [
                    "Juan",
                    "Peter",
                    "Michael",
                    "Moby",
                    "Kim",
                ]
            ),
            age=random.randint(1, 50),
        )
        # create the message
        # message = user.serialize()
        producer.send("t_raw", str(user))

    print("Stoping producer...")


if __name__ == "__main__":
    load_dotenv()
    send()
    consume()