import os
import subprocess

def convert_to_pdfa(file_path):
    _, file_extension = os.path.splitext(file_path)
    if file_extension.lower() == ".pdf":
        # Use Ghostscript to convert PDF to PDF/A
        new_name = file_path.replace(".pdf", "_pdfa.pdf")
        command = ["gs", "-dPDFA", "-dBATCH", "-dNOPAUSE", "-sProcessColorModel=DeviceRGB", "-sDEVICE=pdfwrite", "-sPDFACompatibilityPolicy=1", "-sOutputFile=" + new_name, file_path]
        try:
            subprocess.run(command, check=True)
            print(f"{file_path} has been converted to PDF/A-1b format and saved as {new_name}.")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to convert {file_path} to PDF/A format.")
    elif file_extension.lower() == ".txt":
        # Convert TXT to PDF using Ghostscript
        new_name = file_path.replace(".txt", "_pdfa.pdf")
        command = ["gs", "-sDEVICE=pdfwrite", "-o", new_name, file_path]
        try:
            subprocess.run(command, check=True)
            print(f"{file_path} has been converted to PDF/A-1b format and saved as {new_name}.")
        except subprocess.CalledProcessError:
            print(f"Error: Failed to convert {file_path} to PDF/A format.")
    else:
        print(f"Error: Unsupported file format for {file_path}")

def process_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path) and not filename.startswith("."):
            convert_to_pdfa(file_path)

if __name__ == "__main__":
    folder_path = r"/Users/cadev/Downloads/pdf"  # Test folder
    process_folder(folder_path)
