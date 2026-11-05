import csv
from pathlib import Path

def read_csv(
    file_path: Path, 
    delimiter: str = ','
) -> tuple[list[str] | None, list[dict[str, str | None]]]:
    """
    Reads a CSV file and returns its contents as a list of dictionaries.

    Args:
        file_path (Path): The path to the CSV file.
        delimiter (str): The delimiter used in the CSV file. Defaults to ','.
    """

    with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=delimiter)
        header = reader.fieldnames

        if header:
            header = list(header)  # Convert to list to ensure it's mutable
        return header, list(reader)