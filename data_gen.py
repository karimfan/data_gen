from enum import Enum
from random import seed
import random
import string
import math


def generate_random_string(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


class OutputFormat(Enum):
    CSV = 1
    JSON = 2


class University:
    def __init__(self, subjects, grade_range, num_students, separate_first_name_last_name=True):
        seed(1)
        val = random.random()
        self.subjects = subjects
        self.grade_range = grade_range
        self.num_students = num_students
        self.separate_first_name_last_name = separate_first_name_last_name
        self.students = []

    def generate_student_grades(self):
        for i in range(self.num_students):
            first_name, last_name = University.__generate_student_name(
                self.separate_first_name_last_name)
            student = Student(first_name, last_name)
            for s in self.subjects:
                grade = University.__generate_grade(self.grade_range)
                student.set_grade(s, grade)

            self.students.append(student)

    @classmethod
    def __generate_grade(cls, grade_range):
        grade_offset = random.randrange(0, len(grade_range))
        grade = grade_range[grade_offset]

        # Randomly inject some missing grades
        if random.randrange(1, 10) <= 1:
            grade = ""
        return grade

    @classmethod
    def __generate_student_name(cls, separate_first_name_last_name):
        first_name = generate_random_string(math.ceil(random.random() * 10))
        last_name = generate_random_string(math.ceil(random.random() * 10))

        if separate_first_name_last_name is False:
            first_name = first_name + "__" + last_name
            last_name = ""

        return first_name, last_name

    def serialize(self, file_name, format=OutputFormat.CSV):
        with open(file_name, 'w') as outfile:
            if self.separate_first_name_last_name is True:
                outfile.writelines(
                    ["first_name, last_name, subject, grade", "\n"])
            for i in self.students:
                i.serialize(outfile)


class Student:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name
        self.subject_grades = []

    def set_grade(self, subject, grade):
        self.subject_grades.append((subject, grade))

    def serialize(self, file, format=OutputFormat.CSV):
        if format is OutputFormat.CSV:
            return self.__serialize_as_CSV(file)

    def __serialize_as_CSV(self, file):
        lines = []
        for i in self.subject_grades:
            lines.append("{}, {}, {}, {}".format(
                self.first_name, self.last_name, i[0], i[1]))
            lines.append("\n")
        file.writelines(lines)


def main():
    subjects = ["Maths", "Physics",
                "Social Studies", "Art", "Music", "History"]
    grades = ["A", "A-", "B+", "B", "B-",
              "C+", "C", "C-", "D+", "D", "D-", "F"]
    university = University(subjects, grades, 1024)
    university.generate_student_grades()
    university.serialize("./foo.csv")

    subjects = ["Mathematics", "Physics", "Soc Studies", "Art",
                "Music", "Ancient History", "Biology", "Neural Networks"]
    grades = list(range(100))
    university = University(subjects, grades, 1024,
                            separate_first_name_last_name=False)
    university.generate_student_grades()
    university.serialize("./foo2.csv")


if __name__ == "__main__":
    main()
