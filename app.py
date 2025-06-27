import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import DatabaseManager
from data_generator import DataGenerator

# Initialize database and generate data
db = DatabaseManager()
db.create_tables()

# Clear existing data to ensure no NULL values
db.connect()
db.cursor.execute("DELETE FROM placements")
db.cursor.execute("DELETE FROM soft_skills")
db.cursor.execute("DELETE FROM programming")
db.cursor.execute("DELETE FROM students")
db.conn.commit()

# Populate with fresh data
generator = DataGenerator(100)
db.insert_data('students', generator.generate_students())
db.insert_data('programming', generator.generate_programming())
db.insert_data('soft_skills', generator.generate_soft_skills())
db.insert_data('placements', generator.generate_placements())
db.close()

# Streamlit app
st.title("Placement Eligibility Dashboard")

# Sidebar for eligibility criteria
st.sidebar.header("Eligibility Criteria")
min_problems = st.sidebar.slider("Minimum Problems Solved", 0, 100, 50)
min_soft_skills = st.sidebar.slider("Minimum Soft Skills Score", 0, 100, 75)
min_mock_score = st.sidebar.slider("Minimum Mock Interview Score", 0, 100, 70)
min_assessments = st.sidebar.slider("Minimum Assessments Completed", 0, 20, 5)
min_mini_projects = st.sidebar.slider("Minimum Mini Projects", 0, 5, 1)
batch_filter = st.sidebar.multiselect("Course Batch", ['DS_2023', 'DS_2024', 'DS_2025'], default=['DS_2023', 'DS_2024', 'DS_2025'])

# Query for eligible students
db.connect()
query = '''
    SELECT s.name, s.email, s.course_batch, p.problems_solved, 
           (ss.communication + ss.teamwork + ss.presentation)/3 as avg_soft_skills,
           pl.mock_interview_score,
           pl.company_name,
           pl.placement_package,
           DATE_FORMAT(pl.placement_date, '%Y-%m-%d') as placement_date,
           p.assessments_completed,
           p.mini_projects
    FROM students s
    JOIN programming p ON s.student_id = p.student_id
    JOIN soft_skills ss ON s.student_id = ss.student_id
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE p.problems_solved >= %s 
    AND (ss.communication + ss.teamwork + ss.presentation)/3 >= %s
    AND pl.mock_interview_score >= %s
    AND p.assessments_completed >= %s
    AND p.mini_projects >= %s
'''
params = [min_problems, min_soft_skills, min_mock_score, min_assessments, min_mini_projects]

# Handle the IN clause dynamically
if batch_filter:
    query += ' AND s.course_batch IN ({})'.format(','.join(['%s'] * len(batch_filter)))
    params.extend(batch_filter)
else:
    query += ' AND 1=0'  # No results if no batches selected

# Display eligible students
st.header("Eligible Students")
results = db.execute_query(query, tuple(params))
df = pd.DataFrame(results, columns=['Name', 'Email', 'Batch', 'Problems Solved', 
                                  'Avg Soft Skills', 'Mock Interview Score',
                                  'Company Name', 'Placement Package', 'Placement Date',
                                  'Assessments Completed', 'Mini Projects'])
# Format numeric columns, handling potential None values as a fallback
df['Avg Soft Skills'] = df['Avg Soft Skills'].astype(float)
df['Avg Soft Skills'] = df['Avg Soft Skills'].round(2)
df['Placement Package'] = df['Placement Package'].apply(lambda x: f"${x:,.2f}" if x is not None else 'N/A')
df['Company Name'] = df['Company Name'].fillna('N/A')
df['Placement Date'] = df['Placement Date'].fillna('N/A')
st.dataframe(df)

# Display insights
st.header("Placement Insights")

# Query 1: Average programming performance by batch
st.subheader("1. Average Problems Solved by Batch")
batch_data = db.execute_query("SELECT course_batch, AVG(problems_solved) FROM students s JOIN programming p ON s.student_id = p.student_id GROUP BY course_batch")
batch_df = pd.DataFrame(batch_data, columns=['Batch', 'Avg Problems Solved'])
batch_df['Avg Problems Solved'] = batch_df['Avg Problems Solved'].astype(float)
batch_df['Avg Problems Solved'] = batch_df['Avg Problems Solved'].round(2)
fig = px.bar(batch_df, x='Batch', y='Avg Problems Solved', title="Average Problems Solved by Batch")
st.plotly_chart(fig)

# Query 2: Students ready for placement
st.subheader("2. Students Ready for Placement")
# Fetch all records for DataFrame
top_students_data_all = db.execute_query('''
    SELECT s.name, p.latest_project_score, pl.mock_interview_score
    FROM students s
    JOIN programming p ON s.student_id = p.student_id
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE pl.placement_status = 'Ready'
    ORDER BY p.latest_project_score DESC, pl.mock_interview_score DESC
''')
top_students_df_all = pd.DataFrame(top_students_data_all, columns=['Name', 'Latest Project Score', 'Mock Interview Score'])
# Fetch top 5 for visualization
top_students_data_top5 = db.execute_query('''
    SELECT s.name, p.latest_project_score, pl.mock_interview_score
    FROM students s
    JOIN programming p ON s.student_id = p.student_id
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE pl.placement_status = 'Ready'
    ORDER BY p.latest_project_score DESC, pl.mock_interview_score DESC
    LIMIT 5
''')
top_students_df_top5 = pd.DataFrame(top_students_data_top5, columns=['Name', 'Latest Project Score', 'Mock Interview Score'])
# Visualization: Grouped bar chart for top 5
fig = go.Figure(data=[
    go.Bar(name='Latest Project Score', x=top_students_df_top5['Name'], y=top_students_df_top5['Latest Project Score']),
    go.Bar(name='Mock Interview Score', x=top_students_df_top5['Name'], y=top_students_df_top5['Mock Interview Score'])
])
fig.update_layout(barmode='group', title="Top 5 Students Ready for Placement", xaxis_title="Student Name", yaxis_title="Score")
st.plotly_chart(fig)
# DataFrame: All records
st.dataframe(top_students_df_all)

# Query 3: Soft skills distribution
st.subheader("3. Communication Skills Distribution")
skills_data = db.execute_query('''
    SELECT CASE 
        WHEN communication >= 90 THEN '90-100'
        WHEN communication >= 80 THEN '80-89'
        WHEN communication >= 70 THEN '70-79'
        ELSE 'Below 70'
    END as score_range, COUNT(*) as count
    FROM soft_skills
    GROUP BY score_range
''')
skills_df = pd.DataFrame(skills_data, columns=['Score Range', 'Count'])
fig = px.pie(skills_df, names='Score Range', values='Count', title="Communication Skills Distribution")
st.plotly_chart(fig)

# Query 4: Students with multiple internships
st.subheader("4. Students with Multiple Internships")
# Fetch all records for DataFrame
internships_data_all = db.execute_query('''
    SELECT s.name, pl.internships_completed
    FROM students s
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE pl.internships_completed > 1
    ORDER BY pl.internships_completed DESC
''')
internships_df_all = pd.DataFrame(internships_data_all, columns=['Name', 'Internships Completed'])
# Fetch top 5 for visualization
internships_data_top5 = db.execute_query('''
    SELECT s.name, pl.internships_completed
    FROM students s
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE pl.internships_completed > 1
    ORDER BY pl.internships_completed DESC
    LIMIT 5
''')
internships_df_top5 = pd.DataFrame(internships_data_top5, columns=['Name', 'Internships Completed'])
# Visualization: Bar chart for top 5
fig = px.bar(internships_df_top5, x='Name', y='Internships Completed', title="Top 5 Students with Multiple Internships")
st.plotly_chart(fig)
# DataFrame: All records
st.dataframe(internships_df_all)

# Query 5: Average placement package by city
st.subheader("5. Average Placement Package by City")
package_data = db.execute_query('''
    SELECT s.city, AVG(pl.placement_package) as avg_package
    FROM students s
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE pl.placement_status = 'Placed'
    GROUP BY s.city
''')
package_df = pd.DataFrame(package_data, columns=['City', 'Average Package'])
package_df['Average Package'] = package_df['Average Package'].apply(lambda x: f"${x:,.2f}")
fig = px.bar(package_df, x='City', y='Average Package', title="Average Placement Package by City")
st.plotly_chart(fig)

# Query 6: Students with high soft skills scores
st.subheader("6. Students with High Soft Skills Scores")
# Fetch all records for DataFrame
high_soft_skills_data_all = db.execute_query('''
    SELECT s.name, AVG(ss.communication + ss.teamwork + ss.presentation) as avg_soft_skills
    FROM students s
    JOIN soft_skills ss ON s.student_id = ss.student_id
    GROUP BY s.student_id, s.name
    HAVING avg_soft_skills > 85
    ORDER BY avg_soft_skills DESC
''')
high_soft_skills_df_all = pd.DataFrame(high_soft_skills_data_all, columns=['Name', 'Avg Soft Skills'])
high_soft_skills_df_all['Avg Soft Skills'] = high_soft_skills_df_all['Avg Soft Skills'].astype(float)
high_soft_skills_df_all['Avg Soft Skills'] = high_soft_skills_df_all['Avg Soft Skills'].round(2)
# Fetch top 5 for visualization
high_soft_skills_data_top5 = db.execute_query('''
    SELECT s.name, AVG(ss.communication + ss.teamwork + ss.presentation) as avg_soft_skills
    FROM students s
    JOIN soft_skills ss ON s.student_id = ss.student_id
    GROUP BY s.student_id, s.name
    HAVING avg_soft_skills > 85
    ORDER BY avg_soft_skills DESC
    LIMIT 5
''')
high_soft_skills_df_top5 = pd.DataFrame(high_soft_skills_data_top5, columns=['Name', 'Avg Soft Skills'])
high_soft_skills_df_top5['Avg Soft Skills'] = high_soft_skills_df_top5['Avg Soft Skills'].astype(float)
high_soft_skills_df_top5['Avg Soft Skills'] = high_soft_skills_df_top5['Avg Soft Skills'].round(2)
# Visualization: Bar chart for top 5
fig = px.bar(high_soft_skills_df_top5, x='Name', y='Avg Soft Skills', title="Top 5 Students with High Soft Skills Scores")
st.plotly_chart(fig)
# DataFrame: All records
st.dataframe(high_soft_skills_df_all)

# Query 7: Programming language preference
st.subheader("7. Programming Language Preference")
language_data = db.execute_query('''
    SELECT p.language, COUNT(*) as student_count
    FROM programming p
    GROUP BY p.language
''')
language_df = pd.DataFrame(language_data, columns=['Language', 'Student Count'])
fig = px.bar(language_df, x='Language', y='Student Count', title="Programming Language Preference")
st.plotly_chart(fig)

# Query 8: Placement success rate by batch
st.subheader("8. Placement Success Rate by Batch")
success_rate_data = db.execute_query('''
    SELECT s.course_batch, 
           COUNT(CASE WHEN pl.placement_status = 'Placed' THEN 1 END) * 100.0 / COUNT(*) as success_rate
    FROM students s
    JOIN placements pl ON s.student_id = pl.student_id
    GROUP BY s.course_batch
''')
success_rate_df = pd.DataFrame(success_rate_data, columns=['Batch', 'Success Rate'])
success_rate_df['Success Rate'] = success_rate_df['Success Rate'].astype(float)
success_rate_df['Success Rate'] = success_rate_df['Success Rate'].round(2)
fig = px.bar(success_rate_df, x='Batch', y='Success Rate', title="Placement Success Rate by Batch")
st.plotly_chart(fig)

# Query 9: Students with certifications
st.subheader("9. Students with Certifications")
# Fetch all records for DataFrame
certifications_data_all = db.execute_query('''
    SELECT s.name, p.certifications_earned
    FROM students s
    JOIN programming p ON s.student_id = p.student_id
    WHERE p.certifications_earned > 0
    ORDER BY p.certifications_earned DESC
''')
certifications_df_all = pd.DataFrame(certifications_data_all, columns=['Name', 'Certifications Earned'])
# Fetch top 5 for visualization
certifications_data_top5 = db.execute_query('''
    SELECT s.name, p.certifications_earned
    FROM students s
    JOIN programming p ON s.student_id = p.student_id
    WHERE p.certifications_earned > 0
    ORDER BY p.certifications_earned DESC
    LIMIT 5
''')
certifications_df_top5 = pd.DataFrame(certifications_data_top5, columns=['Name', 'Certifications Earned'])
# Visualization: Bar chart for top 5
fig = px.bar(certifications_df_top5, x='Name', y='Certifications Earned', title="Top 5 Students with Certifications")
st.plotly_chart(fig)
# DataFrame: All records
st.dataframe(certifications_df_all)

# Query 10: Recent placements
st.subheader("10. Recent Placements by Company")
recent_placements_data = db.execute_query('''
    SELECT pl.company_name, COUNT(*) as placement_count
    FROM students s
    JOIN placements pl ON s.student_id = pl.student_id
    WHERE pl.placement_status = 'Placed'
    GROUP BY pl.company_name
    ORDER BY MAX(pl.placement_date) DESC
    LIMIT 10
''')
recent_placements_df = pd.DataFrame(recent_placements_data, columns=['Company Name', 'Placement Count'])
fig = px.bar(recent_placements_df, x='Company Name', y='Placement Count', title="Recent Placements by Company")
st.plotly_chart(fig)

db.close()