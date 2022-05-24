import asyncio
import datetime
import json
import os
import random
from time import sleep

from azure.eventhub import EventData
from azure.eventhub.aio import EventHubProducerClient
from dotenv import load_dotenv

load_dotenv()


def create_message(message_id=1):
    return {
        "timestamp": datetime.datetime.now().timestamp(),
        "color": random.choice(
            [
                "red",
                "green",
                "blue",
                "black",
                "yellow",
                "orange",
            ]
        ),
        "height": random.randint(90, 110),
        "width": random.randint(250, 320),
        "depth": random.randint(18, 25),
        "machine_id": random.randint(1, 3),
        "status": random.choices(
            (
                "SUCCESS",
                "ERROR",
            ),
            (
                0.9,
                0.1,
            ),
        ),
        "message_id": message_id,
    }


async def send_event_data(producer):
    # Without specifying partition_id or partition_key
    # the events will be distributed to available partitions via round-robin.
    event_data_batch = await producer.create_batch()

    for i in range(random.randint(1, 5)):
        event_data_batch.add(EventData(json.dumps(create_message(i))))

    await producer.send_batch(event_data_batch)


async def run():

    producer = EventHubProducerClient.from_connection_string(
        conn_str=os.getenv("CONN_STR"),
        eventhub_name=os.getenv("EVENT_HUB"),
    )

    async with producer:
        for _ in range(os.getenv("NUM_MESSAGES")):
            await send_event_data(producer)
            sleep(random.random() * os.getenv("SLEEP_INTERVAL"))


loop = asyncio.get_event_loop()

loop.run_until_complete(run())
