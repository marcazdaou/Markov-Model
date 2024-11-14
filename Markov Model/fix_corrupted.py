from markov_model import MarkovModel
import stdio
import sys


# Entry point.
def main():
    k = int(sys.argv[1])
    corrupted = sys.argv[2]
    text = sys.stdin.read()
    # Create a Markov model using text and k.
    model = MarkovModel(text, k)

    # Use the model to decode corrupted.
    decoded = model.replace_unknown(corrupted)

    # Write the decoded text to standard output.
    stdio.writeln(decoded)


if __name__ == '__main__':
    main()
