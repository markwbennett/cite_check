import re

def parse_citations(file_path):
    citations = []
    last_citation = None
    citation_map = {}

    with open(file_path, 'r') as file:
        for line in file:
            # Extract the first quoted portion
            match = re.search(r"'([^']*)'", line)
            if not match:
                continue

            citation_text = match.group(1)
            
            # Extract pin_cite from "at {number}" or "pin_cite={number}"
            pin_cite_match = re.search(r'at (\d+)', citation_text)
            pin_cite = pin_cite_match.group(1) if pin_cite_match else None

            # Check for explicit pin_cite
            explicit_pin_cite_match = re.search(r"pin_cite=(\d+)", line)
            if explicit_pin_cite_match:
                pin_cite = explicit_pin_cite_match.group(1)

            # Extract plaintiff, defendant, court, and year
            plaintiff_match = re.search(r"plaintiff='([^']*)'", line)
            defendant_match = re.search(r"defendant='([^']*)'", line)
            court_match = re.search(r"court='([^']*)'", line)
            year_match = re.search(r"year='([^']*)'", line)

            plaintiff = plaintiff_match.group(1) if plaintiff_match else 'none'
            defendant = defendant_match.group(1) if defendant_match else 'none'
            court = court_match.group(1) if court_match else 'none'
            year = year_match.group(1) if year_match else 'none'

            # Trim plaintiff and defendant if they contain ' ,'
            if ' ,' in plaintiff:
                plaintiff = plaintiff.split(' ,')[0]
            if ' ,' in defendant:
                defendant = defendant.split(' ,')[0]

            if citation_text == "Id.":
                if last_citation:
                    volume, reporter, page = last_citation
            else:
                # Split the citation text into volume, reporter, and page
                parts = citation_text.split(' ')
                volume, reporter, page = parts[0], ' '.join(parts[1:-1]), parts[-1]

                # Check if the reporter ends with "at"
                if reporter.endswith(" at"):
                    reporter = reporter[:-3]  # Remove " at"
                    page = None
                    pin_cite = parts[-1]  # Set pin_cite to the page number

                last_citation = (volume, reporter, page)

            # Check for previous citation with the same volume-reporter-page
            citation_key = (volume, reporter, page)
            if citation_key in citation_map:
                if plaintiff == 'none' and defendant == 'none':
                    # Look for the first occurrence with non-none plaintiff/defendant
                    stored_citation = citation_map[citation_key]
                    if stored_citation['plaintiff'] != 'none':
                        plaintiff = stored_citation['plaintiff']
                    if stored_citation['defendant'] != 'none':
                        defendant = stored_citation['defendant']
                else:
                    if plaintiff == 'none':
                        plaintiff = citation_map[citation_key]['plaintiff']
                    if defendant == 'none':
                        defendant = citation_map[citation_key]['defendant']
            else:
                # Store the citation in the map
                citation_map[citation_key] = {
                    'plaintiff': plaintiff,
                    'defendant': defendant
                }

            # Create the data structure
            citation_data = {
                'plaintiff': plaintiff,
                'defendant': defendant,
                'volume': volume,
                'reporter': reporter,
                'page': page,
                'court': court,
                'year': year
            }
            if pin_cite:
                citation_data['pin_cite'] = pin_cite

            citations.append(citation_data)

    return citations

# Example usage
file_path = '/Volumes/12TB/Users/MB/github/cite_check/sample.txt'
citations = parse_citations(file_path)
for citation in citations:
    print(citation)