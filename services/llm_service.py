
import os
from groq import Groq
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY not found. Please check your .env file."
    )

# Initialize Groq client
client = Groq(api_key=api_key)


def generate_lead_insights(lead, scoring_result):

    # Extract official score and classification from Python
    score = scoring_result["score"]
    classification = scoring_result["classification"]

    # Prepare prompt for the LLM
    prompt = f"""
    You are an experienced B2B sales analyst.

    Analyze the following lead information:

    Lead Details:
    {lead}

    Official Lead Score: {score}/100
    Official Classification: {classification}

    Positive Scoring Factors:
    {scoring_result.get("positive_factors", [])}

    Negative Scoring Factors:
    {scoring_result.get("negative_factors", [])}

    Missing Fields:
    {scoring_result.get("missing_fields", [])}

    Provide the following sections:

    1. Lead Quality Assessment
    2. Scoring Explanation
    3. Recommended Next Action

    Important Rules:
    - The official score is {score}. Never change it.
    - The official classification is {classification}. Never change it.
    - Explain only the scoring factors provided above.
    - Never invent points or weightages.
    - Do not invent missing lead information.
    - Do not claim conversion probability or refer to past
      conversion rates because no such data is provided.
    - Give practical and professional sales recommendations.
    - Keep the response clear and concise.
    """

    # Send request to Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    # Extract AI-generated response
    insights = response.choices[0].message.content

    return insights
