class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens from the lexer
        self.position = 0     # Current token position
        self.errors = []      # List to store errors for error reporting

    def parse(self):
        """
        Parse the list of tokens and check for syntax correctness.

        Returns:
            bool: True if parsing is successful, otherwise False.
        """
        while self.position < len(self.tokens):
            try:
                self._parse_statement()
            except SyntaxError as e:
                self.errors.append(str(e))
                # Skip the problematic token to continue parsing
                self.position += 1

        return len(self.errors) == 0

    def _parse_statement(self):
        current_token = self._current_token()

        if current_token['type'] == 'KEYWORD' and current_token['value'] == 'int':
            # Look ahead to distinguish function definitions from variable declarations
            next_token = self._look_ahead()
            if next_token and next_token['type'] == 'IDENTIFIER':
                next_next_token = self._look_ahead(2)
                if next_next_token and next_next_token['type'] == 'PUNCTUATION' and next_next_token['value'] == '(':
                    self._parse_function_definition()
                else:
                    self._parse_declaration()
            else:
                self._parse_declaration()
        elif current_token['type'] == 'KEYWORD' and current_token['value'] == 'if':
            self._parse_if_statement()
        elif current_token['type'] == 'KEYWORD' and current_token['value'] == 'return':
            self._parse_return_statement()
        elif current_token['type'] == 'IDENTIFIER':
            self._parse_assignment()
        else:
            raise SyntaxError(f"Unexpected token at line {current_token['line']}: '{current_token['value']}'")

    def _parse_function_definition(self):
        # Expect keyword 'int' followed by an identifier (e.g., 'main')
        self._consume('KEYWORD', 'int')
        function_name = self._consume('IDENTIFIER')['value']

        # Expect '(' and then ')'
        self._consume('PUNCTUATION', '(')
        self._consume('PUNCTUATION', ')')

        # Expect '{' followed by statements and then '}'
        self._consume('PUNCTUATION', '{')
        while self._current_token()['value'] != '}':
            self._parse_statement()
        self._consume('PUNCTUATION', '}')

    def _parse_declaration(self):
        # Expect keyword 'int' followed by an identifier
        self._consume('KEYWORD', 'int')
        identifier = self._consume('IDENTIFIER')['value']

        # Optionally expect '=' followed by a literal or identifier
        if self._current_token()['type'] == 'OPERATOR' and self._current_token()['value'] == '=':
            self._consume('OPERATOR', '=')
            self._parse_expression()

        # End of declaration statement
        self._consume('PUNCTUATION', ';')

    def _parse_if_statement(self):
        # Expect 'if' keyword
        self._consume('KEYWORD', 'if')

        # Expect '(' followed by a condition expression and then ')'
        self._consume('PUNCTUATION', '(')
        self._parse_expression()
        self._consume('PUNCTUATION', ')')

        # Expect '{' followed by statements and then '}'
        self._consume('PUNCTUATION', '{')
        while self._current_token()['value'] != '}':
            self._parse_statement()
        self._consume('PUNCTUATION', '}')

    def _parse_return_statement(self):
        # Expect 'return' keyword
        self._consume('KEYWORD', 'return')

        # Optionally expect a literal or identifier to return
        if self._current_token()['type'] in ['LITERAL', 'IDENTIFIER']:
            self._consume(self._current_token()['type'])

        # End of return statement
        self._consume('PUNCTUATION', ';')

    def _parse_assignment(self):
        # Expect an identifier followed by '=' and then an expression
        identifier = self._consume('IDENTIFIER')['value']
        self._consume('OPERATOR', '=')
        self._parse_expression()
        self._consume('PUNCTUATION', ';')

    def _parse_expression(self):
        # Parse a simple expression, including identifiers, literals, and operators
        token = self._current_token()

        if token['type'] in ['IDENTIFIER', 'LITERAL']:
            self._consume(token['type'])
            # Continue parsing if there is an operator
            while self._current_token() and self._current_token()['type'] == 'OPERATOR':
                self._consume('OPERATOR')
                next_token = self._current_token()
                if next_token and next_token['type'] in ['IDENTIFIER', 'LITERAL']:
                    self._consume(next_token['type'])
                else:
                    raise SyntaxError(f"Invalid token in expression at line {next_token['line']}: '{next_token['value']}'")
        else:
            raise SyntaxError(f"Invalid expression at line {token['line']}: '{token['value']}'")

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
