from faker import Faker
import random
from typing import List, Tuple
from datetime import datetime, timedelta

class DataGenerator:
    def __init__(self, num_records: int = 100):
        self.fake = Faker()
        self.num_records = num_records
        self.batches = ['DS_2023', 'DS_2024', 'DS_2025']
        self.languages = ['Python', 'SQL', 'Java']
        self.cities = ['New York', 'San Francisco', 'Boston', 'Chicago', 'Seattle']
        self.companies = ['Google', 'Amazon', 'Microsoft', 'Infosys', 'TCS', 'Wipro', 'Accenture', 'Deloitte', 'Capgemini', 'OtherTech']

    def generate_students(self) -> List[Tuple]:
        """Generate student data"""
        students = []
        for i in range(1, self.num_records + 1):
            students.append((
                i,
                self.fake.name(),
                random.randint(18, 25),
                random.choice(['Male', 'Female', 'Other']),
                self.fake.unique.email(),
                self.fake.phone_number(),
                random.randint(2021, 2024),
                random.choice(self.batches),
                random.choice(self.cities),
                random.randint(2023, 2026)
            ))
        return students

    def generate_programming(self) -> List[Tuple]:
        """Generate programming performance data"""
        programming = []
        for i in range(1, self.num_records + 1):
            programming.append((
                i,
                i,  # student_id
                random.choice(self.languages),
                random.randint(10, 100),
                random.randint(5, 20),
                random.randint(1, 5),
                random.randint(0, 3),
                random.randint(60, 100)
            ))
        return programming

    def generate_soft_skills(self) -> List[Tuple]:
        """Generate soft skills data"""
        soft_skills = []
        for i in range(1, self.num_records + 1):
            soft_skills.append((
                i,
                i,  # student_id
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100),
                random.randint(50, 100)
            ))
        return soft_skills

    def generate_placements(self) -> List[Tuple]:
        """Generate placement data with non-NULL values for all columns"""
        placements = []
        for i in range(1, self.num_records + 1):
            status = random.choice(['Ready', 'Not Ready', 'Placed'])
            company = random.choice(self.companies)
            package = random.uniform(30000, 80000)  # Salary between 30k and 80k
            date = self.fake.date_between(start_date=datetime(2024, 1, 1), end_date=datetime(2025, 6, 25))
            rounds = random.randint(1, 4) if status == 'Placed' else random.randint(0, 2)
            
            placements.append((
                i,
                i,  # student_id
                random.randint(50, 100),
                random.randint(0, 3),
                status,
                company,
                package,
                rounds,
                date
            ))
        return placements