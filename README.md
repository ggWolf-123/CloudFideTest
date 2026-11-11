This repository is a recruitment task of CloudFide for the Support Data Engineer position. 
The solution can be found in task_Jan_Zdyb.py, which contains three functions:

- is_valid_label for checking if DataFrame columns have valid names,

- evaluation_of_expression, function responsible for performing mathematical operations, including addition, subtraction and multiplication,

- add_virtual_column, function for creating new DataFrame using original DataFrame, it first validates the given data, after that, it determines which operation should be performed and which columns need to be included in the calculation in evaluation_of_expression.

For a quick check I created try_my_answer.py with example of DataFrame and a demonstration of add_virtual_column, examples covering addition, subtraction, multiplication, as well as operation involving more then two columns, also one invalid operation (division -> returns empty DataFrame).

There is also a tests folder with test_solution.py, where you can find all my tests (I used pytest (python -m pytest -v)) for functions.

Documentation used:
- https://docs.python.org/3/library/ast.html

AI usage:
I used AI for two specific purposes:
1. Writing tests.
2. To search the documentation more quickly (https://docs.python.org/3/library/ast.html) and to create a simple explanation of it.