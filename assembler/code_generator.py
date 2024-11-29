class CodeGenerator:
    def __init__(self, parsed_instructions):
        self.instructions = parsed_instructions
        self.machine_code = []

    def generate(self):
        for instruction in self.instructions:
            if instruction['type'] == 'LABEL':
                # Skip labels, as they are only needed for branching instructions
                continue
            elif instruction['type'] == 'INSTRUCTION':
                machine_code_line = self._generate_instruction(instruction)
                self.machine_code.append(machine_code_line)
        return self.machine_code

    def _generate_instruction(self, instruction):
        name = instruction['name']
        operands = instruction['operands']

        # Generate machine code based on the instruction name
        if name == 'MOV':
            return f"1101 {self._reg_to_bin(operands[0])} {self._imm_to_bin(operands[1])}"
        elif name == 'ADD':
            return f"0000 {self._reg_to_bin(operands[0])} {self._reg_to_bin(operands[1])} {self._reg_to_bin(operands[2])}"
        elif name == 'STR':
            return f"0101 {self._reg_to_bin(operands[0])} {self._mem_to_bin(operands[1])}"
        else:
            raise ValueError(f"Unknown instruction: {name}")

    def _reg_to_bin(self, reg):
        return f"{int(reg[1:]):04b}"  # Converts R0, R1 to 4-bit binary

    def _imm_to_bin(self, imm):
        if imm.startswith('#'):
            return f"{int(imm[1:]):08b}"  # Converts #5 to 8-bit binary

    def _mem_to_bin(self, mem):
        # Parse memory references like [R3, #0]
        reg, offset = mem[1:-1].split(', ')
        return f"{self._reg_to_bin(reg)} {self._imm_to_bin(offset)}"
