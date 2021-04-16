from unittest import mock
from pprint import pp, pprint
from datetime import date, datetime

import pytest

from wd2t.decision import Decision, create_decision, DecisionSchema


def test_new_decision():
    today = date.today()
    tags = [{"key": "type", "value": "component"}]
    _input = {
        "title": "A New Decision",
        "description": "Something we decided",
        "tags": tags,
        "decided_on": today,
    }

    DecisionSchema().load(_input)
    result = DecisionSchema().dump(_input)

    assert result["_id"] is not None
    assert result.title == _input["title"]
    assert result.description == _input["description"]
    assert result.decided_on == today
    assert result.tags == tags
    assert result.documented_at.timestamp() == pytest.approx(
        datetime.utcnow().timestamp()
    )
