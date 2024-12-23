import re

class Lexer:
    def __init__(self):
        # Define patterns for different tokens in C++
        self.token_patterns = [
            (r'[ \t]+', None),                       # Ignore whitespace
            (r'\b(int|float|double|char|void|return|if|else|for|while)\b', 'KEYWORD'),  # Keywords
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # Identifiers (e.g., variable or function names)
            (r'\d+\.\d+|\d+', 'LITERAL'),             # Integer and float literals
            (r'==|!=|<=|>=|&&|\|\||[+\-*/=<>]', 'OPERATOR'),  # Operators
            (r'[{}();,]', 'PUNCTUATION'),             # Punctuation characters
            (r'//.*', None),                          # Ignore single-line comments
            (r'/\*[\s\S]*?\*/', None),                # Ignore multi-line comments
        ]
        self.token_regex = self._compile_token_regex()
        self.errors = []  # List to store errors for error reporting

    def _compile_token_regex(self):
        # Compile all token patterns into a single regex
        patterns = [f'(?P<{name}>{pattern})' if name else f'({pattern})' 
                    for pattern, name in self.token_patterns]
        return re.compile('|'.join(patterns))

    def tokenize(self, code):
        tokens = []
        line_number = 1
        for line in code.splitlines():
            position = 0
            while position < len(line):
                match = self.token_regex.match(line, position)
                if not match:
                    # Record the error with line number and invalid token
                    error_message = f"Invalid token at line {line_number}: '{line[position:]}'"
                    self.errors.append(error_message)
                    # Move to the next character to continue lexing
                    position += 1
                else:
                    position = match.end()
                    for name, value in match.groupdict().items():
                        if name and value:
                            tokens.append({'type': name, 'value': value, 'line': line_number})
                            break
            line_number += 1

        # Return the tokens and any errors encountered
        return tokens, self.errors
