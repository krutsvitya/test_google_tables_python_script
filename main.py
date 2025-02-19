from collections import defaultdict

import gspread
from oauth2client.service_account import ServiceAccountCredentials

from models import generate_random_data

scope = ["https://www.googleapis.com/auth/spreadsheets"]
creds = ServiceAccountCredentials.from_json_keyfile_name("possible-willow-445315-a8-6a107575a5e9.json", scope)
client = gspread.authorize(creds)

spreadsheet = client.open_by_key("15ai333vnsMIkvPaS90vsqBayQ7iL6XIvJyOi18wOrJY")

worksheet = spreadsheet.sheet1

students, teachers, lessons, teacher_availability = generate_random_data()
print(teachers)
lesson_groups = defaultdict(list)

for lesson in lessons:
    key = (lesson.teacher.name, lesson.time)
    lesson_groups[key].append(lesson)

headers = worksheet.row_values(1)
for key, group in lesson_groups.items():
    if len(group) > 1:
        print(f"Викладач {key[0]} проводить декілька зайнять у {key[1]}:")

        schedule_conflict = {
            "Teacher": key[0],
            "Date": key[1].strftime('%Y-%m-%d'),
        }
        for teacher in teachers:
            if teacher.name not in teacher_availability[key[1]]:
                schedule_conflict["New teacher"] = teacher.name
                teacher_availability[key[1]].append(teacher.name)
            else:
                schedule_conflict["New teacher"] = 'Немає заміни'

        for i, lesson in enumerate(group):
            schedule_conflict[f"Student{i+1}"] = lesson.student.name
            print(f"  - {lesson}")

        row_data = []
        for header in headers:
            row_data.append(schedule_conflict.get(header, ""))

        data = worksheet.append_row(row_data)

print(data)
