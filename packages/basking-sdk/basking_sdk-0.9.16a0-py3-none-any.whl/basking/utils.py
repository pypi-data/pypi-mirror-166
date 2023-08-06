import logging
from datetime import datetime

import pytz


class Utils:
    def __init__(self, basking_obj):
        self.basking = basking_obj
        self.log = logging.getLogger(self.__class__.__name__)
        basking_log_level = logging.getLogger(self.basking.__class__.__name__).level
        self.log.setLevel(basking_log_level)

    def convert_timestamp_to_building_timezone(self, building_id: str, timestamp: datetime) -> datetime:
        """
        :return: UTC representation of the timestamp in the building's timezone
        TODO: Switch from pytz to dateutil
        """
        timestamp = timestamp.replace(tzinfo=pytz.timezone(timestamp.tzinfo.zone))  # Workaround for pandas bug
        building_tz = pytz.timezone(
            self.basking.location.get_building(building_id=building_id)['data']['getBuilding']['timeZone']
        )
        tz_conversion = building_tz.normalize if timestamp.tzinfo else building_tz.localize
        return datetime.utcfromtimestamp(
            tz_conversion(timestamp).replace(minute=0, second=0, microsecond=0).timestamp()
        )
