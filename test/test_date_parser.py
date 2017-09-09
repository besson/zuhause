from unittest import TestCase
from zuhause.utils.date_parser import parse_date
from datetime import date


class TestDateParser(TestCase):

    def test_date_parse_from(self):
        self.assertEquals("2016-10-30", parse_date("from 30.10.2016"))

    def test_date_range(self):
        self.assertEquals("2016-12-01", parse_date("01.12.2016 - 31.05.2017"))

    def test_date_immediately(self):
        self.assertEquals(date.today().isoformat(), parse_date("immediately"))

    def test_date_parse_german_format(self):
        self.assertEquals("2017-11-01", parse_date("01.11.2017"))

    def test_date_parse_german_format(self):
        self.assertEquals("2017-11-01", parse_date(" 01.11.2017 "))
