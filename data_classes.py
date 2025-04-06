import json

class Person: 
    def __init__(self, name, age, email):
        self.name =name
        self.age = age 
        self.email = email

class Student(Person):
    def __init__(self, name, age, email, student_id):
        super().__init__(name, age, email)
        self.student_id = student_id
    
    def to_dict(self):
        data = {
        "name":self.name,
        "age":self.age,
        "email":self.email,
        "student_id":self.student_id
        }
        return data
    
    def save_to_json(self, filename):
        Student_dict = self .to_dict()
        with open(filename, 'w') as f:
            json.dump(Student_dict,f, indent=4)
   
    def display_json(self):
        student_dict = self.to_dict()
        print(json.dumps(student_dict, indent=4))

    
        