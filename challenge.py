import sys

DoW = {
    "MO": "Monday",
    "TU": "Tuesday",
    "WE": "Wednesday",
    "TH": "Thursday",
    "FR": "Friday",
    "SA": "Saturday",
    "SU": "Sunday",
}

weekday = ["MO", "TU", "WE", "TH", "FR"]
weekend = ["SA", "SU"]

rates_weekday = {
    ("00:01", "09:00"): 25,
    ("09:01", "18:00"): 15,
    ("18:01", "00:00"): 20,
}

rates_weekend = {
    ("00:01", "09:00"): 30,
    ("09:01", "18:00"): 20,
    ("18:01", "00:00"): 25,
}

class Employee:

    salary = 0

    def __init__(self, name, schedule):
        self.name = name
        self.schedule = self.import_schedule(schedule)
        self.salary = self.calculate_salary()

    @staticmethod
    def from_line(line):
        (name, schedule) = line.split("=")
        return Employee(name, schedule)

    def import_schedule(self, raw_schedule):
        intervals = raw_schedule.split(",")
        schedule = {
            dow: [] for dow in DoW.keys()
        }

        for interval in intervals:
            interval_dow = interval[0:2]
            interval_hours = interval[2:]
            schedule[interval_dow].append(interval_hours)

        return schedule

    def calculate_salary(self):
        salary = 0

        for day_key, intervals in self.schedule.items():
            for interval in intervals:
                salary += self.calculate_rate(day_key, interval)

        return salary

    def is_in_interval_start(self, start, rates):
        (start_hour, start_mins) = start.split(":")
        (rate_hour, rate_mins) = rates[0].split(":")
        return (
            start_hour >= rate_hour
            and start_hour <= "24"
            and (start_mins == '00' or start_mins >= rate_mins)
        )

    def is_in_interval_end(self, end, rates):
        (end_hour, end_mins) = end.split(":")
        (rate_hour, rate_mins) = rates[1].split(":")
        return (
            (end_hour <= rate_hour
                or (
                    rate_hour == "00"
                        and (end_hour == "00" or end_hour <= "24")))
            and (end_mins <= "59" or end_mins <= rate_mins)
        )

    def is_in_interval(self, start, end, rates):
        return (
            self.is_in_interval_start(start, rates)
                and self.is_in_interval_end(end, rates)
        )

    def is_between_rates(self, start, end, rates):
        (start_hour, start_mins) = start.split(":")
        (end_hour, end_mins) = end.split(":")
        (rate_start_hour, rate_start_mins) = rates[0].split(":")
        (rate_end_hour, rate_end_mins) = rates[1].split(":")

        return (
            start_hour >= rate_start_hour
                and end_hour <= rate_end_hour
        )

    def is_overnight(self, start, end):
        (start_hour, start_mins) = start.split(":")
        (end_hour, end_mins) = end.split(":")

        return (
            start_hour != "00"
            and start_hour <= "23"
        ) and (
            end_hour >= "00"
            and end_hour != "00"
        ) and end_hour <= start_hour

    def get_hours(self, interval):
        (start, end) = interval.split("-")
        end_val = int(end.split(":")[0]) if end.split(":")[0] != "00" else 24
        return end_val - int(start.split(":")[0])

    def get_rate(self, start, end, rates):
        return next((
            key
            for key in rates.keys()
            if self.is_in_interval(start, end, key)
        ), None)

    def get_start_rate(self, start, rates):
        return next((
            key
            for key in rates.keys()
            if self.is_in_interval_end(start, key)
        ), None)

    def get_next_day(self, day):
        if day == weekend[1]:
            return weekday[0]
        elif day == weekday[4]:
            return weekend[0]
        else:
            return (
                weekday[weekday.index(day) + 1]
                    if day in weekday
                    else weekend[weekend.index(day) + 1]
            )

    def calculate_rate(self, day, interval):
        (start, end) = interval.split("-")
        rates = None

        if day in weekday:
            rates = rates_weekday
        elif day in weekend:
            rates = rates_weekend
        else:
            raise RuntimeError("Day format is wrong or non existent.")

        rate = self.get_rate(start, end, rates)

        if rate is not None and not self.is_overnight(start, end):
            return rates[rate] * self.get_hours(interval)

        first_rate = self.get_start_rate(start, rates)

        if first_rate is None:
            raise RuntimeError()

        rate1 = rates[first_rate] * self.get_hours(f"{start}-{first_rate[1]}")

        if not self.is_overnight(start, end) and not self.is_between_rates(start, end, first_rate):
            rate2 = self.calculate_rate(day, f"{first_rate[1]}-{end}")
            return rate1 + rate2

        elif self.is_overnight(start, end):
            rate2 = self.calculate_rate(self.get_next_day(day), f"00:00-{end}")
            return rate1 + rate2

        raise RuntimeError(f"Could not fit time interval {interval} in any rate.")

if __name__=="__main__":
    sys.setrecursionlimit(20)
    with open("input.txt", "r") as file:
        for line in file.readlines():
            employee = Employee.from_line(line)
            print(f"The amount to pay {employee.name} is: {employee.salary} USD")
