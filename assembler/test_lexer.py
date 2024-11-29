from lexer import Lexer

def main():
    # Assembly Code
    code = """
    MOV R1, 5
    SUB R3, 10
    """
    lexer = Lexer()
    tokens = lexer.tokenize(code)
    for token in tokens:
        print(token)

if __name__ == "__main__":
    main()
