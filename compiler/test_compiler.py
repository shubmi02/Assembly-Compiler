import argparse
from lexer import Lexer
from parser import Parser
from code_generator import CodeGenerator

def main():
    parser = argparse.ArgumentParser(description="Simple C++ Compiler")
    parser.add_argument("file", help="The source code file to compile")
    parser.add_argument("-o", "--output", help="Specify output file for intermediate code", required=False)
    args = parser.parse_args()

    # Step 1: Read the input C++ code
    try:
        with open(args.file, "r") as file:
            code = file.read()
    except FileNotFoundError:
        print(f"Error: The file '{args.file}' was not found.")
        return

    # Step 2: Tokenize the code using the Lexer
    lexer = Lexer()
    tokens, lexer_errors = lexer.tokenize(code)

    if lexer_errors:
        print("Lexer Errors:")
        for error in lexer_errors:
            print(error)
        return

    # Step 3: Parse the tokens using the Parser
    parser = Parser(tokens)
    successful_parse = parser.parse()

    if not successful_parse:
        print("\nParser Errors:")
        for error in parser.errors:
            print(error)
        return

    # Step 4: Generate intermediate code using CodeGenerator
    code_generator = CodeGenerator(tokens)
    generated_code = code_generator.generate()

    # Step 5: Print or save the generated code
    if generated_code:
        if args.output:
            with open(args.output, "w") as output_file:
                for line in generated_code:
                    output_file.write(line + "\n")
            print(f"Intermediate code saved to '{args.output}'")
        else:
            print("\nGenerated Code:")
            for line in generated_code:
                print(line)

if __name__ == "__main__":
    main()
