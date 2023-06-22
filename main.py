class Student:
    def __init__(self, course, name, student_id):
        self.course = course
        self.name = name
        self.student_id = student_id

    def __str__(self):
        return f"{self.course} {self.student_id}, {self.name}"

    def edit(self, course, name, student_id):
        self.course = course
        self.name = name
        self.student_id = student_id


class Course:
    def __init__(self, code, name):
        self.code = code
        self.name = name

    def __str__(self):
        return f"{self.code}, {self.name}"

    def edit(self, code, name):
        self.code = code
        self.name = name
        

class StudentManagementSystem:
    def __init__(self):
        self.students = []
        self.load_from_file("student.txt")
        self.course_management_system = None

    def add_student(self, course, name, student_id):
        if self.is_student_id_duplicate(student_id):
            print("ID number exists. Try again.")
            return
        if not self.course_management_system.is_course_exists(course):
            print("Course does not exist. Do you want to add it?")
            choice = input("[1] Yes [2] No: ")
            if choice == "1":
                course_name = input("Enter the course name: ")
                self.course_management_system.add_course(course, course_name)
            else:
                print("Course and student not added.")
                return
        student = Student(course, name, student_id)
        self.students.append(student)
        self.save_to_file("student.txt")
        self.list_students()
        print("Student added successfully!")

    def delete_student(self, student_id):
        for student in self.students:
            if student.student_id == student_id:
                self.students.remove(student)
                self.save_to_file("student.txt")
                self.list_students()
                print("Student deleted successfully!")
                return
        print("Student not found.")

    def edit_student(self, student_id, course, name, new_student_id):
        if self.is_student_id_duplicate(new_student_id):
            print("ID number exists. Try again.")
            return
        for student in self.students:
            if student.student_id == student_id:
                student.edit(course, name, new_student_id)
                self.save_to_file("student.txt")
                self.list_students()
                print("Student updated successfully!")
                return
        print("Student not found.")

    def list_students(self):
        if not self.students:
            print("No students in the system.")
        else:
            print("List of students:\n")
            for student in self.students:
                print(student)

    def search_student(self, search_key):
        results = []
        for student in self.students:
            if (
                search_key.lower() in student.student_id.lower()
                or search_key.lower() in student.name.lower()
                or search_key.lower() in student.course.lower()
                or search_key.lower() in str(student).lower()
            ):
                results.append(student)
        if not results:
            print("No matching students found.")
        else:
            print(f"{len(results)} matching students found:")
            for result in results:
                print(result)

    def delete_students_by_course(self, course):
        deleted_students = []
        for student in self.students:
            if student.course == course:
                deleted_students.append(student)

        for student in deleted_students:
            self.students.remove(student)

        self.save_to_file("student.txt")

    def is_student_id_duplicate(self, student_id):
        return any(student.student_id == student_id for student in self.students)

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for student in self.students:
                file.write(f"{student.course} {student.student_id}, {student.name}\n")

    def load_from_file(self, filename):
        self.students = []  # Clear the existing student data
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        course, id_name = line.split(" ", 1)
                        student_id, name = id_name.strip().split(",", 1)
                        student = Student(course, name, student_id)
                        self.students.append(student)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")


class CourseManagementSystem:
    def __init__(self):
        self.courses = []
        self.load_from_file("course.txt")
        self.student_management_system = None

    def add_course(self, code, name):
        if self.is_course_code_duplicate(code):
            print("Course already exists. Try again.")
            return
        course = Course(code, name)
        self.courses.append(course)
        self.save_to_file("course.txt")
        self.list_courses()
        print("Course added successfully!")

    def delete_course(self, code):
        deleted_students = self.delete_students_by_course(code)
        if deleted_students:
            print(f"Deleted {len(deleted_students)} associated students:")
            for student in deleted_students:
                print(student)
        else:
            print("No associated students found.")

        for course in self.courses:
            if course.code == code:
                self.courses.remove(course)
                self.save_to_file("course.txt")
                self.list_courses()
                print("Course deleted successfully!")
                break
        else:
            print("Course not found.")

    def delete_students_by_course(self, course_code):
        deleted_students = []
        for student in self.student_management_system.students:
            if student.course == course_code:
                deleted_students.append(student)
        for student in deleted_students:
            self.student_management_system.students.remove(student)
        self.student_management_system.save_to_file("student.txt")
        return deleted_students

    def edit_course(self, code, name):
        for course in self.courses:
            if course.code == code:
                course.edit(code, name)
                self.save_to_file("course.txt")
                self.list_courses()
                print("Course updated successfully!")
                return
        print("Course not found.")

    def list_courses(self):
        if not self.courses:
            print("No courses in the system.")
        else:
            print("List of courses:\n")
            for course in self.courses:
                print(course)

    def search_course(self, search_key):
        results = []
        for course in self.courses:
            if (
                search_key.lower() in course.code.lower()
                or search_key.lower() in course.name.lower()
                or search_key.lower() in str(course).lower()
            ):
                results.append(course)
        if not results:
            print("No matching courses found.")
        else:
            print(f"{len(results)} matching courses found:")
            for result in results:
                print(result)

    def is_course_code_duplicate(self, code):
        return any(course.code == code for course in self.courses)

    def is_course_exists(self, code):
        return any(course.code == code for course in self.courses)

    def save_to_file(self, filename):
        with open(filename, "w") as file:
            for course in self.courses:
                file.write(f"{course.code}, {course.name}\n")

    def load_from_file(self, filename):
        self.courses = []  # Clear the existing course data
        try:
            with open(filename, "r") as file:
                lines = file.readlines()
                for line in lines:
                    line = line.strip()
                    if line:
                        code, name = line.split(",", 1)
                        course = Course(code.strip(), name.strip())
                        self.courses.append(course)
        except FileNotFoundError:
            print(f"File '{filename}' not found.")



def main():
    course_management_system = CourseManagementSystem()
    student_management_system = StudentManagementSystem()
    course_management_system.student_management_system = student_management_system
    student_management_system.course_management_system = course_management_system
   
    while True:
        print("\n1. CRUDL operations for students")
        print("2. CRUDL operations for courses")
        print("3. Exit\n")
        choice = input("Enter your choice:")

        if choice == '1':
            while True:
                print("\n1. Add student")
                print("2. Delete student")
                print("3. Edit student")
                print("4. List of students")
                print("5. Search student")
                print("6. Go back\n")
                student_choice = input("Enter your choice:")

                if student_choice == '1':
                    course = input("Enter the course: ")
                    if not course_management_system.is_course_exists(course):
                        print("Course does not exist. Do you want to add it?")
                        print("[1] Yes")
                        print("[2] No")
                        choice = input("Enter your choice:")
                        if choice == '1':
                            name = input("Enter the course name(BS of Computer Science): ")
                            course_management_system.add_course(course, name)
                        elif choice == '2':
                            print("Course and student not added.")
                            continue
                        else:
                            print("Invalid choice. Course and student not added.")
                            continue

                    name = input("Enter the student name: ")
                    student_id = input("Enter the ID: ")
                    student_management_system.add_student(course, name, student_id)

                elif student_choice == '2':
                    student_id = input("Enter the ID of the student to be deleted: ")
                    student_management_system.delete_student(student_id)

                elif student_choice == '3':
                    student_id = input("Enter the ID of the student to be edited: ")
                    course = input("Enter the new course: ")
                    name = input("Enter the new name: ")
                    new_student_id = input("Enter the new ID: ")
                    student_management_system.edit_student(student_id, course, name, new_student_id)

                elif student_choice == '4':
                    student_management_system.list_students()

                elif student_choice == '5':
                    search_key = input("Enter the search key: ")
                    student_management_system.search_student(search_key)

                elif student_choice == '6':
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == '2':
            while True:
                print("\n1. Add course")
                print("2. Delete course")
                print("3. Edit course")
                print("4. List of courses")
                print("5. Search course")
                print("6. Go back\n")
                course_choice = input("Enter your choice:")

                if course_choice == '1':
                    code = input("Enter the code: ")
                    name = input("Enter the name: ")
                    course_management_system.add_course(code, name)

                elif course_choice == '2':
                    code = input("Enter the code of the course to be deleted: ")
                    course_management_system.delete_course(code)

                elif course_choice == '3':
                    code = input("Enter the code of the course to be edited: ")
                    name = input("Enter the new name: ")
                    course_management_system.edit_course(code, name)

                elif course_choice == '4':
                    course_management_system.list_courses()

                elif course_choice == '5':
                    search_key = input("Enter the search key: ")
                    course_management_system.search_course(search_key)

                elif course_choice == '6':
                    break

                else:
                    print("Invalid choice. Please try again.")

        elif choice == '3':
            print("Exiting program...")
            break

        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()






