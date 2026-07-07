import os
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python cp.py <source file> <target file>")
        sys.exit(2)

    source = sys.argv[1]
    target = sys.argv[2]

    if not os.path.exists(source):
        print("cp: cannot stat '" + source +
              "': No such file or directory", file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(source):
        print("cp: -r not specified; omitting directory '" + source + "'",
              file=sys.stderr)
        sys.exit(1)

    if os.path.isdir(target):
        target = os.path.join(target, os.path.basename(source))

    try:
        if os.path.exists(target) and os.path.samefile(source, target):
            print("cp: '" + source + "' and '" + target +
                  "' are the same file", file=sys.stderr)
            sys.exit(1)

        # Files are copied in blocks so large files do not fill the memory.
        with open(source, "rb") as infile, open(target, "wb") as outfile:
            block = infile.read(4096)
            while len(block) > 0:
                outfile.write(block)
                block = infile.read(4096)

        print("'" + source + "' is copied to '" + target + "'")

    except FileNotFoundError:
        print("cp: cannot create regular file '" + target +
              "': No such file or directory", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print("cp: cannot create regular file '" + target +
              "': Permission denied", file=sys.stderr)
        sys.exit(1)


main()
