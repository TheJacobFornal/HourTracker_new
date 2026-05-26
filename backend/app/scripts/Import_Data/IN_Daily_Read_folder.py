from pathlib import Path
import os
from app.scripts.Import_Data import IN_Read_Excel
from datetime import date
from app.scripts.Import_Data.IN_DB import IN_db
from datetime import datetime
from datetime import date, timedelta


def get_Excel_folder(folder_dir, year, month):
    for folder in folder_dir.iterdir():
        if folder.is_dir() and int(folder.name) == year:
            for subfolder in folder.iterdir():
                folder_number = subfolder.name.split(" ")[0]
                if subfolder.is_dir() and int(folder_number) == month:
                    return subfolder


def main(Main_dir):
    yesterday = date.today() - timedelta(days=1)
    year = yesterday.year
    month = yesterday.month

    Excel_folder = get_Excel_folder(Main_dir, year, month)

    print("Daily import... from ", Excel_folder, month, year, flush=True)
    print()

    IN_db.delete_temp_monthly_data(
        year, month
    )  # delete temp daily data from this month

    for Excel in Excel_folder.iterdir():
        print(Excel.name)

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
        IN_Read_Excel.main_Daily(year, month, Excel)


if __name__ == "__main__":
    # main(Path(r"C:\Users\JakubFornal\Desktop\KP_TEST"))
    main(Path(r"\\SERVER\Projekty\00-BIURO\Karta pracy"))  # Path to folder on server
