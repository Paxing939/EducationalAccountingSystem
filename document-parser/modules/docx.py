from docx import Document
from functools import reduce
from .database import Profession

def load_document(path: str) -> list[Profession]:
    docx = Document(path)
    rows = reduce(lambda r, t: r + list(t.rows), docx.tables, [])[1:]
    professions = [Profession(
        code = row.cells[0].text,
        name = row.cells[1].text,
        etks = row.cells[2].text,
        education_durations = None,
        education_categories = [row.cells[3].text],
        retraining_only = True
        ) for row in rows]
    return professions
