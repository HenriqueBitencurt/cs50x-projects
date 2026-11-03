from cs50 import get_string

def main():
    # Pergunta o nome do utilizador
    name = get_string("What is your name? ")

    # Imprime a saudação com o nome fornecido
    print(f"hello, {name}")

if __name__ == "__main__":
    main()
