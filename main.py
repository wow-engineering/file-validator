from pathlib import Path
from file_validator.reader import read_csv
from file_validator.validators import (
    validate_required_fields,
    validate_unique_fields,
    validate_email_fields
)

def main():
    contacts = read_csv(Path('examples/contacts.csv'))

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

if __name__ == "__main__":
    main()