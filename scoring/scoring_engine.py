
from scoring.classification import classify_lead
from utils.validators import LeadInput
from utils.confidence import calculate_confidence


# 1. SCORING RULES

scoring_rules = {
    "job_title": {
        "Founder": 20,
        "CEO": 20,
        "Director": 17,
        "Manager": 14,
        "Executive": 10,
        "Student": 3
    },

    "company_size": {
        "500+": 15,
        "100-500": 13,
        "50-100": 10,
        "11-50": 7,
        "1-10": 4
    },

    "industry": {
        "IT Services": 10,
        "Healthcare": 9,
        "Finance": 9,
        "Manufacturing": 8,
        "Education": 7
    },

    "lead_source": {
        "Referral": 10,
        "Website": 9,
        "Social Media": 6,
        "Cold Email": 3
    }
}


# 2. BUYING INTENT SCORING


def calculate_buying_intent(requirement):

    if not requirement or not requirement.strip():
        return 0, "No requirement provided"

    text = requirement.lower()

    # Negative intent patterns
    negative_phrases = [
        "not looking",
        "not interested",
        "not ready",
        "not planning",
        "not willing",
        "not currently",
        "do not need",
        "don't need",
        "don't want",
        "do not want",
        "no requirement",
        "no intention",
        "not required"
    ]

    if any(phrase in text for phrase in negative_phrases):
        return 0, "No active buying intent identified"

    # Strong buying intent
    if any(word in text for word in [
        "purchase",
        "buy",
        "implement",
        "ready to invest"
    ]):
        return 30, "Strong purchase intention"

    # Active search
    elif any(word in text for word in [
        "looking for",
        "need a solution",
        "actively searching"
    ]):
        return 25, "Actively looking for a solution"

    # Comparing solutions
    elif any(word in text for word in [
        "comparing",
        "evaluating vendors",
        "shortlisting"
    ]):
        return 20, "Comparing available solutions"

    # Exploring options
    elif any(word in text for word in [
        "exploring",
        "researching"
    ]):
        return 15, "Exploring available options"

    # General enquiry
    else:
        return 8, "General business enquiry"



# 3. MAIN SCORING FUNCTION

def calculate_score(lead):

    score = 0
    positive_factors = []
    negative_factors = []
    missing_fields = []

    # JOB TITLE
    job_title = (lead.get("job_title") or "").strip()

    points = scoring_rules["job_title"].get(job_title, 0)
    score += points

    if points > 0:
        positive_factors.append(
            f"Job title: {job_title} (+{points})"
        )
    elif not job_title:
        missing_fields.append("job_title")

    # COMPANY SIZE
    company_size = (lead.get("company_size") or "").strip()

    points = scoring_rules["company_size"].get(company_size, 0)
    score += points

    if points > 0:
        positive_factors.append(
            f"Company size: {company_size} (+{points})"
        )
    elif not company_size:
        missing_fields.append("company_size")

    # INDUSTRY
    industry = (lead.get("industry") or "").strip()

    points = scoring_rules["industry"].get(industry, 0)
    score += points

    if points > 0:
        positive_factors.append(
            f"Industry: {industry} (+{points})"
        )
    elif not industry:
        missing_fields.append("industry")

    # LEAD SOURCE
    lead_source = (lead.get("lead_source") or "").strip()

    points = scoring_rules["lead_source"].get(lead_source, 0)
    score += points

    if points > 0:
        positive_factors.append(
            f"Lead source: {lead_source} (+{points})"
        )
    elif not lead_source:
        missing_fields.append("lead_source")

    # BUYING INTENT
    intent_points, intent_reason = calculate_buying_intent(
        lead.get("requirement") or ""
    )

    score += intent_points

    if intent_points > 0:
        positive_factors.append(
            f"{intent_reason} (+{intent_points})"
        )

    elif not (lead.get("requirement") or "").strip():
        missing_fields.append("requirement")

    else:
        negative_factors.append(intent_reason)

    # COMPANY PROFILE COMPLETENESS (10 POINTS)
    company_points = 0

    company_name = (lead.get("company_name") or "").strip()
    website = (lead.get("website") or "").strip()

    if company_name:
        company_points += 5
    else:
        missing_fields.append("company_name")

    if website:
        company_points += 5
    else:
        missing_fields.append("website")

    score += company_points

    if company_points > 0:
        positive_factors.append(
            f"Company profile completeness (+{company_points})"
        )

    # CONTACT INFORMATION COMPLETENESS (5 POINTS)
    contact_points = 0

    email = lead.get("email")
    phone = (lead.get("phone") or "").strip()

    if email:
        contact_points += 3
    else:
        missing_fields.append("email")

    if phone:
        contact_points += 2
    else:
        missing_fields.append("phone")

    score += contact_points

    if contact_points > 0:
        positive_factors.append(
            f"Contact information completeness (+{contact_points})"
        )

    # FINAL SCORE
    score = min(score, 100)

    return {
        "score": score,
        "positive_factors": positive_factors,
        "negative_factors": negative_factors,
        "missing_fields": missing_fields
    }


# 4. COMPLETE LEAD EVALUATION

def evaluate_lead(lead):

    result = calculate_score(lead)

    result["classification"] = classify_lead(
        result["score"]
    )

    return result


# 5. VALIDATION AND CONFIDENCE

def process_lead(lead_data):

    validated_lead = LeadInput(**lead_data)

    lead = validated_lead.model_dump()

    result = evaluate_lead(lead)

    confidence = calculate_confidence(lead)

    result["confidence_score"] = confidence["confidence_score"]
    result["confidence_level"] = confidence["confidence_level"]

    return result
