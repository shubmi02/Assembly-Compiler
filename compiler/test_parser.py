from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def main():
    # Step 1: Read the input C++ code from a text file
    input_file = "input.cpp"
    try:
        with open(input_file, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{input_file}' was not found.")
        return

    # Step 2: Tokenize the code using the Lexer
    lexer = Lexer()
    tokens, lexer_errors = lexer.tokenize(code)

    if lexer_errors:
        print("Lexer Errors:")
        for error in lexer_errors:
            print(error)
        return  # Stop if there are lexer errors

    # Step 3: Parse the tokens using the Parser
    parser = Parser(tokens)
    successful_parse = parser.parse()

    if not successful_parse:
        print("\nParser Errors:")
        for error in parser.errors:
            print(error)
    else:
        print("\nParsing successful with no errors.")

        # Step 4: Generate intermediate code using CodeGenerator
        code_generator = CodeGenerator(tokens)
        generated_code = code_generator.generate()
        print("\nGenerated Code:")
        for line in generated_code:
            print(line)

if __name__ == "__main__":
    main()
