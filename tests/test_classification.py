
from scoring.classification import classify_lead


def test_hot_classification():
    assert classify_lead(80) == "Hot"


def test_warm_classification():
    assert classify_lead(55) == "Warm"


def test_cold_classification():
    assert classify_lead(25) == "Cold"


def test_classification_boundaries():
    assert classify_lead(70) == "Hot"
    assert classify_lead(40) == "Warm"
    assert classify_lead(39) == "Cold"
