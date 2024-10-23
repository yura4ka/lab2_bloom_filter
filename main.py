import argparse
import random
import string
import time

from BloomFilter import BloomFilter


def generate_random_string():
    length = random.randint(6, 15)
    letters = string.ascii_lowercase
    random_string = "".join(random.choice(letters) for _ in range(length))
    return random_string


def generate_input():
    n = random.randint(100000, 100000)
    used_strings = []
    result = []
    for _ in range(n):
        action = random.choice(["+", "?"])
        use_existing = used_strings and random.random() >= 0.5
        word = ""
        if use_existing:
            word = random.choice(used_strings)
        else:
            word = generate_random_string()
            used_strings.append(word)
        result.append(f"{action} {word}\n")

    filename = f"generated_input_{int(time.time())}.in"
    with open(filename, "w", encoding="utf-8") as f:
        f.writelines(result)
        f.write("#\n")
    return filename


def main():
    bloom_filter = BloomFilter(50000, 0.33)
    test_set = set()
    total_checks = 0
    false_positives = 0

    def handle_command(command: str):
        nonlocal total_checks, false_positives
        [action, word] = command.split()
        if action == "+":
            bloom_filter.add(word)
            test_set.add(word)
        elif action == "?":
            check = bloom_filter.check(word)
            real = word in test_set
            if check != real:
                false_positives += 1
            total_checks += 1
            print(f"Y {"(N)" if not real else ""}" if check else "N")

    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--file", type=str)
    parser.add_argument(
        "-g",
        "--generate",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if args.generate:
        filename = generate_input()
        print(f"generated input in {filename}")
        return

    if args.file:
        filename = args.file
        with open(filename, "r", encoding="utf-8") as f:
            for command in f:
                if command.strip() == "#":
                    print(
                        f"Total checks: {total_checks}; false positives: {false_positives}; ({100 * false_positives / total_checks}%)"
                    )
                    return
                handle_command(command)
        return

    while True:
        try:
            command = input()
            if command == "#":
                break
            handle_command(command)
        except (EOFError, KeyboardInterrupt):
            break
        except ValueError:
            print("invalid command")


if __name__ == "__main__":
    main()
