import streamlit as st
import pandas as pd
import sqlite3
from llm import generate_sql

# -------------------- PAGE CONFIG --------------------
st.set_page_config(
    page_title="Football AI Assistant",
    page_icon="⚽",
    layout="wide"
)

# -------------------- CUSTOM STYLING --------------------
st.markdown("""
<style>
.main {
    background-color: #0e1117;
}
.block-container {
    padding-top: 2rem;
}
.stTextInput > div > div > input {
    background-color: #262730;
    color: white;
}
</style>
""", unsafe_allow_html=True)

# -------------------- DATABASE CONNECTION --------------------
conn = sqlite3.connect("football.db")

# -------------------- SIDEBAR --------------------
st.sidebar.title("⚽ Football AI")

st.sidebar.markdown("### 💡 Example Questions")
st.sidebar.write("• Top scoring teams")
st.sidebar.write("• Average goals per match")
st.sidebar.write("• Matches in 2023")

st.sidebar.markdown("---")
st.sidebar.write("Built by Dhruv 🚀")

# -------------------- HEADER --------------------
st.markdown("""
## ⚽ Football AI Assistant  
Ask football questions using AI + SQL
""")

# -------------------- CHAT MEMORY --------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# -------------------- INPUT --------------------
question = st.text_input("Ask a question:")

# -------------------- PROCESS QUESTION --------------------
if question:
    st.session_state.chat_history.append(("user", question))

    with st.spinner("Thinking... 🤔"):
        sql_query = generate_sql(question)

    try:
        df = pd.read_sql(sql_query, conn)
        st.session_state.chat_history.append(("bot", (sql_query, df)))
    except Exception as e:
        st.session_state.chat_history.append(("bot", ("ERROR", str(e))))

# -------------------- DISPLAY CHAT --------------------
for role, message in st.session_state.chat_history:

    if role == "user":
        st.markdown(f"**🧑 You:** {message}")

    else:
        sql_query, result = message

        st.markdown("**🤖 AI Response:**")

        if sql_query == "ERROR":
            st.error(result)

        else:
            # SQL Expander
            with st.expander("🔍 View Generated SQL"):
                st.code(sql_query, language="sql")

            # Results
            st.success("✅ Results ready!")
            st.dataframe(result, use_container_width=True)

            # Metrics
            if not result.empty:
                col1, col2 = st.columns(2)

                with col1:
                    st.metric("Rows Returned", len(result))

                with col2:
                    st.metric("Columns", len(result.columns))

                # Chart
                try:
                    st.write("### 📈 Insights")
                    st.bar_chart(result.set_index(result.columns[0]))
                except:
                    pass