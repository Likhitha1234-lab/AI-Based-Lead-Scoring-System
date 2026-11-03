
def calculate_confidence(lead):

    # Fields used to calculate data completeness
    important_fields = [
        "name",
        "company_name",
        "job_title",
        "industry",
        "company_location",
        "company_size",
        "lead_source",
        "requirement",
        "email"
    ]

    completed_fields = 0

    # Count fields containing information
    for field in important_fields:

        value = lead.get(field)

        if value and str(value).strip():
            completed_fields += 1

    # Calculate completeness percentage
    total_fields = len(important_fields)

    confidence_score = round(
        (completed_fields / total_fields) * 100
    )

    # Determine confidence level
    if confidence_score >= 90:
        confidence_level = "High"

    elif confidence_score >= 70:
        confidence_level = "Medium"

    else:
        confidence_level = "Low"

    return {
        "confidence_score": confidence_score,
        "confidence_level": confidence_level
    }
