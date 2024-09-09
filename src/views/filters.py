from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from datetime import datetime, timedelta

class CustomDateRangeFilter(BaseSQLAFilter):
    def __init__(self, column, name, start_date=None, end_date=None):
        super().__init__(column, name)
        self.start_date = start_date
        self.end_date = end_date

    def apply(self, query, value, alias=None):
        # Alapértelmezett értékek használata, ha nincs megadva érték
        start_date = self.start_date or datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = self.end_date or start_date + timedelta(days=1)
        return query.filter(self.column.between(start_date, end_date))

    def operation(self):
        return f"Date between {self.start_date} and {self.end_date}"

class TodayFilter(CustomDateRangeFilter):
    def __init__(self, column):
        today = datetime.now()
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        super().__init__(column, 'Today', start_date, end_date)

class ThisWeekFilter(CustomDateRangeFilter):
    def __init__(self, column):
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday())
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=7)
        super().__init__(column, 'This Week', start_date, end_date)

class ThisMonthFilter(CustomDateRangeFilter):
    def __init__(self, column):
        today = datetime.now()
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if today.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1)
        else:
            end_date = start_date.replace(month=start_date.month + 1)
        super().__init__(column, 'This Month', start_date, end_date)