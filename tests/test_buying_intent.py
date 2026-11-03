
from scoring.scoring_engine import calculate_buying_intent


def test_strong_buying_intent():
    assert calculate_buying_intent(
        "We are ready to purchase a solution"
    )[0] == 30


def test_active_search():
    assert calculate_buying_intent(
        "We are looking for a solution"
    )[0] == 25


def test_exploring_options():
    assert calculate_buying_intent(
        "We are exploring available options"
    )[0] == 15


def test_negative_buying_intent():
    assert calculate_buying_intent(
        "We are not looking for a solution"
    )[0] == 0


def test_empty_requirement():
    assert calculate_buying_intent("")[0] == 0
