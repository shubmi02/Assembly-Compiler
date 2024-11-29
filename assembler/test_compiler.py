from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def main():
    # Step 1: Read the assembly code from a text file
    input_file = "input.txt"
    try:
        with open(input_file, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Step 2: Tokenize the code using the Lexer
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    print("Tokens:")
    for token in tokens:
        print(token)

    # Step 3: Parse the tokens using the Parser
    parser = Parser(tokens)
    parsed_instructions = parser.parse()
    print("\nParsed Instructions:")
    for instruction in parsed_instructions:
        print(instruction)

    # Step 4: Generate machine code using the CodeGenerator
    code_generator = CodeGenerator(parsed_instructions)
    machine_code = code_generator.generate()
    print("\nMachine Code:")
    for line in machine_code:
        print(line)

    # Step 5: Save the machine code to an output file
    output_file = "output_machine_code.txt"
    with open(output_file, "w") as file:
        for line in machine_code:
            file.write(line + "\n")
    print(f"\nMachine code saved to '{output_file}'")

if __name__ == "__main__":
    main()
