import argparse

from pathlib import Path
from file_validator.reader import read_csv
from file_validator.validators import (
    validate_required_fields,
    validate_unique_fields,
    validate_email_fields
)
from file_validator.report import (
    build_summary, 
    render_html_report
)

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
    contacts = read_csv(file_path)
    issues = []

    if contacts:
        print(f"Successfully read {len(contacts)} contacts from the CSV file.")
        for contact in contacts:
            print(contact)

        issues = validate_required_fields(
            contacts, 
            required_fields=['client_id', 'name', 'email']
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

        for issue in issues:
            print(issue)

    summary = build_summary(
        len(contacts), 
        issues
    )
    for key, value in summary.items():
        print(f"{key}: {value}")

    html_report = render_html_report(
        summary, issues, file_path.name
    )

    if not args.output:
        output_path = Path(f"report_{file_path.stem}.html")

    else:
        output_path = Path(args.output)
        if output_path.suffix != ".html":
            output_path = output_path.with_suffix(".html")

    output_path.write_text(html_report, encoding='utf-8')
    print(f"HTML report saved to: {output_path}")


if __name__ == "__main__":
    main()