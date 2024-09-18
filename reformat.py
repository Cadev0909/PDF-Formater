import os
import sys
import fitz  # PyMuPDF

def is_pdfa_compliant(doc):
    metadata = doc.metadata
    return "/pdfaid" in metadata

def convert_to_pdfa(file_path):
    doc = None  # Initialize doc variable

    # Check if the file is a PDF or TXT file
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        # Open the PDF
        doc = fitz.open(file_path)
    elif file_extension.lower() == ".txt":
        # Open the TXT file and convert it to PDF
        doc = fitz.open()
        with open(file_path, "r", encoding="utf-8") as txt_file:
            text = txt_file.read()
            page = doc.new_page()
            page.insert_text((50, 50), text)

    # Check if the document is valid (not None)
    if doc is None:
        print(f"Error: Unsupported file format for {file_path}")
        return

    # Check if the PDF is already in PDF/A-1b format
    if is_pdfa_compliant(doc):
        print("Original file %s is already PDF/A compliant." % file_path)
        doc.close()  # Close the document
        return

    # Delete the original file
    os.remove(file_path)
    print(f"Original file {file_path} has been deleted.")
    # Define original and new file paths
    original_name, _ = os.path.splitext(file_path)
    new_name = original_name + ".pdf"

    # Create a PDF/A-1b compliant document
    pdfa_compliant_doc = fitz.open()

    # Add pages from the original document to the PDF/A-1b compliant document
    for page in doc:
        pdfa_compliant_doc.insert_pdf(doc, from_page=page.number, to_page=page.number)

    # Save the PDF/A-1b compliant document with the original name
    pdfa_compliant_doc.save(new_name)
    pdfa_compliant_doc.close()
    doc.close()

    print(f"{file_path} has been converted to PDF/A-1b format and saved as {new_name}.")


def process_folder(folder_path):
    # Iterate over files in the folder
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and not filename.startswith("."):
            convert_to_pdfa(file_path)

if __name__ == "__main__":
    #folder_path = r"/Users/cadev/Downloads/pdf"  # Test folder
    #folder_path = r"/smb/recv"
    if len(sys.argv) != 2:
        print("Usage: python reformat.py $folder_path")
        sys.exit(1)

    process_folder(sys.argv[1])