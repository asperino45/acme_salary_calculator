from challenge import Employee, rates_weekday
import unittest

class TestChallenge(unittest.TestCase):

    def setUp(self):
        self.employee_schedule = "ASTRID=MO10:00-12:00,TH12:00-14:00,SU20:00-21:00"
        self.employee = Employee.from_line(self.employee_schedule)
        self.default_rate = list(rates_weekday.keys())[1]

    def test_employee(self):
        self.assertEqual(self.employee.name, "ASTRID")

    def test_salary(self):
        self.assertEqual(self.employee.salary, 85)

    def test_schedule(self):
        self.assertEqual(
            self.employee.schedule,
            {
                "MO": ["10:00-12:00"],
                "TU": [],
                "WE": [],
                "TH": ["12:00-14:00"],
                "FR": [],
                "SA": [],
                "SU": ["20:00-21:00"],
            })

    def test_is_in_interval(self):
        is_in_interval = self.employee.is_in_interval("23:00", "01:00", self.default_rate)
        self.assertTrue(is_in_interval)

    def test_interval_overnight(self):
        is_overnight = self.employee.is_overnight("23:00", "01:00")
        self.assertTrue(is_overnight)

    def test_interval_not_between_rates(self):
        between_rates = self.employee.is_between_rates("08:00", "10:00", self.default_rate)
        self.assertFalse(between_rates)

    def test_interval_between_rates(self):
        between_rates = self.employee.is_between_rates("09:00", "10:00", self.default_rate)
        self.assertTrue(between_rates)

    def test_calculate_rate_overnight_weekday(self):
        rate = self.employee.calculate_rate("TH", "22:00-02:00")
        self.assertEqual(rate, 90)

    def test_calculate_rate_overnight_weekend(self):
        rate = self.employee.calculate_rate("FR", "22:00-02:00")
        self.assertEqual(rate, 100)

    def test_calculate_rate_not_is_between_rates(self):
        rate = self.employee.calculate_rate("FR", "16:00-20:00")
        self.assertEqual(rate, 70)


if __name__=="__main__":
    unittest.main()