from unittest import TestCase
from zuhause.utils.date_parser import parse_date
from datetime import date


class TestDateParser(TestCase):

    def test_date_parse_from(self):
        self.assertEqual("2016-10-30", parse_date("from 30.10.2016"))

    def test_date_range(self):
        self.assertEqual("2016-12-01", parse_date("01.12.2016 - 31.05.2017"))

    def test_date_immediately(self):
        self.assertEqual(date.today().isoformat(), parse_date("immediately"))

    def test_date_parse_german_format(self):
        self.assertEqual("2017-11-01", parse_date("01.11.2017"))

    def test_date_parse_german_format(self):
        self.assertEqual("2017-11-01", parse_date(" 01.11.2017 "))

    def test_date_parse_german_format_not_usual(self):
        self.assertEqual("2018-12-01", parse_date(" 01/12/2018 "))

    def test_date_parse_german_break_format(self):
        self.assertEqual("2018-01-09", parse_date(" 09/01/2018 "))

    def test_invalid_date_are_immediately(self):
        self.assertEqual(date.today().isoformat(), parse_date(" 1.10. "))

    def test_fix_wrong_formats(self):
        self.assertEqual(date.today().isoformat(), parse_date("  15.9.2018  "))



