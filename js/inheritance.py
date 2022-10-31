class First: 
	def __init__(self, a, b):
		self.a = a
		self.b = b

	def talk(self):
		print(f"a: {self.a}, b: {self.b}")

class Second(First):
	def __init__(self, a, b, c):
		First.__init__(self, a, b)
		self.c = c

	def talk(self):
		First.talk(self)
		print("And then me! c:" + str(self.c))

second = Second(1, 2, 3)
second.talk()