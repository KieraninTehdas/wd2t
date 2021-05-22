from datetime import datetime

import pytest
from wd2t.datetime_utils import get_utc_today
from wd2t.models import DecisionBase


def test_decision_base():
    model_dict = {
        "title": "title",
        "description": "description",
        "tags": [],
        "decided_on": datetime(2020, 1, 1).date(),
    }

    model = DecisionBase.parse_obj(model_dict)

    assert model.decided_on == datetime(2020, 1, 1).date()


def test_decision_base_when_alias():
    model_dict = {
        "title": "title",
        "description": "description",
        "tags": [],
        "decidedOn": datetime(2020, 1, 1).date(),
    }

    model = DecisionBase.parse_obj(model_dict)

    assert model.decided_on == datetime(2020, 1, 1).date()


def test_decision_base_when_defaults():
    model_dict = {"title": "title", "description": "description", "tags": []}

    model = DecisionBase.parse_obj(model_dict)

    assert model.decided_on == get_utc_today()
