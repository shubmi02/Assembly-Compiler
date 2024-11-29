import re

class Lexer:
    def __init__(self):
        # Define the patterns for different tokens
        self.token_patterns = [
            (r'[ \t]+', None),  # Ignore whitespace
            (r'MOV|ADD|SUB', 'INSTRUCTION'),  # Instructions
            (r'R[0-9]+', 'REGISTER'),  # Registers (e.g., R0, R1)
            (r'[a-zA-Z_][a-zA-Z0-9_]*:', 'LABEL'),  # Labels (e.g., start:)
            (r'[0-9]+', 'LITERAL'),  # Integers
            (r',', 'COMMA'),  # Separator
            (r'#.*', None),  # Ignore comments
        ]
        self.token_regex = self._compile_token_regex()

    def _compile_token_regex(self):
        """
        Combines all token patterns into a single regular expression.
        """
        patterns = [f'(?P<{name}>{pattern})' if name else f'({pattern})' 
                    for pattern, name in self.token_patterns]
        return re.compile('|'.join(patterns))

    def tokenize(self, code):
        """
        Tokenizes the given assembly code.
        """
        tokens = []
        line_number = 1

        for line in code.splitlines():
            position = 0
            while position < len(line):
                match = self.token_regex.match(line, position)
                if not match:
                    raise SyntaxError(f"Invalid token at line {line_number}: '{line[position:]}'")
                
                position = match.end()  # Move to the end of the matched token
                
                for name, value in match.groupdict().items():
                    if name and value:  # Ignore patterns with None
                        tokens.append({'type': name, 'value': value, 'line': line_number})
                        break
            line_number += 1
        
        return tokens
