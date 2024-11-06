import re
from collections import defaultdict
import os

def parse_citation_line(line):
    # Regular expression to extract citation details
    full_case_pattern = re.compile(
        r"FullCaseCitation\('(?P<volume>\d+) (?P<reporter>\S+) (?P<page>\d+)', groups=\{.*?\}, metadata=FullCaseCitation\.Metadata\(parenthetical=(?P<parenthetical>None|'.*?'), pin_cite=(?P<pin_cite>None|\d+), year=(?P<year>None|\d+), court=(?P<court>None|'.*?'), plaintiff=(?P<plaintiff>None|'.*?'), defendant=(?P<defendant>None|'.*?'), extra=None\)\)\)"
    )
    short_case_pattern = re.compile(
        r"ShortCaseCitation\('(?P<volume>\d+) (?P<reporter>\S+) at (?P<pin_cite>\d+)', groups=\{.*?\}, metadata=ShortCaseCitation\.Metadata\(.*?\)\)"
    )

    full_case_match = full_case_pattern.match(line)
    short_case_match = short_case_pattern.match(line)

    if full_case_match:
        return {
            'type': 'FullCaseCitation',
            'volume': full_case_match.group('volume'),
            'reporter': full_case_match.group('reporter'),
            'page': full_case_match.group('page'),
            'pin_cite': full_case_match.group('pin_cite') if full_case_match.group('pin_cite') != 'None' else '',
            'year': full_case_match.group('year') if full_case_match.group('year') != 'None' else '',
            'court': full_case_match.group('court').strip("'") if full_case_match.group('court') != 'None' else '',
            'plaintiff': full_case_match.group('plaintiff'),
            'defendant': full_case_match.group('defendant')
        }
    elif short_case_match:
        return {
            'type': 'ShortCaseCitation',
            'volume': short_case_match.group('volume'),
            'reporter': short_case_match.group('reporter'),
            'pin_cite': short_case_match.group('pin_cite')
        }
    return None

def generate_html_from_file(file_path):
    citations = []

    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            citation = parse_citation_line(line)
            if citation:
                # Extract citation details
                plaintiff = citation.get('plaintiff', '')
                defendant = citation.get('defendant', '')
                volume = citation.get('volume', 'Unknown')
                reporter = citation.get('reporter', 'Unknown')
                page = citation.get('page', '')
                pin_cite = citation.get('pin_cite', '')

                # Truncate defendant at the first occurrence of ' , '
                if ' ,' in defendant:
                    defendant = defendant.split(' , ')[0]

                # Determine the case name
                if plaintiff and defendant:
                    case_name = f"{plaintiff} v. {defendant}"
                elif plaintiff:
                    case_name = plaintiff
                else:
                    case_name = defendant

                # Format the citation line based on the presence of page and pin_cite
                if pin_cite and not page:
                    citation_line = f"{volume} {reporter} at {pin_cite}"
                else:
                    citation_line = f"{case_name}, {volume} {reporter} {page}"
                    if pin_cite:
                        citation_line += f", {pin_cite}"

                # Add the formatted line to the list
                citations.append(f"<p>{citation_line}</p>")
            else:
                print(f"Line {line_number} not matched: {line.strip()}")

    # Join all citation lines into a single HTML output
    html_output = "\n".join(citations)
    return html_output

# Specify the path to your file
file_path = os.path.join(os.path.dirname(__file__), 'sample.txt')
html_output = generate_html_from_file(file_path)

# Print or save the HTML output
print(html_output)