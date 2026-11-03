
def classify_lead(score):

    if score >= 70:
        return "Hot"

    elif score >= 40:
        return "Warm"

    else:
        return "Cold"
