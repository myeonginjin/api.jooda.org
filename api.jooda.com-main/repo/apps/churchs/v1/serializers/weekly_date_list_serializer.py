from apps.churchs.models import ChurchWeekly
from datetime import datetime


class ChurchWeeklyDeteListSerializer:
    def get_date_list(date_list: ChurchWeekly) -> list:
        formatted_date_list = []
        for year, month in date_list:
            date = datetime(int(year), int(month), 1)
            formatted_date_list.append(f"20{date.strftime('%y년 %m월')}")

        return formatted_date_list
