# Install and execution

1. Make sure to have a python install in your $PATH variable.
2. Run tests with `python3 test_challenge.py`
3. Run the program with inputs from input.txt with `python3 challenge.py`

# Solution

This problem, due to it's simple nature of no requirements, was implemented as a simple script, with an entity representing the employee with name, schedule and salary, as well as utility functions.

The solution implements a single readline loop, that parses each line as an employee, and calculates the salary from the parsed schedule. An intermediate representation of the schedule was created to make the salary calculation easier. The solution also handles overnight and hours between different rate intervals.
