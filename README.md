# 🎯 AI-Based Lead Scoring System

An AI-powered application that evaluates and prioritizes business leads using a transparent, rule-based scoring methodology and generates actionable sales insights using a Large Language Model (LLM).

Each lead gets a score between 0 and 100, a Hot, Warm or Cold classification, explainable scoring factors and AI-generated recommendations.

---

## 🏗️ System Architecture

![System Architecture](screenshots/architecture.png)

---

## 📸 Application Screenshots

### 1. Lead Information Form
![Lead Input Form](screenshots/01_lead_input.png)

### 2. Lead Scoring Results
![Lead Scoring Results](screenshots/02_scoring_results.png)

### 3. AI-Generated Insights
![AI Generated Insights](screenshots/03_ai_insights.png)

### 4. Lead History
![Lead History](screenshots/04_lead_history.png)

---

## 🚀 Key Features

- **Rule-Based Scoring:** Consistent 0-100 score using predefined rules and weightages.
- **Lead Classification:** Hot, Warm or Cold.
- **Explainable Scoring:** Shows positive and negative scoring factors.
- **Buying Intent Analysis:** Keyword-based evaluation of the lead's requirement.
- **Missing Information Handling:** Missing data is reported separately and not treated as negative evidence.
- **Confidence Assessment:** Based on the completeness of the lead information.
- **AI-Generated Insights:** Quality assessment, scoring explanation and next action using Groq LLM.
- **Lead History:** Evaluated leads are stored in SQLite and kept after restarting the app.

---

## 🛠️ Technology Stack

| Category | Technology |
|---|---|
| Language | Python |
| Frontend | Streamlit |
| Validation | Pydantic |
| LLM | Groq API (openai/gpt-oss-20b) |
| Database | SQLite |
| Testing | Pytest |

---

## ⚙️ Scoring Methodology

The system uses a weighted, rule-based scoring approach to evaluate business leads. Each lead receives a score between 0 and 100 based on seven predefined parameters.

| Scoring Parameter | Maximum Weightage |
|---|---:|
| Job Title | 20 |
| Company Size | 15 |
| Industry | 10 |
| Lead Source | 10 |
| Buying Intent | 30 |
| Company Profile Completeness | 10 |
| Contact Information Completeness | 5 |
| **Total** | **100** |

### 1. Job Title (20 Points)

Evaluates the lead's decision-making authority.

| Job Title | Points |
|---|---:|
| Founder | 20 |
| CEO | 20 |
| Director | 17 |
| Manager | 14 |
| Executive | 10 |
| Student | 3 |
| Other / Unknown | 0 |

### 2. Company Size (15 Points)

Evaluates the size and potential business value of the company.

| Company Size | Points |
|---|---:|
| 500+ employees | 15 |
| 100–500 employees | 13 |
| 50–100 employees | 10 |
| 11–50 employees | 7 |
| 1–10 employees | 4 |
| Unknown | 0 |

### 3. Industry (10 Points)

Evaluates industry relevance based on the defined business rules.

| Industry | Points |
|---|---:|
| IT Services | 10 |
| Healthcare | 9 |
| Finance | 9 |
| Manufacturing | 8 |
| Education | 7 |
| Other / Unknown | 0 |

### 4. Lead Source (10 Points)

Evaluates how the lead was acquired.

| Lead Source | Points |
|---|---:|
| Referral | 10 |
| Website | 9 |
| Social Media | 6 |
| Cold Email | 3 |
| Unknown | 0 |

### 5. Buying Intent (30 Points)

Evaluates the lead's purchase intention using keyword-based rule matching.

| Requirement / Intent | Points |
|---|---:|
| Strong purchase intention | 30 |
| Actively looking for a solution | 25 |
| Comparing available solutions | 20 |
| Exploring available options | 15 |
| General business enquiry | 8 |
| No requirement / Negative intent | 0 |

The system checks predefined positive and negative phrases. Negative-intent checks are performed before positive keyword matching to avoid awarding purchase-intent points to the tested negative statements.

### 6. Company Profile Completeness (10 Points)

Evaluates the availability of company information.

| Information | Points |
|---|---:|
| Company Name provided | 5 |
| Website provided | 5 |

### 7. Contact Information Completeness (5 Points)

Evaluates the availability of contact details.

| Information | Points |
|---|---:|
| Valid Email provided | 3 |
| Phone Number provided | 2 |

### Total Score Calculation

The final lead score is calculated by adding the points earned across all seven parameters.

**Maximum Possible Score: 100**

### Lead Classification

| Score Range | Classification |
|---|---|
| 70–100 | Hot |
| 40–69 | Warm |
| 0–39 | Cold |

### Important Scoring Rules

- The scoring engine uses predefined rules, ensuring consistent results for identical inputs.
- Missing information is tracked separately from negative scoring factors.
- Unknown or unrecognized values receive zero points for the corresponding category.
- The final score is capped at 100.
- Confidence level is calculated separately based on lead information completeness; it is not a conversion probability.

### Role of the LLM

Python is responsible for calculating the official score and classification.

Groq LLM is used only to generate the lead quality assessment, scoring explanation, and recommended next action. It does not modify the official score or classification.

---

## 💻 Installation and Setup

```bash
git clone https://github.com/Likhitha1234-lab/AI-Based-Lead-Scoring-System.git
cd AI-Based-Lead-Scoring-System
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root and add your Groq API key:

```env
GROQ_API_KEY=your_groq_api_key
```

Run the application:

```bash
streamlit run app.py
```

---

## 🧪 Testing

```bash
pytest -v
```

Tests cover score calculation, Hot/Warm/Cold boundaries, buying intent, missing information and consistency of results.