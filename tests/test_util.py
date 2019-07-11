import pytest
from runium.util import get_seconds


class TestGetSeconds(object):

    def test_number(self):
        assert get_seconds(10) == 10

    def test_float(self):
        assert get_seconds(1.2) == 1.2

    def test_seconds_string(self):
        assert get_seconds('10 seconds') == 10

    def test_minutes_string(self):
        assert get_seconds('10 minutes') == 600

    def test_hours_string(self):
        assert get_seconds('10 hours') == 36000

    def test_days_string(self):
        assert get_seconds('10 days') == 864000

    def test_invalid_string(self):
        pytest.raises(ValueError, get_seconds, 'abcd')

    def test_invalid_scale_string(self):
        pytest.raises(ValueError, get_seconds, '10 months')

    def test_invalid_type(self):
        pytest.raises(TypeError, get_seconds, [10])

    def test_none(self):
        assert get_seconds(None) is None
