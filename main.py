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

def main():
    file_path = Path('examples/contacts.csv')
    # file_path = Path('examples/contacts_ok.csv')

    contacts = read_csv(file_path)

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
        Path("report.html").write_text(html_report, encoding='utf-8')

    else:
        print("No contacts found in the CSV file.")


if __name__ == "__main__":
    main()