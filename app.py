import streamlit as st
import pandas as pd
from langchain_config import llm_chain, get_summary


# Storage for queries
if "query_history" not in st.session_state:
    st.session_state.query_history = []

query = st.text_input("Enter your query")

if st.button("Get News 📰"):
    if query:
        summaries = get_summary(query)
        response = llm_chain.run({"query": query, "summaries": summaries})

        # Save Query & Response
        st.session_state.query_history.append({"Query": query, "Summary": response})

        st.subheader("🔹 Summary:")
        st.write(response)

        # Download as CSV
        df = pd.DataFrame(st.session_state.query_history)
        csv = df.to_csv(index=False).encode("utf-8")

        st.download_button("📥 Download History", csv, "summary_history.csv", "text/csv")
