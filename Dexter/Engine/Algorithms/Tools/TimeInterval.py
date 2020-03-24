from datetime import datetime, timedelta


class TimeInterval:
    """Used to handle various dateTime related operations"""

    def __init__(self, start_date_string, end_date_string, format_=None):
        if format_ is None:
            self.start_date = datetime.fromisoformat(start_date_string)
            self.end_date = datetime.fromisoformat(end_date_string)
        else:
            self.start_date = datetime.strptime(start_date_string, format_)
            self.end_date = datetime.strptime(end_date_string, format_)

    def get_start_date_string(self, given_format=None):
        if given_format is None:
            return self.start_date.isoformat()
        else:
            return self.start_date.strftime(given_format)

    def get_end_date_string(self, given_format=None):
        if given_format is None:
            return self.end_date.isoformat()
        else:
            return self.end_date.strftime(given_format)

    def to_string(self, given_format=None):
        # Used for logging
        return 'StartDate = ' + self.get_start_date_string(given_format) + ', EndDate = ' + self.get_end_date_string(given_format)

    def get_time_delta(self):
        delta = self.end_date - self.start_date
        return delta.total_seconds() / timedelta(days=1).total_seconds()

    @staticmethod
    def get_date_time_object(date_string, given_format=None):
        if given_format is None:
            return datetime.fromisoformat(date_string)
        else:
            return datetime.strptime(date_string, given_format)

    # TODO: check this
    @staticmethod
    def get_time_delta(start_date, end_date):
        delta = end_date - start_date
        return delta.total_seconds() / timedelta(days=1).total_seconds()
