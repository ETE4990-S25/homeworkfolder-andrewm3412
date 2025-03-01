import json

class Person:
    def __init__(self, name,age, email):
        self.name = name
        self.age = age 
        self.email = email
    

class Student(Person):
    def __init__(self,name,age,email, student_id):
        super().__init__(name,age,email)
        self.student_id = student_id
   
    def save_to_json(self,filename="students.json"):
         with open(filename, "w") as file:
              json.dump(self.__dict__, file, indent = 4)

    def display_student(self, filename = "students.json"):
        try:
            with open(filename, "r") as file:
             student = json.load(file)
             print(student)
        except FileNotFoundError:
            print("No student data found.")

student = Student("Alice", 20, "alice@example.com", 226812)
student.save_to_json()
student.display_student()

   




        