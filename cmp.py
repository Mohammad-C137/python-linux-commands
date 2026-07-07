import os
import sys


def main():
    if len(sys.argv) != 3:
        print("Usage: python cmp.py <file1> <file2>")
        sys.exit(2)

    file1 = sys.argv[1]
    file2 = sys.argv[2]

    try:
        # As requested, file sizes are checked before their contents.
        size1 = os.path.getsize(file1)
        size2 = os.path.getsize(file2)

        with open(file1, "rb") as f1, open(file2, "rb") as f2:
            byte_number = 1
            line_number = 1
            bytes_left = min(size1, size2)

            while bytes_left > 0:
                block_size = min(4096, bytes_left)
                block1 = f1.read(block_size)
                block2 = f2.read(block_size)

                if block1 != block2:
                    for i in range(len(block1)):
                        if block1[i] != block2[i]:
                            print(file1 + " " + file2 + " differ: byte " +
                                  str(byte_number + i) + ", line " +
                                  str(line_number))
                            sys.exit(1)
                        if block1[i] == 10:
                            line_number += 1

                else:
                    line_number += block1.count(b"\n")

                byte_number += len(block1)
                bytes_left -= len(block1)

            if size1 != size2:
                if size1 < size2:
                    shorter_file = file1
                    shorter_size = size1
                else:
                    shorter_file = file2
                    shorter_size = size2

                if shorter_size == 0:
                    print("cmp: EOF on " + shorter_file + " which is empty")
                else:
                    print("cmp: EOF on " + shorter_file + " after byte " +
                          str(shorter_size) + ", in line " + str(line_number))
                sys.exit(1)

            print(file1 + " and " + file2 + " are identical")

    except FileNotFoundError as e:
        print("cmp: " + str(e.filename) + ": No such file or directory",
              file=sys.stderr)
        sys.exit(2)
    except PermissionError as e:
        print("cmp: " + str(e.filename) + ": Permission denied",
              file=sys.stderr)
        sys.exit(2)


main()
