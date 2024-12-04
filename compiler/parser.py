class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # List of tokens from the lexer
        self.position = 0     # Current token position
        self.errors = []      # List to store errors for error reporting

    def parse(self):
        """
        Parse the list of tokens and build the AST.

        Returns:
            ASTNode: The root node of the AST.
        """
        root = ProgramNode()

        while self.position < len(self.tokens):
            try:
                root.children.append(self._parse_statement())
            except SyntaxError as e:
                self.errors.append(str(e))
                # Skip the problematic token to continue parsing
                self.position += 1

        return root

    def _parse_statement(self):
        current_token = self._current_token()

        if current_token['type'] == 'KEYWORD' and current_token['value'] == 'int':
            # Look ahead to distinguish function definitions from variable declarations
            next_token = self._look_ahead()
            if next_token and next_token['type'] == 'IDENTIFIER':
                next_next_token = self._look_ahead(2)
                if next_next_token and next_next_token['type'] == 'PUNCTUATION' and next_next_token['value'] == '(':
                    return self._parse_function_definition()
                else:
                    return self._parse_declaration()
            else:
                return self._parse_declaration()
        elif current_token['type'] == 'KEYWORD' and current_token['value'] == 'if':
            return self._parse_if_statement()
        elif current_token['type'] == 'KEYWORD' and current_token['value'] == 'return':
            return self._parse_return_statement()
        elif current_token['type'] == 'IDENTIFIER':
            return self._parse_assignment()
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
        body = []
        while self._current_token()['value'] != '}':
            body.append(self._parse_statement())
        self._consume('PUNCTUATION', '}')

        # Return a FunctionDefinitionNode to add to the AST
        return FunctionDefinitionNode(function_name, body)

    def _parse_declaration(self):
        # Expect keyword 'int' followed by an identifier
        self._consume('KEYWORD', 'int')
        identifier = self._consume('IDENTIFIER')['value']

        # Optionally expect '=' followed by a literal or identifier
        value = None
        if self._current_token()['type'] == 'OPERATOR' and self._current_token()['value'] == '=':
            self._consume('OPERATOR', '=')
            value = self._parse_expression()

        # End of declaration statement
        self._consume('PUNCTUATION', ';')

        # Return a DeclarationNode to add to the AST
        return DeclarationNode(identifier, value)

    def _parse_if_statement(self):
        # Expect 'if' keyword
        self._consume('KEYWORD', 'if')

        # Expect '(' followed by a condition expression and then ')'
        self._consume('PUNCTUATION', '(')
        condition = self._parse_expression()
        self._consume('PUNCTUATION', ')')

        # Expect '{' followed by statements and then '}'
        self._consume('PUNCTUATION', '{')
        body = []
        while self._current_token()['value'] != '}':
            body.append(self._parse_statement())
        self._consume('PUNCTUATION', '}')

        # Return an IfStatementNode to add to the AST
        return IfStatementNode(condition, body)

    def _parse_return_statement(self):
        # Expect 'return' keyword
        self._consume('KEYWORD', 'return')

        # Optionally expect a literal or identifier to return
        value = None
        if self._current_token()['type'] in ['LITERAL', 'IDENTIFIER']:
            value = self._consume(self._current_token()['type'])['value']

        # End of return statement
        self._consume('PUNCTUATION', ';')

        # Return a ReturnNode to add to the AST
        return ReturnNode(value)

    def _parse_assignment(self):
        # Expect an identifier followed by '=' and then an expression
        identifier = self._consume('IDENTIFIER')['value']
        self._consume('OPERATOR', '=')
        expression = self._parse_expression()

        # End of assignment statement
        self._consume('PUNCTUATION', ';')

        # Return an AssignmentNode to add to the AST
        return AssignmentNode(identifier, expression)

    def _parse_expression(self):
        # Parse a simple expression, including identifiers, literals, and operators
        token = self._current_token()

        if token['type'] in ['IDENTIFIER', 'LITERAL']:
            left = self._consume(token['type'])['value']
            # Continue parsing if there is an operator
            while self._current_token() and self._current_token()['type'] == 'OPERATOR':
                operator = self._consume('OPERATOR')['value']
                next_token = self._current_token()
                if next_token and next_token['type'] in ['IDENTIFIER', 'LITERAL']:
                    right = self._consume(next_token['type'])['value']
                    left = BinaryOperationNode(operator, left, right)
                else:
                    raise SyntaxError(f"Invalid token in expression at line {next_token['line']}: '{next_token['value']}'")
            return left
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

# AST Node Classes
class ASTNode:
    def __init__(self, node_type):
        self.type = node_type
        self.children = []

class ProgramNode(ASTNode):
    def __init__(self):
        super().__init__('Program')

class DeclarationNode(ASTNode):
    def __init__(self, identifier, value=None):
        super().__init__('Declaration')
        self.identifier = identifier
        self.value = value

class AssignmentNode(ASTNode):
    def __init__(self, identifier, expression):
        super().__init__('Assignment')
        self.identifier = identifier
        self.expression = expression

class IfStatementNode(ASTNode):
    def __init__(self, condition, body):
        super().__init__('IfStatement')
        self.condition = condition
        self.body = body

class FunctionDefinitionNode(ASTNode):
    def __init__(self, name, body):
        super().__init__('FunctionDefinition')
        self.name = name
        self.body = body

class ReturnNode(ASTNode):
    def __init__(self, value):
        super().__init__('Return')
        self.value = value

class BinaryOperationNode(ASTNode):
    def __init__(self, operator, left, right):
        super().__init__('BinaryOperation')
        self.operator = operator
        self.left = left
        self.right = right
