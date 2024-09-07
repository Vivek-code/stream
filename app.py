import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Example: Data frame for tracking student performance
data = pd.DataFrame({
    'Student': ['John', 'Emma', 'Sophia'],
    'Score': [85, 40, 70],
    'Struggles_with': ['Math', 'Science', 'Math']
})

# Personalized learning path decision tree
def recommend_resources(score, struggle_area):
    if score < 50:
        return f"Provide basic resources in {struggle_area}."
    elif score < 70:
        return f"Provide intermediate resources in {struggle_area}."
    else:
        return "Provide advanced resources."

# Streamlit UI
st.set_page_config(page_title="Learning Path Recommendations", layout="wide")

st.title('🎓 Personalized Learning Path Recommendations')

# Sidebar for adding new student data
st.sidebar.header('📚 Add New Student Performance Data')
student_name = st.sidebar.text_input("Student Name", "")
score = st.sidebar.number_input("Score", min_value=0, max_value=100, value=50)
struggle_area = st.sidebar.selectbox("Struggles with", ["Math", "Science", "English", "History"])

if st.sidebar.button("Add Student"):
    if student_name:
        new_data = pd.DataFrame({
            'Student': [student_name],
            'Score': [score],
            'Struggles_with': [struggle_area]
        })
        data = pd.concat([data, new_data], ignore_index=True)
        st.sidebar.success(f"Added data for {student_name}.")

# Apply recommendations
data['Recommendation'] = data.apply(lambda x: recommend_resources(x['Score'], x['Struggles_with']), axis=1)

# Display data and recommendations
st.subheader('📊 Student Performance Data')
st.dataframe(data.style.applymap(lambda x: 'background-color: #d3f8e2' if x == 'Provide advanced resources.' else '', subset=['Recommendation']))

st.subheader('🔍 Recommendations')
for _, row in data.iterrows():
    st.write(f"**Student:** {row['Student']}  \n**Recommendation:** {row['Recommendation']}")

# Create a bar chart for scores
st.subheader('📈 Score Distribution')
fig, ax = plt.subplots()
sns.barplot(x='Student', y='Score', data=data, ax=ax, palette='viridis')
ax.set_title('Score Distribution by Student')
ax.set_xlabel('Student')
ax.set_ylabel('Score')
st.pyplot(fig)

# Create a pie chart for struggle areas
st.subheader('🍰 Struggle Areas Distribution')
fig, ax = plt.subplots()
struggle_counts = data['Struggles_with'].value_counts()
ax.pie(struggle_counts, labels=struggle_counts.index, autopct='%1.1f%%', startangle=140, colors=sns.color_palette('pastel'))
ax.set_title('Distribution of Struggle Areas')
st.pyplot(fig)
