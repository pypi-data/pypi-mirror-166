import argparse
import asyncio
import aiohttp
from datetime import datetime, date
from math import floor
from .request import *
from .formatting import *


def get_current_day_timestamp() -> int:
    """
    Gets current day (starting from 00:00:00) timestamp
    """
    current_day = date.today()
    return floor(datetime(
        year=current_day.year,
        month=current_day.month,
        day=current_day.day
    ).timestamp())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "gancio_instance",
        type=str,
        help="The gancio instance url from which fetch data"
    )
    args = parser.parse_args()
    instance_url = args.gancio_instance

    # fetch the events
    try:
        events_data = asyncio.run(
            # NOTE: this will print also the events ending in 00:00:00
            get_events(instance_url, {"start": get_current_day_timestamp()})
        )
        # print outcome
        if events_data["status"] == 200:  # successfully request
            events = events_data["json_content"]
            if events == []:
                print("There aren't any scheduled events.")
            else:
                print()
                for event_dict in events:
                    print(format_event_info(event_dict, instance_url))
                    print()
        else:
            print("Si è verificato un errore.")
    except aiohttp.ClientError:  # Base class for all client specific exceptions.
        print(f"It hasn't been possible to connect to {instance_url}")
        print("Maybe there is a typo in the url, or maybe the site is down (You can check on https://www.isitdownrightnow.com)")


if __name__ == "__main__":
    main()
