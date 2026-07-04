import re
import sys


def print_line(line, filename, show_name):
    if show_name:
        sys.stdout.buffer.write(filename.encode("utf-8") + b":")
    sys.stdout.buffer.write(line)
    if not line.endswith(b"\n"):
        sys.stdout.buffer.write(b"\n")


def search_file(pattern, filename, show_name):
    found = False

    try:
        if filename == "-":
            infile = sys.stdin.buffer
        else:
            infile = open(filename, "rb")

        for line in infile:
            if pattern.search(line) is not None:
                print_line(line, filename, show_name)
                found = True

        if filename != "-":
            infile.close()

    except FileNotFoundError:
        print("grep: " + filename + ": No such file or directory",
              file=sys.stderr)
        return found, True
    except PermissionError:
        print("grep: " + filename + ": Permission denied", file=sys.stderr)
        return found, True

    return found, False


def main():
    if len(sys.argv) < 2:
        print("Usage: python grep.py <pattern> [file ...]")
        sys.exit(2)

    try:
        pattern = re.compile(sys.argv[1].encode("utf-8"))
    except re.error as e:
        print("grep: " + str(e), file=sys.stderr)
        sys.exit(2)

    files = sys.argv[2:]
    if len(files) == 0:
        files = ["-"]

    show_name = len(files) > 1
    any_match = False
    any_error = False

    for filename in files:
        found, error = search_file(pattern, filename, show_name)
        if found:
            any_match = True
        if error:
            any_error = True

    if any_error:
        sys.exit(2)
    if any_match:
        sys.exit(0)
    sys.exit(1)


main()
