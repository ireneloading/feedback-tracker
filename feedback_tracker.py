import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# ---- App Title ----
st.set_page_config(page_title="Client Feedback Tracker", layout="centered")
st.title("📝 Client Feedback Tracker")
st.write("Track and analyze feedback from your clients using simple charts.")

# ---- Initialize Data ----
if 'feedback_data' not in st.session_state:
    st.session_state.feedback_data = pd.DataFrame(columns=[
        "Client Name", "Feedback Type", "Rating", "Comments", "Date"
    ])

# ---- Feedback Entry Form ----
st.header("Submit Feedback")
with st.form("feedback_form"):
    client_name = st.text_input("Client Name (optional)")
    feedback_type = st.selectbox("Feedback Type", ["Positive", "Neutral", "Negative"])
    rating = st.slider("Rating", 1, 5, step=1)
    comments = st.text_area("Comments")
    date = st.date_input("Date", value=datetime.today())
    submit = st.form_submit_button("Add Feedback")

    if submit:
        new_entry = {
            "Client Name": client_name,
            "Feedback Type": feedback_type,
            "Rating": rating,
            "Comments": comments,
            "Date": pd.to_datetime(date)
        }
        st.session_state.feedback_data = pd.concat([
            st.session_state.feedback_data,
            pd.DataFrame([new_entry])
        ], ignore_index=True)
        st.success("✅ Feedback added! Scroll down to view.")

# ---- Show Dashboard & Export only if data exists ----
if not st.session_state.feedback_data.empty:
    st.header("📊 Feedback Dashboard")

    data = st.session_state.feedback_data.copy()

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Feedback Type Distribution")
        pie_data = data["Feedback Type"].value_counts()
        fig1, ax1 = plt.subplots()
        ax1.pie(pie_data, labels=pie_data.index, autopct="%1.1f%%", startangle=90)
        ax1.axis("equal")
        st.pyplot(fig1)

    with col2:
        st.subheader("Ratings Count")
        bar_data = data["Rating"].value_counts().sort_index()
        fig2, ax2 = plt.subplots()
        ax2.bar(bar_data.index, bar_data.values)
        ax2.set_xlabel("Rating")
        ax2.set_ylabel("Count")
        st.pyplot(fig2)

    st.subheader("Average Rating Over Time")
    line_data = data.groupby("Date")["Rating"].mean()
    fig3, ax3 = plt.subplots()
    line_data.plot(marker='o', ax=ax3)
    ax3.set_ylabel("Average Rating")
    st.pyplot(fig3)

    st.metric("📋 Total Feedback Entries", len(data))

    # ---- Export Option ----
    st.header("📥 Export Data")
    csv = data.to_csv(index=False)
    st.download_button("Download CSV", csv, "client_feedback.csv", "text/csv")
