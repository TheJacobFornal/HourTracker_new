from pathlib import Path
import os
from app.scripts.Import_Data import IN_Read_Excel


def go_with_Excels_in_folder(year, month, folder: Path):

    for Excel in folder.iterdir():
        # print("Processing file:", Excel.name, flush=True)
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

        # print(month, year, Excel.name)
        IN_Read_Excel.main(year, month, Excel)


def main_multiple_folder(
    Main_dir,
):  # multiple folders import structure year/month/Excels
    print("Starting import multiple foders... from ", Main_dir, flush=True)
    year = Main_dir.name
    year = int(year.strip())

    for folder in Main_dir.iterdir():
        month = folder.name
        month = int(month.strip())

        go_with_Excels_in_folder(year, month, folder)


if __name__ == "__main__":
    print("Importer do softu HourTracker (version v1.0):")
    mode = input(
        "1 - Import całego miesiąca \n2 - Import jednego Excela \n Wybierz tryb (1/2): "
    )
    print()

    if mode == "1":  # Import całego miesiąca
        # folder_path = r"C:\Users\JakubFornal\Desktop\KP_symulacja_Monthly"
        folder_path = input("Podaj ścieżkę do folderu z Excelami: ")
        year = input("Podaj rok: ")
        month = input("Podaj miesiąc (1-12): ")

        year_int = int(year)
        month_int = int(month)

        print()
        delete_choice = (
            input(
                "Czy chcesz usunąć dane z poprzedniego miesiąca z tymczasowej tabeli? (tak / nie): "
            )
            .strip()
            .lower()
        )

        if delete_choice == "tak":  # delete temp data from temp table logs
            from app.scripts.Import_Data.IN_DB import IN_db

            IN_db.delete_temp_monthly_data(
                int(year), int(month) - 1
            )  # delte previous month temp logs

        print()

        print("Let's gooo..")
        go_with_Excels_in_folder(int(year), int(month), Path(folder_path))

    elif mode == "2":  # Import jednego Excela

        # Excel = r"C:\Users\JakubFornal\Desktop\KP_symulacja_Monthly"
        Excel = input("Podaj ścieżkę do pliku Excel: ")
        year = input("Podaj rok: ")
        month = input("Podaj miesiąc (1-12): ")
        print()
        print("Loading...")
        IN_Read_Excel.main(int(year), int(month), Path(Excel))

    input("Koniec ... naciśnij Enter aby zakończyć.")
