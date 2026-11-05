import argparse

from pathlib import Path
from file_validator.reader import read_csv
from file_validator.validators import (
    validate_required_fields,
    validate_unique_fields,
    validate_email_fields,
    validate_header_fields
)
from file_validator.report import (
    build_summary, 
    render_html_report
)
REQUIRED_FIELDS = ['client_id', 'name', 'email']

def parse_arguments():
    parser = argparse.ArgumentParser(description="Validate a CSV file.")
    parser.add_argument("file", help="Path to the CSV file to validate")
    parser.add_argument(
        "--output", 
        "-o", 
        help="Path to save the HTML report", 
        default=None
    )
    return parser.parse_args()

def main():
    args = parse_arguments()

    file_path = Path(args.file)

    if not file_path.is_file():
        print(f"Error: '{file_path}' is not an existing file.")
        return
    

    try:
        header, contacts = read_csv(file_path)
    except (OSError, UnicodeDecodeError) as e:
        print(f"Error: Could not read the file '{file_path}'. {e}")
        return

    summary = None
    issues = validate_header_fields(
        header=header,
        required_fields=REQUIRED_FIELDS
    )

    if issues:
        print("The CSV file is missing required header fields. Validation cannot proceed.")
        for issue in issues:
            print(f"Row {issue['row']}: {issue['message']}")

    else:
        if contacts:
            if len(contacts) > 1:
                print(f"Successfully read {len(contacts)} contacts from the CSV file.")
            else:
                print("Successfully read 1 contact from the CSV file.")

            issues.extend(
                validate_required_fields(
                    contacts, 
                    required_fields=REQUIRED_FIELDS
                )
            )

            issues.extend(
                validate_unique_fields(
                    contacts,
                    unique_fields=['client_id']
                )
            )

            issues.extend(
                validate_email_fields(
                    contacts,
                    email_fields=['email']
                )
            )

        else:
            print("The CSV file contains only the header row. No data to validate.")

        summary = build_summary(
            len(contacts), 
            issues
        )

    html_report = render_html_report(
        summary, issues, file_path.name
    )

    if not args.output:
        output_path = Path(f"report_{file_path.stem}.html")

    else:
        output_path = Path(args.output)
        if output_path.suffix != ".html":
            output_path = output_path.with_suffix(".html")

        if not output_path.parent.is_dir():
            print(f"Error: The directory '{output_path.parent}' does not exist.")
            return
    try:
        output_path.write_text(html_report, encoding='utf-8')
        print(f"HTML report saved to: {output_path}")

    except OSError as e:
        print(f"Error: Could not write to file '{output_path}'. {e}")


if __name__ == "__main__":
    main()