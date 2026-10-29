from cs50 import get_int

def main():
    # Pede a altura ao utilizador até que seja um valor válido entre 1 e 8
    while True:
        height = get_int("Height: ")
        if 1 <= height <= 8:
            break

    # Gera a pirâmide linha por linha
    for i in range(1, height + 1):
        # Imprime os espaços em branco seguidos pelos caracteres '#'
        print(" " * (height - i) + "#" * i)

if __name__ == "__main__":
    main()
