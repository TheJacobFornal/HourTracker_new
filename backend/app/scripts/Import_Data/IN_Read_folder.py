from pathlib import Path
import os
from app.scripts.Import_Data import IN_Read_Excel


def main(Main_dir=Path(r"/Users/jacob/Downloads/2024")):

    year = Main_dir.name
    year = int(year.strip())
    print(year)

    for folder in Main_dir.iterdir():

        month = folder.name
        month = int(month.strip())

        for Excel in folder.iterdir():

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

            print(month, year, Excel.name)
            IN_Read_Excel.main(year, month, Excel)

        print(year, month)


if __name__ == "__main__":
    main()
