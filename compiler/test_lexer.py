from lexer import Lexer

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

    # Step 3: Print out the tokens and any errors
    if lexer_errors:
        print("Lexer Errors:")
        for error in lexer_errors:
            print(error)
    else:
        print("Tokens:")
        for token in tokens:
            print(token)

if __name__ == "__main__":
    main()
