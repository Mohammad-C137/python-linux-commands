# Simple Linux Commands in Python

Small Python implementations of four common Linux commands: `cp`, `cmp`,
`grep`, and `diff`. This project is mainly an exercise in file handling,
command-line arguments, binary data, regular expressions, and exit codes.

## Usage

```powershell
py cp.py source.txt destination.txt
py cmp.py file1.txt file2.txt
py grep.py "pattern" file.txt
py diff.py file1.txt file2.txt
```

### cp

Copies a file in 4096-byte blocks. The destination can be a file path or an
existing directory. A confirmation message is printed after a successful copy.

### cmp

Checks file sizes first and then compares the contents as binary data. It
reports the first different byte and line, or prints a message when the files
are identical.

### grep

Prints lines that match the given regular expression. More than one input file
can be searched in the same command.

### diff

Shows line-by-line differences between two text files using the normal `diff`
output format.

These programs implement the basic form of each command. Options such as `-r`,
`-i`, `-n`, `-u`, and `--color` are not included.

## Exit codes

- `0`: The operation succeeded, the files are identical, or `grep` found a match.
- `1`: The files differ, `grep` found no match, or `cp` could not copy the file.
- `2`: The command usage is invalid or an input file could not be opened.
