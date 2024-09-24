from flask_admin.contrib.sqla.filters import BaseSQLAFilter
from datetime import datetime, timedelta

class CustomDateRangeFilter(BaseSQLAFilter):
    def __init__(self, column, name):
        super().__init__(column, name)

    def apply(self, query, value, alias=None):
        # Az aktuális dátumokat itt határozzuk meg, minden kérésnél újra
        start_date, end_date = self.get_date_range()
        return query.filter(self.column.between(start_date, end_date))

    def operation(self):
        start_date, end_date = self.get_date_range()
        return f"Date between {start_date} and {end_date}"

    def get_date_range(self):
        """Ez a metódus adja vissza a dátumtartományokat, amelyeket a szűrők fognak használni"""
        raise NotImplementedError("Subclasses must implement this method")

class TodayFilter(CustomDateRangeFilter):
    def __init__(self, column):
        super().__init__(column, 'Today')

    def get_date_range(self):
        today = datetime.now()
        start_date = today.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=1)
        return start_date, end_date

class ThisWeekFilter(CustomDateRangeFilter):
    def __init__(self, column):
        super().__init__(column, 'This Week')

    def get_date_range(self):
        today = datetime.now()
        start_date = today - timedelta(days=today.weekday())  # Hét eleje (hétfő)
        start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)
        end_date = start_date + timedelta(days=7)  # A hét végéig (vasárnap)
        return start_date, end_date

class ThisMonthFilter(CustomDateRangeFilter):
    def __init__(self, column):
        super().__init__(column, 'This Month')

    def get_date_range(self):
        today = datetime.now()
        start_date = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)  # Hónap első napja
        if today.month == 12:
            end_date = start_date.replace(year=start_date.year + 1, month=1)  # Következő hónap
        else:
            end_date = start_date.replace(month=start_date.month + 1)  # Következő hónap
        return start_date, end_date
