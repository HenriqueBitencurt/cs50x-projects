import csv
import sys


def main():

    if len(sys.argv) != 3:
        print("Usage: python dna.py data.csv sequence.txt")
        sys.exit(1)

    database_file = sys.argv[1]
    sequence_file = sys.argv[2]

    rows = []
    with open(database_file) as file:
        reader = csv.DictReader(file)
        for row in reader:
            rows.append(row)

    with open(sequence_file) as file:
        dna_sequence = file.read()

    str_counts = {}
    subsequences = list(rows[0].keys())[1:]

    for sub in subsequences:
        str_counts[sub] = longest_match(dna_sequence, sub)

    for person in rows:
        match = True
        for sub in subsequences:
            if int(person[sub]) != str_counts[sub]:
                match = False
                break
        if match:
            print(person["name"])
            return

    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    for i in range(sequence_length):

        count = 0

        while True:

            start = i + count * subsequence_length
            end = start + subsequence_length

            if sequence[start:end] == subsequence:
                count += 1

            else:
                break

        longest_run = max(longest_run, count)

    return longest_run


if __name__ == "__main__":
    main()
