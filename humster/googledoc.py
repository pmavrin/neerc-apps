import gspread
from humster.models import Semester, Course, Student, State, Score

__author__ = 'Pavel Mavrin'


def login():
    return gspread.login('pavel.mavrin@gmail.com', 'gfhfyjhvfk')


def reload_semester_from_gd(semester, sheet=None):
    if sheet is None:
        gc = login()
        sheet = gc.open(semester.stream.gd_spreadsheet_name).worksheet(semester.gd_sheet_name)
    old_students = dict()
    for student in semester.stream.student_set.all():
        old_students[student.full_name()] = student
    old_courses = dict()
    for course in semester.course_set.all():
        old_courses[course.name] = course

    #load courses
    first_row = sheet.row_values(1)
    second_row = sheet.row_values(2)
    courses = [None] * len(first_row)
    for c in range(2, min(len(first_row), len(second_row))):
        s = first_row[c].strip()
        if len(s) > 0:
            if s in old_courses:
                course = old_courses[s]
            else:
                course = Course(name=s, semester=semester)
            course.update_mode = second_row[c]
            if course.update_mode == "skip":
                course.state = State.DISABLED
            else:
                course.state = State.OK
            course.save()
            courses[c] = course

    #load students
    first_col = sheet.col_values(1)
    second_col = sheet.col_values(2)
    semester.students = []
    for r in range(3, min(len(first_col), len(second_col))):
        s = first_col[r].strip()
        if len(s) > 0:
            s = s.split()
            s.append("")
            s.append("")
            full_name = s[0] + " " + s[1] + " " + s[2]
            if full_name in old_students:
                student = old_students[full_name]
            else:
                student = Student(last_name=s[0], first_name=s[1], father_name=s[2], group=int(second_col[r]),
                                  stream=semester.stream, state=State.OK)
            student.save()
            semester.students.add(student)
            scores = dict()
            for score in student.score_set.all():
                scores[score.course] = score

            for c in range(len(courses)):
                if course is not None:
                    score_val = Score.parse(sheet.cell(r, c).value.strip())

                    if len(s) > 0:
                        if s in old_courses:
                            course = old_courses[s]
                        else:
                            course = Course(name=s, semester=semester)
                        course.update_mode = second_row[c]
                        if course.update_mode == "skip":
                            course.state = State.DISABLED
                        else:
                            course.state = State.OK
                        course.save()

    semester.save()





def reload_stream_from_gd(stream):
    gc = login()
    sheets = gc.open(stream.gd_spreadsheet_name).worksheets()
    old_semesters = dict()
    for semester in stream.semester_set.all():
        old_semesters[semester.name] = semester
    for sheet in sheets:
        name = sheet._title
        if sheet.cell(3, 1).value == "login":
            if name[0].isdigit():
                name = "семестр " + name
            if name in old_semesters:
                semester = old_semesters[name]
                del old_semesters[name]
            else:
                semester = Semester(name=name, stream=stream)
            semester.year = sheet.cell(2, 2).value
            semester.semester_num = int(sheet.cell(3, 2).value)
            semester.save()
            reload_semester_from_gd(semester, sheet)
    for semester in old_semesters:
        semester.delete()


