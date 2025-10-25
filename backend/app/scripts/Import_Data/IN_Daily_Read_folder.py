from pathlib import Path
import os
from app.scripts.Import_Data import IN_Read_Excel
from datetime import date


def main(Main_dir):
    today = date.today()
    day = today.day
    year = today.year
    month = today.month

    day_import = day - 1

    print("Daily import... from ", Main_dir, day_import, month, year, flush=True)

    for folder_yaer in Main_dir.iterdir():
        year_dir = folder_yaer.name
        year_dir_int = int(year_dir.strip())

        if year_dir_int == year:  # Year Folder Selection
            for folder_month in folder_yaer.iterdir():  # Month Folder Selection

                month_dir = folder_month.name
                month_dir_int = int(month_dir.strip())

                if month_dir_int == month:

                    for Excel in folder_month.iterdir():

                        # Skip if it's not a file
                        if not Excel.is_file():
                            continue

                        # Skip if it doesn't have an Excel extension
                        if Excel.suffix.lower() not in [".xlsx", ".xls", ".xlsm"]:
                            continue

                        # Skip files starting with "0"
                        base_name = Excel.name
                        if base_name.startswith("00") or base_name.startswith("~$"):
                            continue

                        # print(month, year, day, Excel.name)
                        IN_Read_Excel.main_Daily(year, month, day_import, Excel)


if __name__ == "__main__":
    folder_path = r"C:\Users\JakubFornal\Desktop\KP_symulacja_Daily"
    main(Path(folder_path))
