import streamlit as st

from scoring.scoring_engine import process_lead
from services.llm_service import generate_lead_insights
from database.db import create_table, save_lead, get_all_leads


# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Lead Scoring System",
    page_icon="🎯",
    layout="wide"
)


# SOFT COLOUR THEME
st.markdown("""
<style>

/* Main Background */
.stApp {
    background-color: #F7F5FC;
}

[data-testid="stHeader"] {
    background-color: #F7F5FC;
}

/* Headings */
h1 {
    color: #51446F !important;
}

h2, h3, h4 {
    color: #625779 !important;
}

/* General Text Visibility */
p, label,
.stMarkdown,
[data-testid="stMarkdownContainer"],
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li,
[data-testid="stMarkdownContainer"] strong,
[data-testid="stMarkdownContainer"] span {
    color: #403858 !important;
}

/* AI Insights and Markdown Content */
[data-testid="stMarkdownContainer"] {
    color: #403858 !important;
}

[data-testid="stMarkdownContainer"] table {
    color: #403858 !important;
    border-collapse: collapse;
    width: 100%;
}

[data-testid="stMarkdownContainer"] th {
    background-color: #E9E2F5 !important;
    color: #403858 !important;
    padding: 12px;
    text-align: left;
}

[data-testid="stMarkdownContainer"] td {
    background-color: #FFFFFF !important;
    color: #403858 !important;
    padding: 12px;
    border-bottom: 1px solid #E5DFF0 !important;
}

/* Markdown Headings */
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3,
[data-testid="stMarkdownContainer"] h4 {
    color: #51446F !important;
}

/* Buttons */
div.stButton > button,
div.stFormSubmitButton > button {
    background-color: #8875B9;
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 10px 22px;
}

div.stButton > button:hover,
div.stFormSubmitButton > button:hover {
    background-color: #71609F;
    color: white !important;
    border: none;
}

/* Metrics */
div[data-testid="stMetric"] {
    background-color: white;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #E9E3F2;
}

/* Input Form */
div[data-testid="stForm"] {
    background-color: #FFFFFF;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E9E3F2;
}

/* Expanders */
div[data-testid="stExpander"] {
    background-color: white;
    border-radius: 12px;
    border: 1px solid #E9E3F2;
}

/* Divider */
hr {
    border-color: #E5DFF0;
}

</style>
""", unsafe_allow_html=True)


# DATABASE INITIALIZATION
create_table()


# HEADER
st.title("🎯 AI-Based Lead Scoring System")

st.write(
    "Evaluate, understand and prioritize your business leads using AI."
)

st.divider()


# LEAD INPUT FORM
st.subheader("📝 Enter Lead Information")

with st.form("lead_form"):

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input("Full Name")

        company_name = st.text_input("Company Name")

        website = st.text_input("Website")

        job_title = st.text_input("Job Title")

        industry = st.selectbox(
            "Industry",
            [
                "IT Services",
                "Healthcare",
                "Finance",
                "Education",
                "Manufacturing",
                "Other"
            ]
        )

        company_location = st.text_input("Company Location")

    with col2:

        company_size = st.selectbox(
            "Company Size",
            [
                "1-10",
                "11-50",
                "50-100",
                "100-500",
                "500+"
            ]
        )

        lead_source = st.selectbox(
            "Lead Source",
            [
                "Website",
                "Referral",
                "Social Media",
                "Cold Email"
            ]
        )

        requirement = st.text_area("Business Requirement")

        email = st.text_input("Email Address")

        phone = st.text_input("Phone Number")

    submitted = st.form_submit_button(
        "Evaluate Lead",
        use_container_width=True
    )


# EVALUATE LEAD
if submitted:

    lead = {
        "name": name,
        "company_name": company_name,
        "website": website or None,
        "job_title": job_title,
        "industry": industry,
        "company_location": company_location,
        "company_size": company_size,
        "lead_source": lead_source,
        "requirement": requirement,
        "email": email,
        "phone": phone or None
    }


    # PYTHON SCORING
    try:

        with st.spinner("Calculating lead score..."):

            result = process_lead(lead)

    except Exception as e:

        st.error(f"Unable to evaluate lead: {e}")

        st.stop()


    # GROQ AI INSIGHTS
    insights = "AI insights are temporarily unavailable."

    try:

        with st.spinner("Generating AI insights..."):

            insights = generate_lead_insights(
                lead,
                result
            )

    except Exception as e:

        st.warning(
            "AI insights are temporarily unavailable. "
            "Your Python scoring result is still available."
        )

        st.caption(f"AI service error: {e}")


    # SAVE TO DATABASE
    try:

        save_lead(lead, result, insights)

        st.success("Lead evaluated and saved successfully!")

    except Exception as e:

        st.error(f"Database saving failed: {e}")


    # RESULTS
    st.divider()

    st.subheader("📊 Lead Scoring Results")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Lead Score",
            f'{result["score"]}/100'
        )

    with col2:

        st.metric(
            "Classification",
            result["classification"]
        )

    with col3:

        st.metric(
            "Confidence Level",
            result["confidence_level"],
            f'{result["confidence_score"]}% data completeness'
        )


    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        st.markdown("### 🟢 Positive Factors")

        if result["positive_factors"]:

            for factor in result["positive_factors"]:

                st.success(factor)

        else:

            st.info("No positive factors found.")


    with col2:

        st.markdown("### 🟠 Negative Factors")

        if result["negative_factors"]:

            for factor in result["negative_factors"]:

                st.warning(factor)

        else:

            st.info("No negative factors found.")


    # MISSING INFORMATION
    st.markdown("### 📌 Missing Information")

    if result["missing_fields"]:

        st.write(", ".join(result["missing_fields"]))

    else:

        st.success("No missing information.")


    st.divider()


    # AI-GENERATED INSIGHTS
    st.subheader("🤖 AI-Generated Insights")

    st.markdown(insights)


# LEAD HISTORY
st.divider()

st.subheader("📁 Lead History")

try:

    leads = get_all_leads()

    if leads:

        st.write(f"Total evaluated leads: {len(leads)}")

        for lead in leads:

            lead_id = lead[0]

            lead_name = lead[1]

            company = lead[2]

            score = lead[12]

            classification = lead[13]

            confidence = lead[15]

            insights = lead[19]

            created_at = lead[20]


            with st.expander(
                f"👤 {lead_name} - {company} | "
                f"{score}/100 | {classification}"
            ):

                col1, col2 = st.columns(2)

                with col1:

                    st.write("Lead ID:", lead_id)

                    st.write("Name:", lead_name)

                    st.write("Company:", company)

                with col2:

                    st.write("Score:", score)

                    st.write("Classification:", classification)

                    st.write("Confidence:", confidence)


                st.caption(f"Created at: {created_at}")

                st.markdown("#### AI Insights")

                st.markdown(insights)

    else:

        st.info("No leads have been evaluated yet.")


except Exception as e:

    st.error(f"Unable to retrieve lead history: {e}")
