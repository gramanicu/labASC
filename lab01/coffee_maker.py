"""
A command-line controlled coffee maker.
"""

import sys

"""
Implement the coffee maker's commands. Interact with the user via stdin and print to stdout.

Requirements:
    - use functions
    - use __main__ code block
    - access and modify dicts and/or lists
    - use at least once some string formatting (e.g. functions such as strip(), lower(),
    format()) and types of printing (e.g. "%s %s" % tuple(["a", "b"]) prints "a b"
    - BONUS: read the coffee recipes from a file, put the file-handling code in another module
    and import it (see the recipes/ folder)

There's a section in the lab with syntax and examples for each requirement.

Feel free to define more commands, other coffee types, more resources if you'd like and have time.
"""

"""
Tips:
*  Start by showing a message to the user to enter a command, remove our initial messages
*  Keep types of available coffees in a data structure such as a list or dict
e.g. a dict with coffee name as a key and another dict with resource mappings (resource:percent)
as value
"""

import load_recipes as recipes

# Commands
EXIT = "exit"
LIST_COFFEES = "list"
MAKE_COFFEE = "make"  #!!! when making coffee you must first check that you have enough resources!
HELP = "help"
REFILL = "refill"
RESOURCE_STATUS = "status"
commands = {}

# Recipes
recipe_dict = {}

# Coffee
coffee_types = []

# Resources
WATER = "water"
COFFEE = "coffee"
MILK = "milk"

# Coffee maker's resources - the values represent the fill percents
RESOURCES = {WATER: 50, COFFEE: 50, MILK: 50}

# Coffee makers commands
# Exit the program
def exit():
    quit()

# Show all the coffee types
def list_c():
    for type in sorted(coffee_types):
        print(type, end = ' ')
    print()

# Make a coffee
def make():
    # Read the coffee type that is requested
    command = input("Which coffee?: ").lower()

    # Check if the coffee type is valid
    if command in recipe_dict:
        # Check if there are enough resources
        required = recipe_dict[command]

        enough = True
        # Check if there are enough items to make the coffee
        for req_res, req_val in required.items():
            if RESOURCES[req_res] - int(req_val) < 0:
                enough = False

        if enough:
            # Make the coffee and substract the resources
            for req_res, req_val in required.items():
                RESOURCES[req_res] -= int(req_val)
            
            print("Here's your " + command)
        else:
            print("Not enough resources to make this coffee")
    else:
        print("This coffee type does not exist")

# Refill a resource
def refill():
    # Load the resources (for the help text)
    pos_ins = ""
    for res in RESOURCES:
        pos_ins += res + ", "

    pos_ins += "all"

    # Read the resource that will be refilled from input
    command = input("Which resource? (" + pos_ins + "): ").lower()

    # Check if the command is valid
    if command in RESOURCES:
        # Refill one resource
        RESOURCES[command] = 100
    elif command == "all":
        # Refill all resources, one by one
        for res in RESOURCES:
            RESOURCES[res] = 100
    else:
        print("Resource does not exist!")

# Show help (print the available commands)
def help():
    for cmd in commands:
        print(cmd)

# Print the resource levels of the machine
def status():
    for res, val in RESOURCES.items():
        print(res + ": " + str(val) + "%")

# Function that loads the commands in the dictionary
def load_commands():
    commands[EXIT] = exit
    commands[LIST_COFFEES] = list_c
    commands[MAKE_COFFEE] = make
    commands[REFILL] = refill
    commands[RESOURCE_STATUS] = status
    commands[HELP] = help

# Get the coffee types from the recipes (what this machine knows to do)
def parse_recipes():
    global recipe_dict
    recipe_dict = recipes.load()

    for type in recipe_dict:
        coffee_types.append(type)

def main():
    parse_recipes()
    load_commands()
    print("Drink Java Everyday")

    while True:
        # Read the command from input
        command = input("Enter Command: ").lower()

        # Check if the command is valid
        if command in commands:
            commands[command]()
        else:
            print("Command does not exist!")

        # Empty line before asking for another command
        print()

if __name__ == "__main__":
    main()

"""
Example result/interactions:

I'm a smart coffee maker
Enter command:
list
americano, cappuccino, espresso
Enter command:
status
water: 100%
coffee: 100%
milk: 100%
Enter command:
make
Which coffee?
espresso
Here's your espresso!
Enter command:
refill
Which resource? Type 'all' for refilling everything
water
water: 100%
coffee: 90%
milk: 100%
Enter command:
exit
"""
