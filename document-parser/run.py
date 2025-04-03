import sys
import modules.pdf as pdf
import modules.docx as docx
from modules.database import add_professions

if len(sys.argv) < 4:
    print(f"Usage: {sys.argv[0]} <pdf_patches_file> <pdf_professions_file> <docx_file>")
    exit(1)

professions = pdf.load_documents(sys.argv[1], sys.argv[2])
add_professions(professions)

professions = docx.load_document(sys.argv[3])
add_professions(professions)
