# # Why use class methods
# class Student():

# 	def __init__(self,name,school):

# 		self.name = name
# 		self.school = school
# 		self.marks = []

# 	def average(self):

# 		return self(self.marks) / len(self.marks)

# 	def friend(self, friend_name):

# 		return Student(friend_name, self.school)

# 	@classmethod
# 	def friend(cls, origin, friend_name):
		
# 		if cls is WorkingStudent:
# 			return cls(friend_name, origin.school, 20.00)
# 		elif cls is Student:
# 			return cls(friend_name, origin.school)


# # Inheritance
# class WorkingStudent(Student):

# 	def __init__(self, name, school, salary):

# 		super().__init__(name, school)
# 		self.salary = salary


# anna = WorkingStudent('ana','Oxford', 20)

# greg = WorkingStudent.friend(anna, 'Greg')
# joan =  Student.friend(anna, 'Joan')
# print(greg.salary)
# print(joan.name)

