import streamlit as st
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
        "date": str(date),
        "learning": learning,
        "challenge": challenge,
        "goal": goal
    })
    st.success("Progress saved!")

# Show Progress Data
if st.session_state.progress_data:
    st.subheader("📊 Progress Summary")
    for entry in st.session_state.progress_data:
        st.write(f"📅 **{entry['date']}**")
        st.write(f"✅ **Learned:** {entry['learning']}")
        st.write(f"⚠️ **Challenge:** {entry['challenge']}")
        st.write(f"🎯 **Next Goal:** {entry['goal']}")
        st.write("---")

    # Generate PDF Report
    if st.button("📄 Generate PDF Report"):
        pdf_path = f"{name}_progress_report.pdf"
        c = canvas.Canvas(pdf_path, pagesize=letter)
        c.drawString(100, 750, f"Student Progress Report - {name}")
        c.drawString(100, 730, f"Grade: {grade}")
        c.drawString(100, 710, f"Subject: {subject}")

        y = 690
        for entry in st.session_state.progress_data:
            c.drawString(100, y, f"{entry['date']}:")
            c.drawString(120, y - 20, f"Learned: {entry['learning']}")
            c.drawString(120, y - 40, f"Challenge: {entry['challenge']}")
            c.drawString(120, y - 60, f"Goal: {entry['goal']}")
            y -= 100  # Move down for next entry
        
        c.save()
        st.success(f"PDF Report Saved: {pdf_path}")
        st.download_button("📥 Download Report", open(pdf_path, "rb"), file_name=pdf_path)
