from cs50 import get_string

def main():
    text = get_string("Text: ")

    letters = 0
    words = 0
    sentences = 0

    length = len(text)

    for i in range(length):
        c = text[i]

        if c.isalpha():
            letters += 1

        if c == ' ' or i == length - 1:
            if c != ' ' or (i > 0 and text[i - 1] != ' '):
                words += 1

        if c == '.' or c == '!' or c == '?':
            sentences += 1

    L = (letters / words) * 100
    S = (sentences / words) * 100

    index = round(0.0588 * L - 0.296 * S - 15.8)

    if index >= 16:
        print("Grade 16+")
    elif index < 1:
        print("Before Grade 1")
    else:
        print(f"Grade {index}")

if __name__ == "__main__":
    main()
