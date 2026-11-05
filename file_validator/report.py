import html
from file_validator.models import ValidationIssue

def build_summary(
    total_rows: int,
    issues: list[ValidationIssue]
) -> dict[str, int]:
    total_issues = len(issues)
    invalid_rows = len(set(issue['row'] for issue in issues))
    valid_rows = total_rows - invalid_rows

    return {
        "total_rows": total_rows,
        "total_issues": total_issues,
        "invalid_rows": invalid_rows,
        "valid_rows": valid_rows
    }

def render_html_report(
    summary: dict[str, int] | None,
    issues: list[ValidationIssue],
    csv_filename: str = "data.csv"
) -> str:
    
    html_content = f"""
        <html>
        <head>
            <title>Validation Report</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                table {{ border-collapse: collapse; width: 100%; }}
                th, td {{ border: 1px solid #ddd; padding: 8px; }}
                th {{ background-color: #f2f2f2; }}
            </style>
        </head>
        <body>
            <h1>Validation Report</h1>
            <h3><i>Filename: {html.escape(csv_filename, quote=True)}</i></h3>
    """
    if summary:
        if summary['total_rows'] > 0:
            html_content += """
                <h2>Summary</h2>
            """

            if summary['invalid_rows'] > 0:
                if summary['total_rows'] == 1:
                    summary_message = "The only row needs correction"
                else:
                    summary_message = (
                        f"{summary['invalid_rows']} of {summary['total_rows']} "
                        f"rows need correction"
                    )

            else:
                if summary['valid_rows'] > 1:
                    summary_message = f"All {summary['total_rows']} rows are valid"
                else:
                    summary_message = f"The only row is valid"

            html_content += f"""
                <h4><i>{summary_message}</i></h4>
                <ul>
                    <li>Total Rows Processed: {summary['total_rows']}</li>
                    <li>Total Issues Found: {summary['total_issues']}</li>
                    <li>Invalid Rows: {summary['invalid_rows']}</li>
                    <li>Valid Rows: {summary['valid_rows']}</li>
                </ul>
            """

        else:
            html_content += "<p>No rows were processed.</p>"

    if issues:
        html_content += """
            <h2>Issues</h2>
            <table>
                <tr>
                    <th>Row</th>
                    <th>Field</th>
                    <th>Code</th>
                    <th>Message</th>
                </tr>
        """

        sorted_issues = sorted(
            issues, 
            key=lambda x: x['row'],
        )

        for issue in sorted_issues:
            html_content += f"""
                <tr>
                    <td>{issue['row']}</td>
                    <td>{html.escape(issue['field'], quote=True)}</td>
                    <td>{html.escape(issue['code'], quote=True)}</td>
                    <td>{html.escape(issue['message'], quote=True)}</td>
                </tr>
            """

        html_content += "</table>"

    html_content += """
    </body>
    </html>
    """

    return html_content