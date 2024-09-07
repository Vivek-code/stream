import streamlit as st
import pandas as pd
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet

# Initialize session state if not already done
if 'questions' not in st.session_state:
    st.session_state.questions = []
if 'polling' not in st.session_state:
    st.session_state.polling = []

# Function to provide feedback with visual enhancements
def provide_feedback(correct_answer, student_answer):
    if student_answer == correct_answer:
        feedback = "Correct! Great job! 🎉"
        color = "#d4edda"  # Light green background color for correct answers
        icon = "✅"        # Check mark emoji
    else:
        feedback = "Incorrect. Keep trying! 😔"
        color = "#f8d7da"  # Light red background color for incorrect answers
        icon = "❌"        # Cross mark emoji
    return feedback, color, icon

# Function to add a question
def add_question(question, options, correct_answer):
    st.session_state.questions.append({
        "question": question,
        "options": options,
        "correct_answer": correct_answer
    })

# Function to load questions from a CSV file
def load_questions_from_csv(file):
    df = pd.read_csv(file)
    for _, row in df.iterrows():
        question = row['question']
        options = [row[f'option{i}'] for i in range(1, 5) if pd.notna(row[f'option{i}'])]
        correct_answer = row['correct_answer']
        add_question(question, options, correct_answer)
    st.sidebar.success("Questions loaded successfully from CSV!")

# Function to generate PDF report card
def generate_pdf(student_data, selected_student, selected_subject, mean_score, max_score, min_score, total_activities, status):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawString(1*inch, height - 1*inch, f"Report Card for {selected_student}")
    
    # Subject
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 1.5*inch, f"Subject: {selected_subject}")
    
    # Overall Statistics Table
    data = [
        ["Metric", "Value"],
        ["Average Score", f"{mean_score:.2f}"],
        ["Maximum Score", str(max_score)],
        ["Minimum Score", str(min_score)],
        ["Total Activities", str(total_activities)],
        ["Status", status]
    ]
    
    table = Table(data, colWidths=[3*inch, 2*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    table.wrapOn(c, width, height)
    table.drawOn(c, 1*inch, height - 2.2*inch)

    # Individual Activity Marks Table
    activity_data = [["Activity", "Score", "Date", "Subject"]]
    for _, row in student_data.iterrows():
        activity_data.append([
            row['activity'].capitalize(),
            str(row['score']),
            row['timestamp'].strftime('%Y-%m-%d'),
            row['subject']
        ])
    
    activity_table = Table(activity_data, colWidths=[1.5*inch, 1*inch, 1.5*inch, 1.5*inch])
    activity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    activity_table.wrapOn(c, width, height)
    activity_table.drawOn(c, 1*inch, height - 4*inch)
    
    # Highest Marks Achieved by Any Student in the Class
    highest_marks_in_class = student_data['score'].max()
    
    # Comment Section
    styles = getSampleStyleSheet()
    comment = ""
    
    if mean_score >= 80:
        comment = "Excellent work! Keep up the great performance."
    elif mean_score >= 60:
        comment = "Good job! There is room for improvement."
    else:
        comment = "Needs improvement. Consider revising the material more thoroughly."
    
    c.setFont("Helvetica-Bold", 14)
    c.drawString(1*inch, height - 6.5*inch, f"Highest Marks Achieved by Any Student in the Class: {highest_marks_in_class}")
    
    c.setFont("Helvetica-Bold", 12)
    c.drawString(1*inch, height - 7*inch, "Comments:")
    
    c.setFont("Helvetica", 12)
    c.drawString(1*inch, height - 7.5*inch, comment)
    
    # Save PDF
    c.save()
    buffer.seek(0)
    return buffer

# Streamlit UI
st.set_page_config(page_title="Classroom Polling System", layout="centered")

# Title
st.title('Classroom Polling System 📊')

# Sidebar for file upload
st.sidebar.header("Upload Questions CSV")

uploaded_file = st.sidebar.file_uploader("Upload CSV with Questions", type=["csv"])

if uploaded_file is not None:
    load_questions_from_csv(uploaded_file)

# Sidebar for adding new questions
st.sidebar.header("Add a New Question")

# Input fields for new question
question_text = st.sidebar.text_input("Question Text", "")
option1 = st.sidebar.text_input("Option 1", "")
option2 = st.sidebar.text_input("Option 2", "")
option3 = st.sidebar.text_input("Option 3", "")
option4 = st.sidebar.text_input("Option 4", "")
correct_answer = st.sidebar.selectbox("Correct Answer", [option1, option2, option3, option4])

if st.sidebar.button("Add Question"):
    if question_text and any([option1, option2, option3, option4]):
        add_question(question_text, [option1, option2, option3, option4], correct_answer)
        st.sidebar.success("Question added successfully!")
    else:
        st.sidebar.error("Please fill out all fields.")

# File upload section
st.sidebar.header("Upload Files for the Classroom")

uploaded_file = st.sidebar.file_uploader("Upload a file (image, document, etc.)", type=["png", "jpg", "jpeg", "pdf", "docx", "xlsx"])

if uploaded_file is not None:
    if uploaded_file.type.startswith("image"):
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
    elif uploaded_file.type == "application/pdf":
        st.write("PDF file uploaded, but cannot be displayed directly.")
        st.download_button(label="Download PDF", data=uploaded_file, file_name=uploaded_file.name, mime="application/pdf")
    else:
        st.write(f"File '{uploaded_file.name}' uploaded successfully!")

# Polling System
if st.session_state.questions:
    st.header("Current Questions")

    # Display questions and polling options
    for i, q in enumerate(st.session_state.questions):
        st.subheader(f"Q{i + 1}: {q['question']}")
        selected_option = st.radio("Choose an option:", q['options'], key=f"q{i}")

        if st.button(f"Submit Answer for Q{i + 1}"):
            feedback, color, icon = provide_feedback(q['correct_answer'], selected_option)
            
            # Display feedback with color and icon
            st.markdown(f"""
                <div style="background-color: {color}; padding: 10px; border-radius: 5px; text-align: center;">
                    <h3 style="margin: 0;">{icon} {feedback}</h3>
                </div>
            """, unsafe_allow_html=True)

# Display all the added questions and options
if st.session_state.questions:
    st.sidebar.subheader("All Questions")
    for i, q in enumerate(st.session_state.questions):
        st.sidebar.write(f"Q{i + 1}: {q['question']}")
        for opt in q['options']:
            st.sidebar.write(f" - {opt}")
        st.sidebar.write(f"Correct Answer: {q['correct_answer']}")
