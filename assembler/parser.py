class Parser:
    def __init__(self, tokens):
        self.tokens = tokens  # The list of tokens from the lexer
        self.position = 0     # Track the current token position

    def parse(self):
        """
        Parse the list of tokens and build a representation of the program.

        Returns:
            List[dict]: A list of parsed instructions, where each instruction is represented as a dictionary.
        """
        instructions = []
        
        while self.position < len(self.tokens):
            instruction = self._parse_instruction()
            if instruction:
                instructions.append(instruction)
        
        return instructions

    def _parse_instruction(self):
        """
        Parse a single instruction.

        Returns:
            dict: A dictionary representing the parsed instruction.
        """
        # Get the current token
        if self.position >= len(self.tokens):
            return None
        
        current_token = self.tokens[self.position]

        # Handle label definitions (e.g., 'start:')
        if current_token['type'] == 'LABEL':
            self.position += 1
            return {'type': 'LABEL', 'name': current_token['value'][:-1]}  # Remove the colon (:)

        # Handle instructions (e.g., MOV, ADD, SUB)
        if current_token['type'] == 'INSTRUCTION':
            instruction_name = current_token['value']
            self.position += 1
            
            # Parse the operands
            operands = []
            while self.position < len(self.tokens):
                current_token = self.tokens[self.position]
                
                if current_token['type'] in ['REGISTER', 'LITERAL', 'MEMORY', 'IMMEDIATE']:
                    operands.append(current_token['value'])
                    self.position += 1
                elif current_token['type'] == 'COMMA':
                    # Skip commas
                    self.position += 1
                else:
                    # End of instruction
                    break
            
            # Validate the instruction (e.g., correct number of operands)
            self._validate_instruction(instruction_name, operands)

            return {'type': 'INSTRUCTION', 'name': instruction_name, 'operands': operands}
        
        # If we encounter anything unexpected, raise a syntax error
        raise SyntaxError(f"Unexpected token at line {current_token['line']}: '{current_token['value']}'")

    def _validate_instruction(self, name, operands):
        """
        Validate the given instruction based on its name and operands.
        Raises a SyntaxError if the instruction is invalid.
        """
        # Define expected operand counts for supported instructions
        instruction_formats = {
            'MOV': 2,  # MOV <destination>, <source>
            'ADD': 3,  # ADD <destination>, <source1>, <source2>
            'SUB': 3,  # SUB <destination>, <source1>, <source2>
            'LDR': 2,  # LDR <destination>, [<base register>, #<offset>]
            'STR': 2,  # STR <source>, [<base register>, #<offset>]
            'CMP': 2,  # CMP <register1>, <register2>
            'B': 1,    # B <label>
        }

        if name in instruction_formats:
            expected_count = instruction_formats[name]
            if len(operands) != expected_count:
                raise SyntaxError(f"Invalid number of operands for '{name}': Expected {expected_count}, got {len(operands)}")
        else:
            raise SyntaxError(f"Unknown instruction: '{name}'")
