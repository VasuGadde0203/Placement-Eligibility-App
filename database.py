import mysql.connector
from typing import List, Tuple
from dotenv import load_dotenv
import os

class DatabaseManager:
    def __init__(self):
        load_dotenv()
        self.config = {
            'host': os.getenv('DB_HOST', 'localhost'),
            'user': os.getenv('DB_USER', 'root'),
            'password': os.getenv('DB_PASSWORD', ''),
            'database': os.getenv('DB_NAME', 'placement_db')
        }
        self.conn = None
        self.cursor = None

    def connect(self):
        """Establish database connection"""
        self.conn = mysql.connector.connect(**self.config)
        self.cursor = self.conn.cursor()

    def create_tables(self):
        """Create all required tables with relationships"""
        self.connect()
        
        # Students Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS students (
                student_id INT PRIMARY KEY AUTO_INCREMENT,
                name VARCHAR(255) NOT NULL,
                age INT,
                gender VARCHAR(10),
                email VARCHAR(255) UNIQUE,
                phone VARCHAR(20),
                enrollment_year INT,
                course_batch VARCHAR(50),
                city VARCHAR(100),
                graduation_year INT
            )
        ''')

        # Programming Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS programming (
                programming_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                language VARCHAR(50),
                problems_solved INT,
                assessments_completed INT,
                mini_projects INT,
                certifications_earned INT,
                latest_project_score INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')

        # Soft Skills Table
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS soft_skills (
                soft_skill_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                communication INT,
                teamwork INT,
                presentation INT,
                leadership INT,
                critical_thinking INT,
                interpersonal_skills INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')

        # Placements Table 
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS placements (
                placement_id INT PRIMARY KEY AUTO_INCREMENT,
                student_id INT,
                mock_interview_score INT,
                internships_completed INT,
                placement_status VARCHAR(50),
                company_name VARCHAR(100) NOT NULL,
                placement_package FLOAT NOT NULL,
                placement_date DATE NOT NULL,
                interview_rounds_cleared INT,
                FOREIGN KEY (student_id) REFERENCES students(student_id)
            )
        ''')
        
        self.conn.commit()

    def insert_data(self, table: str, data: List[Tuple]):
        """Insert data into specified table"""
        if table == 'students':
            self.cursor.executemany('''
                INSERT IGNORE INTO students 
                (student_id, name, age, gender, email, phone, enrollment_year, course_batch, city, graduation_year)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', data)
        elif table == 'programming':
            self.cursor.executemany('''
                INSERT INTO programming 
                (programming_id, student_id, language, problems_solved, assessments_completed, 
                 mini_projects, certifications_earned, latest_project_score)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', data)
        elif table == 'soft_skills':
            self.cursor.executemany('''
                INSERT INTO soft_skills 
                (soft_skill_id, student_id, communication, teamwork, presentation, 
                 leadership, critical_thinking, interpersonal_skills)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            ''', data)
        elif table == 'placements':
            self.cursor.executemany('''
                INSERT INTO placements 
                (placement_id, student_id, mock_interview_score, internships_completed, 
                 placement_status, company_name, placement_package, interview_rounds_cleared, placement_date)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            ''', data)
        
        self.conn.commit()

    def execute_query(self, query: str, params: tuple = ()) -> List[Tuple]:
        """Execute SQL query and return results"""
        self.cursor.execute(query, params)
        return self.cursor.fetchall()

    def close(self):
        """Close database connection"""
        if self.conn:
            self.cursor.close()
            self.conn.close()