# Smart Calculator
import re
from collections import deque


class Calculator:
    def __init__(self):
        self.user_input = ''
        self.var_dict = dict()
        self.latin_letters = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
        self.help_text = '''Smart Calculator Manual:
                1. Enter your math equation with each number and symbol separated by a space. Equal signs and parentheses don't need space separation.
                2. This calculator supports unary and binary minus operators. (Unary as in: -2) (Binary as in: 3 - 4)
                3. Use variables in your equations only after you have already assigned them. Enter them alone to see their value
                4. Adding any more spaces than 1 does not affect your result.'''
        self.priority = {'+': 1, '-': 1,
                         '*': 2, '/': 2,
                         '^': 3,
                         '(': 0, ')': 0}
        self.postfix = deque()
        self.calc_stack = deque()
        self.calc_in = deque()

    def generate_postfix(self, list_in):
        # SHUNTING-YARD ALGORITHM (Find exact pseudocode on wikipedia)
        list_in = deque(list_in)
        opr_stack = deque()
        while list_in:
            token = list_in.popleft()
            if self.is_number(token):
                self.postfix.append(token)

            # elif token is a function...

            # if token is an operator:
            elif token in self.priority and token not in ['(', ')']:
                if opr_stack:
                    while opr_stack and (self.priority[token] < self.priority[opr_stack[-1]] or (
                            self.priority[token] ==
                            self.priority[opr_stack[-1]] and token != '^')) and opr_stack[-1] != '(':
                        self.postfix.append(opr_stack.pop())
                opr_stack.append(token)

            elif token == '(':
                opr_stack.append(token)

            elif token == ')':
                while opr_stack[-1] != '(':
                    self.postfix.append(opr_stack.pop())
                    if not opr_stack:
                        # Unmatched closing parentheses
                        return IndexError
                if opr_stack[-1] == '(':
                    opr_stack.pop()

        if opr_stack:
            while opr_stack:
                n = opr_stack.pop()
                if n in ['(', ')']:
                    # Unmatched parentheses
                    return IndexError
                self.postfix.append(n)

        return self.postfix

    @staticmethod
    def is_number(string):
        try:
            float(string)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def do_the_math(operator, num2, num1):
        if operator == '+':
            return num1 + num2
        elif operator == '-':
            return num1 - num2
        elif operator == '*':
            return num1 * num2
        elif operator == '/':
            return num1 / num2
        elif operator == '^':
            return num1 ** num2

    def calculate_list(self, input_list):
        self.calc_stack.clear()
        self.calc_in = input_list
        while self.calc_in:
            item = self.calc_in[0]
            # If first item in input_list is a number then add it to the stack
            if isinstance(item, float) or isinstance(item, int):
                self.calc_stack.append(self.calc_in.popleft())

            # Enter the (operator, then the last number, then the second to last) into the do_the_math function
            else:
                self.calc_stack.append(
                    self.do_the_math(self.calc_in.popleft(), self.calc_stack.pop(), self.calc_stack.pop()))
        return self.calc_stack.pop()

    @staticmethod
    def print_it(num):
        if num == int(num):
            num = int(num)
            print(int(num))
        else:
            print(num)

    @property
    def run(self):
        # 1. Save user's input
        self.user_input = input()

        # 2. Check if user's input contains anything
        if self.user_input:

            # 3. Determine input type (command [exit, help], print variable value, var assignment, equation)
            # A. command: execute command
            if self.user_input[0] == '/':
                if self.user_input == '/exit':
                    print('Bye!')
                    exit()
                elif self.user_input == '/help':
                    print(self.help_text)
                else:
                    print('Unknown command')
            else:
                # B. print variable value
                # Separate each item of input into a list and identify the following symbols from nums and placeholders
                for s in ['=', '(', ')', '^', '*']:
                    self.user_input = self.user_input.replace(s, f';{s};')
                self.user_input = re.split('\s|;', self.user_input)
                self.user_input = [x for x in self.user_input if x != '']

                # Converts a list like [2, '--', 3, '+', 'abc', '-', 1] into [2, ['-', '-'], 3, '+', 'abc', '-', 1]
                self.user_input = [
                    float(x) if self.is_number(x) else list(x) if len(x) > 1 and ('+' in x or '-' in x) else x for x in
                    self.user_input]

                if len(self.user_input) == 1:
                    # If input is one number, print it
                    if self.is_number(self.user_input[0]):
                        self.user_input = self.user_input[0]
                        self.print_it(self.user_input)
                        return None
                    # If input is one word or letter, print the variable's value
                    if all(ele in self.latin_letters for ele in self.user_input[0]):
                        try:
                            self.print_it(self.var_dict[self.user_input[0]])
                        except KeyError:
                            print('Unknown variable')
                            return None
                    else:
                        return None
                else:
                    # C. var assignment: save var in a dict
                    # If the second item in a list like ['a', '=', 3] is an equals sign, then assign variable
                    if self.user_input[1] == '=':
                        if len(self.user_input) != 3:
                            print('Invalid assignment')
                            return None
                        # Check if variable name is only latin letters
                        if isinstance(self.user_input[0], str):
                            if all(ele in self.latin_letters for ele in self.user_input[0]):
                                try:
                                    # If user is assigning variable to a number, then do so
                                    if isinstance(self.user_input[2], float):
                                        self.var_dict[self.user_input[0]
                                                      ] = self.user_input[2]

                                    else:
                                        # Becuase user is assigning a variable to another, assign value of var to var
                                        self.var_dict[self.user_input[0]
                                                      ] = self.var_dict[self.user_input[2]]
                                except KeyError:
                                    # User attempted to assign the value a var that doesn't exist to another var
                                    print('Invalid assignment')
                            else:
                                # User attempted to create a variable name that contains non-latin letters
                                print('Invalid identifier')
                        else:
                            # User attempted to create a variable name that is not a string
                            print('Invalid identifier')
                    else:
                        # D. equation: Do the following
                        # a. Simplify repeating minuses.
                        self.user_input = [
                            x if not isinstance(x, list) else '-' if '-' in x and len(x) % 2 != 0 else '+' for x in
                            self.user_input]
                        # b. Convert variables to respective values if possible
                        try:
                            self.user_input = [x if isinstance(x, float) or x in '+-*/^()' else self.var_dict[x] for x
                                               in self.user_input]
                        except KeyError:
                            # Because an unknown variable was referenced, create a list that contains the unknown vars
                            self.user_input = [x for x in self.user_input if
                                               not isinstance(x, float) and x not in '+-*/^()']

                            # Run through the list of unknown vars and check if they contain operators
                            for i in self.user_input:
                                if '/' in i or '*' in i or '^' in i:
                                    print('Invalid expression')
                                    return None

                            # The variable the user referenced could not be found and did not contain operators
                            print('Unknown variable')
                            return None

                        # c. Convert to postfix
                        try:
                            self.user_input = self.generate_postfix(
                                self.user_input)
                        except IndexError:
                            print('Invalid Syntax')

                        # d. Compute mathematically
                        try:
                            self.user_input = self.calculate_list(
                                self.user_input)
                            # 4. Output result
                            self.print_it(self.user_input)
                        except (ArithmeticError, TypeError, IndexError):
                            print('Invalid expression')
                            return None

        return self.user_input


calc = Calculator()

while True:
    calc.run
