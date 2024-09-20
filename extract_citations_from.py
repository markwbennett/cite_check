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
    else:
        raise ValueError("Unsupported file type")

    citations = extract_citations(text)
    save_citations_to_file(citations, output_path)

def main(file_path=None):
    if file_path is None:
        file_path = input("Please enter the file path: ")

    if not os.path.isfile(file_path):
        raise ValueError("The provided file path does not exist.")
    
    file_name, file_extension = os.path.splitext(file_path)
    output_path = f"{file_name}_citations.txt"
    
    process_file(file_path, output_path)

if __name__ == "__main__":
    main()