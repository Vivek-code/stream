import streamlit as st
import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph
from reportlab.lib import colors
from reportlab.lib.units import inch  # Ensure this import is included
from reportlab.lib.styles import getSampleStyleSheet

# Sample data
data = {
    'student_id': ['student_01', 'student_01', 'student_02', 'student_03', 'student_01', 'student_02', 'student_03', 'student_01', 'student_02', 'student_03',
                   'student_01', 'student_01', 'student_02', 'student_03', 'student_01', 'student_02', 'student_03', 'student_01', 'student_02', 'student_03'],
    'student_name': ['Alice', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie',
                     'Alice', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie', 'Alice', 'Bob', 'Charlie'],
    'activity': ['quiz', 'poll', 'test', 'quiz', 'test', 'poll', 'quiz', 'test', 'poll', 'quiz',
                 'quiz', 'test', 'poll', 'quiz', 'poll', 'test', 'quiz', 'poll', 'test', 'quiz'],
    'subject': ['Math', 'Math', 'Science', 'Math', 'Science', 'Science', 'Math', 'History', 'History', 'History',
                'English', 'Math', 'Science', 'History', 'English', 'Math', 'Science', 'History', 'English', 'Math'],
    'score': [85, 90, 78, 92, 88, 75, 84, 91, 77, 89,
              82, 79, 88, 85, 87, 78, 90, 84, 92, 80],
    'timestamp': [
        datetime.datetime(2024, 8, 15), datetime.datetime(2024, 8, 16), datetime.datetime(2024, 8, 17), datetime.datetime(2024, 8, 20), datetime.datetime(2024, 8, 25),
        datetime.datetime(2024, 8, 28), datetime.datetime(2024, 9, 1), datetime.datetime(2024, 9, 5), datetime.datetime(2024, 9, 10), datetime.datetime(2024, 9, 12),
        datetime.datetime(2024, 9, 15), datetime.datetime(2024, 9, 18), datetime.datetime(2024, 9, 20), datetime.datetime(2024, 9, 22), datetime.datetime(2024, 9, 25),
        datetime.datetime(2024, 9, 30), datetime.datetime(2024, 10, 5), datetime.datetime(2024, 10, 10), datetime.datetime(2024, 10, 15), datetime.datetime(2024, 10, 20)
    ]
}

df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="Student Progress Tracker", layout="wide")

st.title("Student Progress Tracker 📈")

# Select student
students = df['student_name'].unique()
selected_student = st.sidebar.selectbox("Select Student", students)

# Filtering data for selected student
student_data = df[df['student_name'] == selected_student]

# Define a function to plot histograms
def plot_histogram(student_data):
    if student_data.empty:
        st.write("No data available for the selected student.")
        return

    # Plotting histogram with subjects on x-axis and marks on y-axis
    plt.figure(figsize=(12, 6))
    ax = sns.histplot(data=student_data, x='subject', hue='score', multiple='stack', palette='viridis', binwidth=1, kde=False)
    
    ax.set_title(f"Score Distribution for {selected_student}", fontsize=16, fontweight='bold', color='darkblue')
    ax.set_xlabel("Subject", fontsize=12, fontweight='bold')
    ax.set_ylabel("Marks", fontsize=12, fontweight='bold')
    plt.xticks(rotation=45, fontsize=10)
    plt.yticks(fontsize=10)
    plt.grid(True, linestyle='--', alpha=0.7)
    st.pyplot(plt.gcf())

# Display progress reports
st.subheader(f"Score Distribution for {selected_student}")
plot_histogram(student_data)

# Display activity summaries
st.subheader("Activity Summary")

# Group by activity type and show average scores
activity_summary = student_data.groupby('activity').agg({'score': ['mean', 'count']}).reset_index()
activity_summary.columns = ['activity', 'average_score', 'total_count']

# Display activity summary with colors
st.markdown("""
    <style>
    .activity-summary {
        display: flex;
        flex-direction: column;
        align-items: center;
    }
    .activity-card {
        background-color: #f8f9fa;
        padding: 15px;
        margin: 10px;
        border-radius: 10px;
        width: 80%;
        box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
    }
    .activity-card h4 {
        margin: 0;
        color: #343a40;
    }
    .activity-card p {
        margin: 5px 0;
    }
    </style>
""", unsafe_allow_html=True)

for _, row in activity_summary.iterrows():
    st.markdown(f"""
        <div class="activity-card">
            <h4>{row['activity'].capitalize()}</h4>
            <p><strong>Average Score:</strong> {row['average_score']:.2f}</p>
            <p><strong>Total Activities:</strong> {row['total_count']}</p>
        </div>
    """, unsafe_allow_html=True)

# Display overall statistics
st.subheader(f"Overall Statistics for {selected_student}")

mean_score = student_data['score'].mean()
max_score = student_data['score'].max()
min_score = student_data['score'].min()
total_activities = student_data['activity'].count()

# Passing percentage and pass/fail status
passing_percentage = 60
status = "Passed" if mean_score >= passing_percentage else "Failed"

st.markdown(f"""
    <div style="background-color: #e9ecef; padding: 20px; border-radius: 10px; text-align: center;">
        <h2 style="color: #343a40;">{selected_student}'s Report Card</h2>
        <p style="font-size: 18px; color: #28a745;"><strong>Average Score:</strong> {mean_score:.2f}</p>
        <p style="font-size: 18px; color: #dc3545;"><strong>Maximum Score:</strong> {max_score}</p>
        <p style="font-size: 18px; color: #ffc107;"><strong>Minimum Score:</strong> {min_score}</p>
        <p style="font-size: 18px; color: #007bff;"><strong>Total Activities:</strong> {total_activities}</p>
        <p style="font-size: 18px; color: #ff5733;"><strong>Status:</strong> {status}</p>
    </div>
""", unsafe_allow_html=True)

# Display individual quiz/test/poll marks
st.subheader("Individual Activity Marks")

if not student_data.empty:
    st.dataframe(student_data[['subject', 'activity', 'score', 'timestamp']])

# Calculate class ranking
class_avg_scores = df.groupby('student_name')['score'].mean().reset_index()
class_avg_scores.columns = ['student_name', 'average_score']
class_avg_scores = class_avg_scores.sort_values(by='average_score', ascending=False).reset_index(drop=True)
class_avg_scores['rank'] = class_avg_scores.index + 1

# Display topper
st.subheader("Topper")

topper = class_avg_scores.iloc[0]

st.markdown(f"""
    <div style="background-color: #e9ecef; padding: 15px; border-radius: 10px; text-align: center;">
        <h3 style="color: #343a40;">Topper in the Class</h3>
        <p style="font-size: 16px; color: #007bff;"><strong>Name:</strong> {topper['student_name']}</p>
        <p style="font-size: 16px; color: #28a745;"><strong>Average Score:</strong> {topper['average_score']:.2f}</p>
    </div>
""", unsafe_allow_html=True)

# Function to generate PDF report card
def generate_pdf(df, selected_student):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=72)
    elements = []

    # Styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    normal_style = styles['Normal']

    # Title
    title = Paragraph(f"Comprehensive Report Card for {selected_student}", title_style)
    elements.append(title)
    elements.append(Paragraph("<br/>", normal_style))

    # Overall Statistics Table
    student_data = df[df['student_name'] == selected_student]
    mean_score = student_data['score'].mean()
    max_score = student_data['score'].max()
    min_score = student_data['score'].min()
    total_activities = student_data['activity'].count()

    stats_data = [
        ["Metric", "Value"],
        ["Average Score", f"{mean_score:.2f}"],
        ["Maximum Score", str(max_score)],
        ["Minimum Score", str(min_score)],
        ["Total Activities", str(total_activities)]
    ]
    
    stats_table = Table(stats_data, colWidths=[3*inch, 2*inch])
    stats_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(stats_table)
    elements.append(Paragraph("<br/>", normal_style))  # Added space

    # Individual Activity Marks Table
    activity_data = [["Subject", "Activity", "Score", "Date"]]
    for _, row in student_data.iterrows():
        activity_data.append([
            row['subject'],
            row['activity'].capitalize(),
            str(row['score']),
            row['timestamp'].strftime('%Y-%m-%d')
        ])
    
    activity_table = Table(activity_data, colWidths=[1.5*inch, 1.5*inch, 1*inch, 1.5*inch])
    activity_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(activity_table)
    elements.append(Paragraph("<br/>", normal_style))  # Added space

    # Highest Marks Achieved by the Selected Student
    highest_marks = student_data['score'].max()
    
    comment = ""
    if mean_score >= 80:
        comment = "Excellent work! Keep up the great performance."
    elif mean_score >= 60:
        comment = "Good job! There is room for improvement."
    else:
        comment = "Needs improvement. Consider revising the material more thoroughly."
    
    elements.append(Paragraph(f"Highest Marks Achieved by {selected_student}: {highest_marks}", normal_style))
    elements.append(Paragraph("<br/>", normal_style))  # Added space
    elements.append(Paragraph(f"Comments: {comment}", normal_style))
    elements.append(Paragraph("<br/>", normal_style))  # Added space

    # Build the PDF
    doc.build(elements)
    buffer.seek(0)
    return buffer

# Button to download the PDF
if st.button("Download Comprehensive Report Card as PDF"):
    pdf_buffer = generate_pdf(df, selected_student)
    st.download_button(label="Download PDF", data=pdf_buffer, file_name=f"{selected_student}_Comprehensive_Report_Card.pdf", mime="application/pdf")
