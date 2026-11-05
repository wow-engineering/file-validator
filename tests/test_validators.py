import unittest
from file_validator.validators import (
    validate_email_fields,
    validate_required_fields,
    validate_unique_fields,
    validate_header_fields
)


class TestEmailFields(unittest.TestCase):
    def test_valid_email(self):
        issues = validate_email_fields(
            rows=[{'email': 'alice@example.com'}],
            email_fields=['email']
        )
        self.assertEqual(issues, [])

    def test_invalid_format(self):
        values = [
            "alice@example.com text",  # Extra text after valid email
            "alice@@example.com",  # Double @
            "alice@examplecom",  # Missing domain name
            "sarah.example.com",  # Missing @
        ]

        for value in values:
            with self.subTest(value=value):
                issues = validate_email_fields(
                    rows=[{'email': value}],
                    email_fields=['email']
                )
                self.assertEqual(len(issues), 1)
                self.assertEqual(issues[0]['row'], 2)
                self.assertEqual(issues[0]['field'], 'email')
                self.assertEqual(issues[0]['code'], 'invalid_email')

    def test_missing_values_are_ignored(self):
        for record in [{}, {'email': None}, {'email': ''}, {'email': ' '}]:
            with self.subTest(record=record):
                issues = validate_email_fields(
                    rows=[record],
                    email_fields=['email']
                )
                self.assertEqual(issues, [])


class TestRequiredFields(unittest.TestCase):
    def test_all_required_fields_present_in_header(self):
        issues = validate_header_fields(
            header=['client_id', 'name', 'email'],
            required_fields=['client_id', 'name', 'email']
        )
        self.assertEqual(issues, [])

    def test_missing_required_field_in_header(self):
        issues = validate_header_fields(
            header=['client_id', 'name'],
            required_fields=['client_id', 'name', 'email']
        )

        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['field'], 'email')
        self.assertEqual(issues[0]['code'], 'missing_header')
        self.assertEqual(issues[0]['row'], 1)

    def test_missing_required_fields_in_header(self):
        issues = validate_header_fields(
            header=['client_id'],
            required_fields=['client_id', 'name', 'email']
        )

        self.assertEqual(len(issues), 2)

        self.assertEqual(issues[0]['field'], 'name')
        self.assertEqual(issues[0]['code'], 'missing_header')
        self.assertEqual(issues[0]['row'], 1)

        self.assertEqual(issues[1]['field'], 'email')
        self.assertEqual(issues[1]['code'], 'missing_header')
        self.assertEqual(issues[1]['row'], 1)

    def test_empty_header(self):
        issues = validate_header_fields(
            header=None,
            required_fields=['client_id', 'name', 'email']
        )
        self.assertEqual(len(issues), 1)
        self.assertEqual(issues[0]['field'], '')
        self.assertEqual(issues[0]['code'], 'missing_header')
        self.assertEqual(issues[0]['row'], 1)


    def test_valid_required_fields(self):
        issues = validate_required_fields(
            rows=[{'client_id': 'C001', 'name': 'Alice', 'email': 'alice@example.com'}],
            required_fields=['client_id', 'name', 'email']
        )
        self.assertEqual(issues, [])

    def test_invalid_required_fields(self):
        issues = validate_required_fields(
            rows=[
                {'client_id': 'C001', 'name': '', 'email': 'alice@example.com'},
                {'client_id': 'C002', 'name': 'Bob'},
                {'client_id': '', 'name': 'Charlie', 'email': 'charlie@example.com'}
            ],
            required_fields=['client_id', 'name', 'email']
        )

        self.assertEqual(len(issues), 3)

        self.assertEqual(issues[0]['field'], 'name')
        self.assertEqual(issues[0]['code'], 'required_field')

        self.assertEqual(issues[1]['field'], 'email')
        self.assertEqual(issues[1]['code'], 'required_field')

        self.assertEqual(issues[2]['field'], 'client_id')
        self.assertEqual(issues[2]['code'], 'required_field')

    def test_missing_two_required_fields(self):
        issues = validate_required_fields(
            rows=[{'client_id': 'C001', 'name': '', 'email': ''}],
            required_fields=['client_id', 'name', 'email']
        )
        self.assertEqual(len(issues), 2)
        self.assertEqual(
            {issue["field"] for issue in issues}, 
            {'name', 'email'}
        )

    def test_none_and_whitepace_are_missing(self):
        for value in [None, '', ' ']:
            with self.subTest(value=value):
                issues = validate_required_fields(
                    rows=[{'name': value}],
                    required_fields=['name']
                )
                self.assertEqual(len(issues), 1)
                self.assertEqual(issues[0]['field'], 'name')
                self.assertEqual(issues[0]['code'], 'required_field')
                self.assertEqual(issues[0]['row'], 2)


class TestUniqueFields(unittest.TestCase):
    def test_valid_unique_fields(self):
        issues = validate_unique_fields(
            rows=[
                {'client_id': 'C001'},
                {'client_id': 'C002'},
                {'client_id': 'C003'}
            ],
            unique_fields=['client_id']
        )
        self.assertEqual(issues, [])

    def test_three_duplicate_values(self):
        issues = validate_unique_fields(
            rows=[
                {'client_id': 'C002'},
                {'client_id': 'C002'},
                {'client_id': 'C002'},
            ],
            unique_fields=['client_id']
        )

        self.assertEqual(len(issues), 2)

        self.assertEqual(issues[0]['field'], 'client_id')
        self.assertEqual(issues[0]['code'], 'duplicate_value')
        self.assertEqual(issues[0]['row'], 3)

        self.assertEqual(issues[1]['field'], 'client_id')
        self.assertEqual(issues[1]['code'], 'duplicate_value')
        self.assertEqual(issues[1]['row'], 4)

        for issue in issues:
            self.assertEqual(
                issue['message'],
                f"Duplicate value 'C002' in field 'client_id' (first seen at row 2)."
            )

    def test_two_duplicate_values(self):
        issues = validate_unique_fields(
            rows=[
                {'client_id': 'C002'},
                {'client_id': 'C002 '},
            ],
            unique_fields=['client_id']
        )

        self.assertEqual(len(issues), 1)

        self.assertEqual(issues[0]['field'], 'client_id')
        self.assertEqual(issues[0]['code'], 'duplicate_value')
        self.assertEqual(issues[0]['row'], 3)

    def test_no_duplicate_values(self):
        issues = validate_unique_fields(
            rows=[
                {'client_id': 'C001'},
                {'client_id': 'C002'},
                {'client_id': 'c002'},
            ],
            unique_fields=['client_id']
        )
        self.assertEqual(issues, [])

    def test_missing_values_are_ignored(self):
        issues = validate_unique_fields(
            rows=[
                {'client_id': ''},
                {'client_id': ' '},
                {'client_id': None},
                {},
            ],
            unique_fields=['client_id']
        )
        self.assertEqual(issues, [])

    def test_same_value_in_different_fields(self):
        issues = validate_unique_fields(
            rows=[
                {'client_id': 'C001', 'external_id': 'C002'},
                {'client_id': 'C002', 'external_id': 'C001'},
            ],
            unique_fields=['client_id', 'external_id']
        )
        self.assertEqual(issues, [])