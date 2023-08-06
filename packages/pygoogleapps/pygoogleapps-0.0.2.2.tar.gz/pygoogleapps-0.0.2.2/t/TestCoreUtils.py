import pytest
import sys, re
import datetime
import dateutil
import time
sys.path.insert(0,'.')
import googleapps

class TestCamel():

    def setup_class(self):
        # Many Test Cases taken from strcase, a Go conversion module by Ian Coleman (2015, 2018)
        # https://github.com/iancoleman/strcase/blob/master/snake_test.go

        self.to_snake_cases = [
		    ("numbers2and55with000", "numbers_2_and_55_with_000"),
		    ("testCase", "test_case"),
		    ("TestCase", "test_case"),
		    (" TestCase", "test_case"),
		    ("TestCase ", "test_case"),
		    (" testCase ", "test_case"),
		    ("test", "test"),
		    ("Test", "test"),
		    ("ManyManyWords", "many_many_words"),
		    ("manyManyWords", "many_many_words"),
		    ("AnyKindOf_string", "any_kind_of_string"),
		    ("JSONData", "json_data"),
		    ("userID", "user_id"),
            ("middleATMJunk", "middle_atm_junk"),
		    ("AAAbbb", "aa_abbb"),
		    ("10Four","10_four"),
            ("tenFour","ten_four"),
            ("ten4","ten_4"),
        ]


        self.to_camel_cases = [
		    ("test_case","testCase"),
		    (" test_case","testCase"),
		    ("test_case ","testCase"),
		    (" test_case ","testCase"),
		    ("test","test"),
		    ("many_many_words","manyManyWords"),
		    ("any_kind_of_string","anyKindOfString"),
		    ("numbers_2_and_55_with_000","numbers2And55With000"),
		    ("10_four","10Four"),
            ("ten_four","tenFour"),
            ("ten_4","ten4"),
		    ("json_data","jsonData"),
		    ("user_id","userId"),
		    ("aa_abbb","aaAbbb"),
        ]

    def test_camel_case(self):
        for case in self.to_camel_cases:
            assert googleapps.toCamel(case[0]) == case[1], "Failed to convert " + case[0] + " to CamelCase (expected "+case[1]+", but got "+googleapps.toCamel(case[0])+")"

    def test_snake_case(self):
        for case in self.to_snake_cases:
            assert googleapps.fromCamel(case[0]) == case[1], "Failed to convert " + case[0] + " to snake_case (expected "+case[1]+", but got "+googleapps.fromCamel(case[0])+")"



class TestRFC3339():

    def setup_class(self):
        tz_hour_offset = datetime.datetime.now(dateutil.tz.tzlocal()).utcoffset().total_seconds()/3600
        self.tzoffset = str(int(tz_hour_offset)) + ':00'

        # these should be valid to test in all situations
        self.cases = [
            ("1985-04-12T23:20:50.52Z",   (1985, 4,  12, 23, 20, 50, 520000, datetime.timezone.utc)),
            ("1996-12-19T16:39:57-08:00", (1996, 12, 19, 16, 39, 57,  0, datetime.timezone(datetime.timedelta(hours=-8)))),
            ("1990-12-31T23:59:59Z",      (1990, 12, 31, 23, 59, 59,  0, datetime.timezone.utc)),
            ("1990-12-31T15:59:01-08:00", (1990, 12, 31, 23, 59, 1,  0, datetime.timezone.utc)),
            ("2008-04-02T20:00:00Z",      (2008,  4,  2, 20,  0,  0,  0, datetime.timezone.utc)),
            ("1970-01-01T00:00:00Z",      (1970, 1, 1, 0,0,0,0, datetime.timezone.utc)),
            ("1996-12-19T16:39:57-08:00", (1996, 12, 19, 16, 39, 57,0, datetime.timezone(datetime.timedelta(hours=-8)))),
            ("1937-01-01T00:00:27.87+00:30", (1937, 1, 1, 0, 00, 27, 870000, datetime.timezone(datetime.timedelta(hours=.5)))),
            ("1937-01-01T01:00:27.87+00:30", (1937, 1, 1, 0, 30, 27, 870000, datetime.timezone.utc)),
        ]
        # these include time equations that cross days, so we can't use them test to datetime.date or datetime.time options
        self.datetime_only = [
            ("1996-12-19T16:39:57-08:00", (1996, 12, 20,  0, 39, 57,  0, datetime.timezone.utc)),
            ("1937-01-01T00:00:27.87+00:30", (1936, 12, 31, 23, 30, 27, 870000, datetime.timezone.utc)),
        ]

    def test_from_rfctime(self):
        for rfc, params in self.cases + self.datetime_only:
            assert googleapps.from_rfctime(rfc) == datetime.datetime(*params), "Failed to identify " + rfc

    def test_to_rfctime(self):
        for rfc, params in self.cases + self.datetime_only:
            dt = datetime.datetime(*params)
            assert  googleapps.from_rfctime(googleapps.to_rfctime(dt)) ==  googleapps.from_rfctime(rfc), "Failed to identify " + str(dt)

    def test_to_rfctime_dateonly(self):
        for rfc, params in self.cases:
            dt = datetime.date(*params[0:3])

            # find local timezone
            lt = time.localtime(datetime.datetime(*params).timestamp())
            if lt.tm_isdst:
                # daylight savings
                seconds = -time.altzone
            else:
                seconds = -time.timezone
            difftime = seconds / 3600
            hours = int(difftime)
            if hours < 0:
                tzi = format(hours, '03d') + ':' + format(int((hours-difftime)*60), '02d')
            else:
                tzi = '+' + format(hours, '03d') + ':' + format(int((difftime-hours)*60), '02d')

            rfcnotime = re.sub(r'T.*', 'T00:00:00' + tzi, rfc)
            assert googleapps.to_rfctime(dt) == rfcnotime, "Failed to identify " + str(dt)

    def test_to_rfctime_epoch(self):
        for rfc, params in self.cases + self.datetime_only:
            dt = datetime.datetime(*params)
            epochtime = datetime.datetime(*params).timestamp()
            #
            # So right, this test is really just making sure that using epoch time works.
            # But it stands on the shoulders of (possibly deformed) giants in that it uses both
            # to_rfctime and from_rfctime in the test. If those are broken, abandon all hope
            assert googleapps.from_rfctime(googleapps.to_rfctime(epochtime)) == googleapps.from_rfctime(googleapps.to_rfctime(dt)), "Failed to identify " + rfc + " from " + str(epochtime)
