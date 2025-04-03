import sys
import modules.xlsx as xlsx
from modules.database import add_hours

if len(sys.argv) < 2:
    print(f"Usage: {sys.argv[0]} <xlsx_hours_file>")
    exit(1)

hours = xlsx.get_hours(sys.argv[1])
add_hours(hours)
