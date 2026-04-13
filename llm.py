import openai
import streamlit as st

# Use Streamlit secrets (for deployment)
openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_sql(question):
    try:
        prompt = f"""
        You are a SQL expert.

        Convert the user's question into a SQLite SQL query.

        Table name: matches
        Columns: team, opponent, goals, date

        Rules:
        - Only return SQL query
        - No explanation
        - No markdown
        - Output must start with SELECT

        Question: {question}
        SQL:
        """

        response = openai.ChatCompletion.create(
            model="gpt-4.1-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=100
        )

        return response['choices'][0]['message']['content'].strip()

    except Exception as e:
        return f"ERROR: {e}"
