"""
	Bonus task: load all the available coffee recipes from the folder 'recipes/'
	File format:
		first line: coffee name
		next lines: resource=percentage

	info and examples for handling files:
		http://cs.curs.pub.ro/wiki/asc/asc:lab1:index#operatii_cu_fisiere
		https://docs.python.org/3/library/io.html
		https://docs.python.org/3/library/os.path.html
"""

import os

RECIPES_FOLDER = "recipes"

def load():
	# The recipe dictionary
	recipes = {}

	# The path to the recipes folder
	path = "./" + RECIPES_FOLDER

	# Get all the filenames from the specified path
	(_, _, filenames) = next(os.walk(path))

	# Generate the path using the filename
	paths = [(path + "/" + filename) for filename in filenames]

	# Read all the recipes from the specified paths
	for path in paths:
		# Open the recipe file
		recipe = open(path, "r")

		# Read the data into a list
		lines = recipe.readlines()
		# Remove the newline char from the strings
		lines = map(str.strip, lines)

		# Parse the recipe
		count = 0
		coffee_requirements = {}
		coffee_type = ""
		for line in lines:
			if count == 0:
				# The first line is the coffee type
				coffee_type = line
			else:
				# The next lines are added to the resource requirements
				(key, val) = line.split("=")
				coffee_requirements[key]=val
			count += 1

		# Add the recipe to the "dictionary"
		recipes[coffee_type] = coffee_requirements

		# Close the recipe file
		recipe.close()

	# Return the dictionary
	return recipes

if __name__ == "__main__":
    load()