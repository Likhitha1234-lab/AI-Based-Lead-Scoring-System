
from scoring.scoring_engine import process_lead


def get_sample_lead():
    return {
        "name": "Rahul",
        "company_name": "ABC Technologies",
        "website": "https://abc.com",
        "job_title": "CEO",
        "industry": "IT Services",
        "company_location": "Bangalore",
        "company_size": "500+",
        "lead_source": "Referral",
        "requirement": "We are ready to purchase an AI solution",
        "email": "rahul@example.com",
        "phone": "9876543210"
    }


def test_perfect_lead_score():
    lead = get_sample_lead()
    result = process_lead(lead)

    assert result["score"] == 100


def test_perfect_lead_classification():
    lead = get_sample_lead()
    result = process_lead(lead)

    assert result["classification"] == "Hot"


def test_weak_lead_score():
    lead = {
        "name": "Arun",
        "company_name": "Small Business",
        "website": None,
        "job_title": "Student",
        "industry": "Other",
        "company_location": "Bangalore",
        "company_size": "1-10",
        "lead_source": "Cold Email",
        "requirement": "Just exploring available options.",
        "email": "arun@example.com",
        "phone": None
    }

    result = process_lead(lead)

    assert result["score"] == 33
    assert result["classification"] == "Cold"


def test_score_never_exceeds_100():
    lead = get_sample_lead()
    result = process_lead(lead)

    assert result["score"] <= 100


def test_identical_inputs_produce_same_score():
    lead = get_sample_lead()

    result1 = process_lead(lead)
    result2 = process_lead(lead)

    assert result1["score"] == result2["score"]
