"""
cd ./scripts
python history.py input.txt output.txt
"""

import re
import sys
from pathlib import Path
from typing import List, Tuple


PR_REGEX = re.compile(r"(https://github\.com/.+/pull/(\d+))")


def format_pr_entry(line: str) -> Tuple[int, str] | None:
    line = line.strip()
    if not line:
        return None

    match = PR_REGEX.search(line)
    if not match:
        return None

    url, pr_number_str = match.groups()
    pr_number = int(pr_number_str)

    # Extract description (before " by ")
    description = line.lstrip("* ").split(" by ")[0].strip()

    formatted = f"+ `#{pr_number} <{url}>`_ - {description}"
    return pr_number, formatted


def convert_file(input_path: Path, output_path: Path) -> None:
    entries: List[Tuple[int, str]] = []

    with input_path.open("r", encoding="utf-8") as infile:
        for line in infile:
            result = format_pr_entry(line)
            if result:
                entries.append(result)

    # Sort by PR number descending
    entries.sort(key=lambda x: x[0], reverse=True)

    with output_path.open("w", encoding="utf-8") as outfile:
        for _, formatted in entries:
            outfile.write(formatted + "\n")


def main() -> None:
    if len(sys.argv) != 3:
        print("Usage: python convert_prs.py <input_file> <output_file>")
        sys.exit(1)

    input_file = Path(sys.argv[1])
    output_file = Path(sys.argv[2])

    if not input_file.exists():
        print(f"Error: input file '{input_file}' does not exist")
        sys.exit(1)

    convert_file(input_file, output_file)
    print(f"Converted entries written to {output_file}")


if __name__ == "__main__":
    main()
