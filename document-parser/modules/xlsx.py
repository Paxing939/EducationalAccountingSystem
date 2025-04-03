import pandas as pd
from .database import ProfessionsHours

def get_hours(path: str) -> list[ProfessionsHours]:
    df = pd.read_excel(path)
    hours = []
    for index, row in df.iterrows():
        duration = float(row[0])
        theory = int(row[1])
        practice = int(row[2])
        hours.append(ProfessionsHours(duration=duration, theory_hours=theory, practice_hours=practice))

    return hours
