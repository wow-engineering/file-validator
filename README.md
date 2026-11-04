# file-validator

A Python command-line tool that checks contact CSV files before import and
generates an HTML report showing which rows need correction.

For example, the sample file contains seven contacts. The report identifies
five rows to correct and explains each issue, including the first occurrence
of a duplicate client ID.

![CSV validation report showing five rows that need correction](docs/report-preview.png)

## What it checks

- **Required values** in `client_id`, `name`, and `email`.
- **Duplicate client IDs**, with the row number of the first occurrence.
- **Basic email format** for non-empty email values.

The tool reads UTF-8 CSV files with a header row. The sample files also
include `city` and `country`.

## Quick start

Run these commands from the repository root with Python 3.12. The project
uses the Python standard library.

```bash
python -m main examples/contacts.csv
```

Open `report_contacts.html` in a browser to see the summary and the list of
issues sorted by row number.

| Command | Report | Expected result |
| --- | --- | --- |
| `python -m main examples/contacts.csv` | `report_contacts.html` | 5 of 7 rows need correction |
| `python -m main examples/contacts_ok.csv -o report_check_file.htm` | `report_check_file.html` | No issues found |
| `python -m main examples/contacts_empty.csv` | `report_contacts_empty.html` | No rows were processed |

By default, the report is written to the current directory as
`report_<input-name>.html`, using the input filename without its extension.
Use `-o` or `--output` to choose an output path. If the extension is missing
or differs from `.html`, the tool sets it to `.html`.

Run `python -m main --help` to see the command-line options.

## Tests

```bash
python -m unittest discover -s tests -v
```

The tests cover required values, duplicate detection, and basic email format,
including missing values and whitespace.