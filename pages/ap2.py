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
    highest_marks_in_class = df['score'].max()
    
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
