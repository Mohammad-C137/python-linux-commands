import difflib
import sys


def number_range(start, end):
    if end - start == 1:
        return str(start + 1)
    return str(start + 1) + "," + str(end)


def write_line(mark, line):
    sys.stdout.buffer.write(mark + line)
    if not line.endswith(b"\n"):
        sys.stdout.buffer.write(b"\n")
        sys.stdout.buffer.write(b"\\ No newline at end of file\n")


def write_text(text):
    sys.stdout.buffer.write(text.encode("utf-8") + b"\n")


def show_change(tag, i1, i2, j1, j2, old_lines, new_lines):
    if tag == "replace":
        command = number_range(i1, i2) + "c" + number_range(j1, j2)
        write_text(command)
        for line in old_lines[i1:i2]:
            write_line(b"< ", line)
        write_text("---")
        for line in new_lines[j1:j2]:
            write_line(b"> ", line)

    elif tag == "delete":
        command = number_range(i1, i2) + "d" + str(j1)
        write_text(command)
        for line in old_lines[i1:i2]:
            write_line(b"< ", line)

    elif tag == "insert":
        command = str(i1) + "a" + number_range(j1, j2)
        write_text(command)
        for line in new_lines[j1:j2]:
            write_line(b"> ", line)


def main():
    if len(sys.argv) != 3:
        print("Usage: python diff.py <file1> <file2>")
        sys.exit(2)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    try:
        with open(file1, "rb") as f1:
            old_data = f1.read()
        with open(file2, "rb") as f2:
            new_data = f2.read()
    except FileNotFoundError as e:
        print("diff: " + str(e.filename) + ": No such file or directory",
              file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        print("diff: " + str(e.filename) + ": Permission denied",
              file=sys.stderr)
        sys.exit(2)

    if old_data == new_data:
        sys.exit(0)

    if b"\0" in old_data or b"\0" in new_data:
        write_text("Binary files " + file1 + " and " + file2 + " differ")
        sys.exit(1)

    old_lines = old_data.splitlines(keepends=True)
    new_lines = new_data.splitlines(keepends=True)

    matcher = difflib.SequenceMatcher(None, old_lines, new_lines,
                                      autojunk=False)

    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            show_change(tag, i1, i2, j1, j2, old_lines, new_lines)

    sys.exit(1)


main()
