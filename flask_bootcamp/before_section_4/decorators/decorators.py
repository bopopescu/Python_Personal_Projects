# Function that gets called before another function 

import functools # Library to use decorators

# Function that receives a function as angument
def my_decorator(func):
	

	@functools.wraps(func)
	def function_that_runs_fun():
		print("In the decorator!")
		func()
		print('After the decorator!')

	return function_that_runs_fun 


@my_decorator # Applying the decorator to the function, chaging the function "decorated" by it
# By doing that, we extend the functionality of the function
def my_function():
	print('Im the function')

@my_decorator
def my_num_function():
	print("Here is 10!")


def decorator_with_arguments(num):
	
	def my_decorator(func):
		@functools.wraps(func)
		def function_that_runs_func(*args, **kwargs):
			print("In the decorator")
			if num == 56:
				print('Not running the function')
			else:
				func(*args, **kwargs)
			print("after the decorator!")
		return function_that_runs_func
	return my_decorator


@decorator_with_arguments(56)
def my_function_too():
	print('Hello')


my_function_too()

# Advanced decorators - DEcorators that can accept arguments




