import docx
import os
import PyPDF2
from eyecite import get_citations, clean

def extract_text_from_docx(docx_path):
    doc = docx.Document(docx_path)
    text = clean.all_whitespace('\n'.join([para.text for para in doc.paragraphs]))
    return text

def extract_text_from_pdf(pdf_path):
    text = ""
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        for page in reader.pages:
            text += page.extract_text() + "\n"
    return clean.all_whitespace(text)

def extract_citations(text):
    citations = get_citations(text)
    return citations

def save_citations_to_file(citations, output_path):
    with open(output_path, 'w') as file:
        for citation in citations:
            file.write(str(citation) + '\n')

def process_file(file_path, output_path):
    if file_path.endswith('.docx'):
        text = extract_text_from_docx(file_path)
    elif file_path.endswith('.pdf'):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith('.txt'):
        with open(file_path, 'r') as file:
            text = clean.all_whitespace(file.read())
    else:
        raise ValueError("Unsupported file type. Supported types are: .docx, .pdf, .txt")

    citations = extract_citations(text)
    save_citations_to_file(citations, output_path)

def main(file_path=None):
    if file_path is None:
        file_path = input("Please enter the file path: ")

    # Debugging: Print the file path to verify
    print(f"Debug: Checking file path: {file_path}")

    if not os.path.isfile(file_path):
        raise ValueError("The provided file path does not exist.")
    
    file_name, file_extension = os.path.splitext(file_path)
    output_path = f"{file_name}_citations.txt"
    
    process_file(file_path, output_path)

def parse_citation_line(line):
    # Extract the relevant parts of the citation
    try:
        # Split the line to extract the citation details
        citation_start = line.find('(') + 1
        citation_end = line.find(')', citation_start)
        citation_details = line[citation_start:citation_end]

        # Extract the volume, reporter, page, pin_cite, plaintiff, and defendant
        parts = citation_details.split(", ")
        volume_reporter_page = parts[0].strip("'")
        pin_cite = parts[1].split('=')[1].strip("'")
        plaintiff = parts[2].split('=')[1].strip("'")
        defendant = parts[3].split('=')[1].strip("'")

        # Format into HTML
        html_paragraph = f"<p>{volume_reporter_page} - {pin_cite} {plaintiff} v. {defendant}</p>"
        return html_paragraph
    except Exception as e:
        print(f"Error parsing line: {line}\n{e}")
        return None

def convert_to_html(file_path):
    html_output = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("FullCaseCitation"):
                html_paragraph = parse_citation_line(line)
                if html_paragraph:
                    html_output.append(html_paragraph)
    return "\n".join(html_output)

if __name__ == "__main__":
    main()
