import streamlit as st
import pandas as pd
import datetime
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

# Title
st.title("📚 Student Growth Mindset Tracker")

# Sidebar - Student Info
st.sidebar.header("Student Details")
name = st.sidebar.text_input("Enter Student Name:")
grade = st.sidebar.selectbox("Select Grade:", ["Grade 1", "Grade 2", "Grade 3", "Grade 4", "Grade 5"])
subject = st.sidebar.text_input("Enter Subject:")

# Store progress in session state
if "progress_data" not in st.session_state:
    st.session_state.progress_data = []

# Progress Tracking
st.subheader("📅 Daily Progress Tracking")
date = st.date_input("Select Date:")
learning = st.text_area("What did you learn today?")
challenge = st.text_area("What was challenging?")
goal = st.text_area("Your goal for tomorrow?")

# Save Data
if st.button("Save Progress"):
    st.session_state.progress_data.append({
        "Date": date.strftime("%Y-%m-%d"),
        "Learning": learning,
        "Challenge": challenge,
        "Goal": goal
    })
    st.success("Progress saved!")

# Show Progress Data
if st.session_state.progress_data:
    st.subheader("📊 Progress Summary")
    progress_df = pd.DataFrame(st.session_state.progress_data)

    st.dataframe(progress_df)

    # Generate CSV
    csv_data = progress_df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv_data, file_name=f"{name}_progress.csv", mime="text/csv")

    # Generate Excel
    excel_buffer = io.BytesIO()
    with pd.ExcelWriter(excel_buffer, engine="xlsxwriter") as writer:
        progress_df.to_excel(writer, index=False, sheet_name="Progress")
    excel_buffer.seek(0)
    st.download_button("📥 Download Excel", data=excel_buffer, file_name=f"{name}_progress.xlsx", mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    # Generate PDF Report
    if st.button("📄 Generate PDF Report"):
        pdf_buffer = io.BytesIO()
        c = canvas.Canvas(pdf_buffer, pagesize=letter)
        c.drawString(100, 750, f"Student Progress Report - {name}")
        c.drawString(100, 730, f"Grade: {grade}")
        c.drawString(100, 710, f"Subject: {subject}")

        y = 690
        for entry in st.session_state.progress_data:
            c.drawString(100, y, f"{entry['Date']}:")
            c.drawString(120, y - 20, f"Learned: {entry['Learning']}")
            c.drawString(120, y - 40, f"Challenge: {entry['Challenge']}")
            c.drawString(120, y - 60, f"Goal: {entry['Goal']}")
            y -= 100  # Move down for next entry

        c.save()
        pdf_buffer.seek(0)
        st.download_button("📥 Download PDF", data=pdf_buffer, file_name=f"{name}_progress.pdf", mime="application/pdf")
