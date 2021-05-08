from datetime import datetime

import pytest
from wd2t import datetime_utils


def test_get_utc_now():
    assert datetime_utils.get_utc_now().timestamp() == pytest.approx(
        datetime.utcnow().timestamp()
    )


def test_get_utc_today():
    assert datetime_utils.get_utc_today() == datetime.utcnow().date()
