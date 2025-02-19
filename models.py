import random
from datetime import date, timedelta
from collections import defaultdict

from faker import Faker

fake = Faker()

class Student:
    def __init__(self, name: str, amount_of_lessons_per_week: int):
        self.name = name
        self.amount_of_lessons_per_week = amount_of_lessons_per_week

    def __repr__(self):
        return f"Student(name={self.name}, lessons per week={self.amount_of_lessons_per_week})"


class Teacher:
    def __init__(self, name: str, amount_of_work_hours_per_week: int):
        self.name = name
        self.amount_of_work_hours_per_week = amount_of_work_hours_per_week

    def __repr__(self):
        return f"Teacher(name={self.name}, work hours per week={self.amount_of_work_hours_per_week})"


class Lesson:
    def __init__(self, teacher: Teacher, student: Student, time: date):
        self.teacher = teacher
        self.student = student
        self.time = time

    def __repr__(self):
        return f"Lesson(teacher={self.teacher.name}, student={self.student.name}, time={self.time})"


def generate_random_data(num_students=7, num_teachers=4, num_lessons=20):
    students = [Student(fake.first_name(), random.randint(1, 7)) for _ in range(num_students)]
    teachers = [Teacher(fake.first_name(), random.randint(20, 40)) for _ in range(num_teachers)]

    lessons = []
    teacher_availability = defaultdict(list)
    student_lessons = defaultdict(list)

    for _ in range(num_lessons):
        teacher = random.choice(teachers)
        student = random.choice(students)
        while True:
            lesson_date = date.today() + timedelta(days=random.randint(1, 7))
            if lesson_date not in student_lessons[student.name]:
                break
        lesson_date = date.today() + timedelta(days=random.randint(1, 7))

        lessons.append(Lesson(teacher, student, lesson_date))
        teacher_availability[lesson_date].append(teacher.name)

    print(teacher_availability)
    return students, teachers, lessons, teacher_availability



