class CodeGenerator:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.generated_code = []
        self.label_count = 0
        self.temp_var_count = 0

    def generate(self):
        """
        Generate intermediate code for the parsed statements.

        Returns:
            List[str]: List of generated intermediate code instructions.
        """
        while self.position < len(self.tokens):
            try:
                self._generate_statement()
            except SyntaxError as e:
                print(f"Code Generation Error: {e}")
                return []

        return self.generated_code

    def _generate_statement(self):
        current_token = self._current_token()

        if current_token['type'] == 'KEYWORD' and current_token['value'] == 'int':
            # Check if it's a function definition like "int main()"
            next_token = self._look_ahead()
            if next_token and next_token['type'] == 'IDENTIFIER':
                next_next_token = self._look_ahead(2)
                if next_next_token and next_next_token['type'] == 'PUNCTUATION' and next_next_token['value'] == '(':
                    self._generate_function_definition()
                else:
                    self._generate_declaration()
            else:
                self._generate_declaration()
        elif current_token['type'] == 'KEYWORD' and current_token['value'] == 'if':
            self._generate_if_statement()
        elif current_token['type'] == 'KEYWORD' and current_token['value'] == 'return':
            self._generate_return_statement()
        elif current_token['type'] == 'IDENTIFIER':
            self._generate_assignment()
        else:
            raise SyntaxError(f"Unexpected token at line {current_token['line']}: '{current_token['value']}'")

    def _generate_function_definition(self):
        # Consume 'int' and function name
        self._consume('KEYWORD', 'int')
        function_name = self._consume('IDENTIFIER')['value']

        # Consume '(' and ')'
        self._consume('PUNCTUATION', '(')
        self._consume('PUNCTUATION', ')')

        # Consume '{' and generate code for all statements inside the function
        self._consume('PUNCTUATION', '{')
        while self._current_token()['value'] != '}':
            self._generate_statement()
        self._consume('PUNCTUATION', '}')

    def _generate_declaration(self):
        # Consume 'int' and identifier
        self._consume('KEYWORD', 'int')
        identifier = self._consume('IDENTIFIER')['value']

        # Optionally handle assignment
        if self._current_token()['type'] == 'OPERATOR' and self._current_token()['value'] == '=':
            self._consume('OPERATOR', '=')
            value = self._generate_expression()
            self.generated_code.append(f"{identifier} = {value}")

        # Consume ';'
        self._consume('PUNCTUATION', ';')

    def _generate_if_statement(self):
        # Consume 'if'
        self._consume('KEYWORD', 'if')

        # Consume '(' and condition, then ')'
        self._consume('PUNCTUATION', '(')
        condition = self._generate_expression()
        self._consume('PUNCTUATION', ')')

        # Generate labels
        true_label = self._new_label()
        end_label = self._new_label()

        # Generate conditional branch code
        self.generated_code.append(f"IF {condition} GOTO {true_label}")
        self.generated_code.append(f"GOTO {end_label}")

        # Consume '{' and generate code for all statements inside the block
        self._consume('PUNCTUATION', '{')
        self.generated_code.append(f"{true_label}:")
        while self._current_token()['value'] != '}':
            self._generate_statement()
        self._consume('PUNCTUATION', '}')

        # End label
        self.generated_code.append(f"{end_label}:")

    def _generate_return_statement(self):
        # Consume 'return'
        self._consume('KEYWORD', 'return')

        # Optionally handle return value
        if self._current_token()['type'] in ['LITERAL', 'IDENTIFIER']:
            return_value = self._consume(self._current_token()['type'])['value']
            self.generated_code.append(f"RETURN {return_value}")

        # Consume ';'
        self._consume('PUNCTUATION', ';')

    def _generate_assignment(self):
        # Consume identifier, '=', and then expression
        identifier = self._consume('IDENTIFIER')['value']
        self._consume('OPERATOR', '=')
        value = self._generate_expression()
        self.generated_code.append(f"{identifier} = {value}")

        # Consume ';'
        self._consume('PUNCTUATION', ';')

    def _generate_expression(self):
        # Generate an expression, including identifiers, literals, and operators
        token = self._current_token()
        if token['type'] in ['IDENTIFIER', 'LITERAL']:
            left_operand = self._consume(token['type'])['value']
            while self._current_token() and self._current_token()['type'] == 'OPERATOR':
                operator = self._consume('OPERATOR')['value']
                right_operand = self._consume(self._current_token()['type'])['value']
                temp_var = self._new_temp()
                self.generated_code.append(f"{temp_var} = {left_operand} {operator} {right_operand}")
                left_operand = temp_var
            return left_operand
        else:
            raise SyntaxError(f"Invalid expression at line {token['line']}: '{token['value']}'")

    def _new_label(self):
        label = f"L{self.label_count}"
        self.label_count += 1
        return label

    def _new_temp(self):
        temp_var = f"t{self.temp_var_count}"
        self.temp_var_count += 1
        return temp_var

    def _current_token(self):
        if self.position < len(self.tokens):
            return self.tokens[self.position]
        return None

    def _look_ahead(self, steps=1):
        if self.position + steps < len(self.tokens):
            return self.tokens[self.position + steps]
        return None

    def _consume(self, expected_type, expected_value=None):
        current_token = self._current_token()
        if current_token and current_token['type'] == expected_type and (expected_value is None or current_token['value'] == expected_value):
            self.position += 1
            return current_token
        else:
            expected_desc = f"{expected_type} '{expected_value}'" if expected_value else expected_type
            raise SyntaxError(f"Expected {expected_desc}, but got '{current_token}'")
