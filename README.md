# Placement Eligibility Dashboard

A **Streamlit** web application for dynamically filtering and shortlisting students based on customizable placement eligibility criteria. This interactive dashboard supports placement teams and EdTech platforms with real-time analytics, student insights, and decision-making tools.

---

##  Features

### Eligibility Filtering
Set minimum thresholds for:
- Problems Solved (0–100)
- Average Soft Skills Score (0–100)
- Mock Interview Score (0–100)
- Assessments Completed (0–20)
- Mini Projects Completed (0–5)
- Course Batch (Multi-select: `DS_2023`, `DS_2024`, `DS_2025`)

### Eligible Students Table
Shows:
- Name, Email, Course Batch, City
- Problems Solved, Soft Skills Average
- Mock Interview Score, Company Name
- Placement Package, Placement Date
- Assessments Completed, Mini Projects

### Placement Insights
10 detailed visualizations and data summaries:
1. **Avg. Problems Solved by Batch** *(Bar Chart)*
2. **Students Ready for Placement** *(Grouped Bar Chart + Table)*
3. **Communication Skills Distribution** *(Pie Chart)*
4. **Multiple Internships** *(Bar Chart + Table)*
5. **Avg. Placement Package by City** *(Bar Chart)*
6. **High Soft Skills Scorers (>85)** *(Bar Chart + Table)*
7. **Programming Language Preference** *(Bar Chart)*
8. **Placement Success Rate by Batch** *(Bar Chart)*
9. **Certified Students** *(Bar Chart + Table)*
10. **Recent Placements by Company** *(Bar Chart)*


## Tech Stack

- **Frontend:** Streamlit + Plotly
- **Backend:** Python, MySQL
- **Data:** Synthetic data (generated fresh on each run)


## Setup Instructions

### 1. Clone the Repository
- git clone [<repository-url>](https://github.com/VasuGadde0203/Placement-Eligibility-App.git)
- cd placement_eligibility_project

### 2.  Install Dependencies
- pip install -r requirements.txt

### 3. Configure MySQL
- Ensure your MySQL server is running.
- Create a new database:
    - CREATE DATABASE placement_db;
- Create a .env file in the root directory:
    - DB_HOST=localhost
    - DB_USER=your_username
    - DB_PASSWORD=your_password
    - DB_NAME=placement_db
Replace your_username and your_password accordingly.

### 4. Run the Application
- streamlit run app.py
Then visit http://localhost:8501 in your browser.

## Usage
-  Set Eligibility Criteria
    - Use the sidebar to filter students. The eligible table updates in real time.

- Explore Placement Insights
    - Scroll down to "Placement Insights" to view 10 visualizations, some with top 5 bar charts + full data tables.

## Usage

### Set Eligibility Criteria
- Use the sidebar to filter students. The eligible table updates in real time.

### Explore Placement Insights
- Scroll down to "Placement Insights" to view 10 visualizations, some with top 5 bar charts + full data tables.

## File Structure
placement_eligibility_project/
│
├── app.py                 # Main Streamlit app
├── database.py            # DB connection, table creation, insertion
├── data_generator.py      # Synthetic data generator
├── queries.sql            # SQL query templates
├── .env                   # DB credentials (not committed)
├── requirements.txt       # Dependencies
└── README.md              # You're reading it!

## Database Schema
- **students**
    - student_id (PK), name, email, course_batch, city

- **programming**
    - student_id (FK), language, problems_solved, latest_project_score, certifications_earned, assessments_completed, mini_projects

- **soft_skills**
    - student_id (FK), communication, teamwork, presentation

- **placements**
    - student_id (FK), placement_status, mock_interview_score, internships_completed, company_name, placement_package, placement_date

## Troubleshooting
- **MySQL Connection Errors:**
    - Confirm .env values and DB is running.

- **No Eligible Students Displayed:**
    - Try relaxing the slider filters or selecting valid course batches.

- **Check for NULL values:**
    - Run:
        - SELECT * FROM placements 
        - WHERE company_name IS NULL OR placement_package IS NULL OR placement_date IS NULL;

- **Debugging Queries in Code:**
    - Add:
        - print("Query results (first 5):", results[:5])

## Future Enhancements
- Add filters for city or placement status
- Persist student data between runs
- Export eligibility results as CSV
- Add more visualization types (scatter plots, heatmaps, etc.)

## Contact
- For feature requests, contributions, or issues, please open an issue or contact me.
- **Name:** Vasu Gadde
- **Mob No:** +91 8793307218
- **Email:** vasugadde0203@gmail.com

## License
- This project is licensed under the MIT License. See LICENSE for more details.
    - Let me know if you want this customized with your name, repo link, or want badges (like Python version, license, etc.) added at the top.
