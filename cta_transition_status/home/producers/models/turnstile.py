"""Creates a turnstile data producer"""
import logging
from pathlib import Path

from confluent_kafka import avro

from models.producer import Producer
from models.turnstile_hardware import TurnstileHardware


logger = logging.getLogger(__name__)


class Turnstile(Producer):
    key_schema = avro.load(f"{Path(__file__).parents[0]}/schemas/turnstile_key.json")

    #
    # TODO: Define this value schema in `schemas/turnstile_value.json, then uncomment the below
    #
    value_schema = avro.load(
        f"{Path(__file__).parents[0]}/schemas/turnstile_value.json"
    )

    def __init__(self, station):
        """Create the Turnstile"""
        station_name = (
            station.name.lower()
            .replace("/", "_and_")
            .replace(" ", "_")
            .replace("-", "_")
            .replace("'", "")
        )

        #
        #
        # TODO: Complete the below by deciding on a topic name, number of partitions, and number of
        # replicas
        #
        #
        super().__init__(
            f"com.cta.station.turnstile", # TODO: Come up with a better topic name
            key_schema=Turnstile.key_schema,
            value_schema=Turnstile.value_schema,
            num_partitions=2,
            num_replicas=1,
        )
        self.station = station
        self.turnstile_hardware = TurnstileHardware(station)
        self.station_name = station_name

    def run(self, timestamp, time_step):
        """Simulates riders entering through the turnstile."""
        num_entries = self.turnstile_hardware.get_entries(timestamp, time_step)
        #logger.info("turnstile kafka integration incomplete - skipping")
        #
        #
        # TODO: Complete this function by emitting a message to the turnstile topic for the number
        # of entries that were calculated
        #
        #
        print(Turnstile.value_schema)
        print(f"num_entries: {num_entries}")
        for _ in range(num_entries):
            print(f"""         station_id: {self.station.station_id},
                               station_name: {self.station_name},
                               line:{self.station.color.name}""")
            try:
                self.producer.produce(
                        topic=self.topic_name,
                        key={"timestamp": self.time_millis()},
                        value={
                              "station_id": self.station.station_id,
                               "station_name": self.station_name,
                               "line":self.station.color.name,
                              },
                        value_schema=Turnstile.value_schema,
                        key_schema=Turnstile.key_schema
                    )
                print("============================Successfull Turnstile message emit===================")
                print("***************************************************************************************")
            except:
                    logger.info("failed to produce message for arrivals")
                    raise
