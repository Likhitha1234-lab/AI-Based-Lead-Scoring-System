
import sqlite3
import json


# Database file
DATABASE_NAME = "leads.db"


def get_connection():

    connection = sqlite3.connect(DATABASE_NAME)

    return connection


def create_table():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS leads (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            company_name TEXT NOT NULL,

            website TEXT,

            job_title TEXT,

            industry TEXT,

            company_location TEXT,

            company_size TEXT,

            lead_source TEXT,

            requirement TEXT,

            email TEXT NOT NULL,

            phone TEXT,

            score INTEGER,

            classification TEXT,

            confidence_score INTEGER,

            confidence_level TEXT,

            positive_factors TEXT,

            negative_factors TEXT,

            missing_fields TEXT,

            ai_insights TEXT,

            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()

    connection.close()


def save_lead(lead, result, insights):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        INSERT INTO leads (
            name,
            company_name,
            website,
            job_title,
            industry,
            company_location,
            company_size,
            lead_source,
            requirement,
            email,
            phone,
            score,
            classification,
            confidence_score,
            confidence_level,
            positive_factors,
            negative_factors,
            missing_fields,
            ai_insights
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        lead["name"],
        lead["company_name"],
        lead.get("website"),
        lead["job_title"],
        lead["industry"],
        lead["company_location"],
        lead["company_size"],
        lead["lead_source"],
        lead["requirement"],
        str(lead["email"]),
        lead.get("phone"),
        result["score"],
        result["classification"],
        result["confidence_score"],
        result["confidence_level"],
        json.dumps(result["positive_factors"]),
        json.dumps(result["negative_factors"]),
        json.dumps(result["missing_fields"]),
        insights
    ))

    connection.commit()

    connection.close()


def get_all_leads():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute("""
        SELECT * FROM leads
        ORDER BY created_at DESC
    """)

    records = cursor.fetchall()

    connection.close()

    return records
