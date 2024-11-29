from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def main():
    input_file = "input.txt"
    try:
        with open(input_file, "r") as file:
            code = file.read()

    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Step 1: Tokenize the code
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    print("Tokens:")
    for token in tokens:
        print(token)

    # Step 2: Parse the tokens
    parser = Parser(tokens)
    parsed_instructions = parser.parse()
    print("\nParsed Instructions:")
    for instruction in parsed_instructions:
        print(instruction)

    # Step 3: Generate machine code
    code_generator = CodeGenerator(parsed_instructions)
    machine_code = code_generator.generate()
    print("\nMachine Code:")
    for line in machine_code:
        print(line)

if __name__ == "__main__":
    main()
