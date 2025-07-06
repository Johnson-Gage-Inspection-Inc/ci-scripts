#!/usr/bin/env python3
"""
Check for #REF! errors in Excel files and export sheets with formulas.
"""
import csv
import os
import sys
from pathlib import Path

import openpyxl
from openpyxl.cell.cell import Cell
from openpyxl.utils.exceptions import InvalidFileException


def export_sheets_with_formulas(xlsx_path: Path, output_dir: Path):
    """Export all sheets from Excel file to CSV, preserving formulas."""
    wb = openpyxl.load_workbook(xlsx_path, data_only=False, keep_links=False)
    output_dir.mkdir(parents=True, exist_ok=True)

    for sheet in wb.worksheets:

        def get_formula_or_value(cell: Cell) -> str:
            val = cell.value
            if cell.data_type == "f":
                return val if isinstance(val, str) else val.text
            else:
                return val

        csv_path = output_dir / f"{sheet.title}.csv"
        with open(csv_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            rows = [
                [get_formula_or_value(cell) for cell in row]
                for row in sheet.iter_rows(values_only=False)
            ]
            writer.writerows(rows)

        # After writing, check if all rows are just commas
        with open(csv_path, "r+", encoding="utf-8") as f:
            content = f.read()
            if all(
                not any(cell.strip() for cell in line.split(","))
                for line in content.splitlines()
            ):
                f.seek(0)
                f.truncate()


def check_ref_errors(file_path: Path):
    """Check for #REF! errors in Excel file."""
    try:
        # Load workbook
        workbook = openpyxl.load_workbook(file_path, data_only=False)
        ref_errors = []

        # Check each worksheet
        for sheet_name in workbook.sheetnames:
            sheet = workbook[sheet_name]

            # Check all cells in the sheet
            for row in sheet.iter_rows():
                for cell in row:
                    if cell.value and isinstance(cell.value, str):
                        if "#REF!" in str(cell.value):
                            ref_errors.append(
                                {
                                    "sheet": sheet_name,
                                    "cell": cell.coordinate,
                                    "formula": cell.value,
                                }
                            )

        workbook.close()
        return ref_errors

    except InvalidFileException:
        print(f"❌ Error: {file_path} is not a valid Excel file")
        return None
    except Exception as e:
        print(f"❌ Error reading {file_path}: {str(e)}")
        return None


def delete_existing_exploded(base_path: str = "exploded"):
    """Delete existing exploded directory contents."""
    exploded_path = Path(base_path)
    if exploded_path.exists():
        for child in exploded_path.glob("*"):
            if child.is_file():
                child.unlink()
            elif child.is_dir():
                for subchild in child.glob("**/*"):
                    if subchild.is_file():
                        subchild.unlink()
                try:
                    child.rmdir()
                except OSError:
                    pass  # Directory not empty, skip


def main():
    """Main function to check Excel files for #REF! errors."""

    # Get Excel file from environment variable or command line
    excel_file = os.environ.get("EXCEL_FILE")
    export_sheets = os.environ.get("EXPORT_SHEETS", "false").lower() == "true"

    if not excel_file and len(sys.argv) > 1:
        excel_file = sys.argv[1]

    if not excel_file:
        print(
            "❌ No Excel file specified. Set EXCEL_FILE environment "
            "variable or pass as argument."
        )
        sys.exit(1)

    file_path = Path(excel_file)

    if not file_path.exists():
        print(f"❌ File not found: {file_path}")
        sys.exit(1)

    supported_extensions = {".xlsx", ".xltm", ".xlsm", ".xltx", ".xlsb"}
    if file_path.suffix.lower() not in supported_extensions:
        print(f"❌ Unsupported file type: {file_path.suffix}")
        sys.exit(1)

    print(f"🔍 Checking {file_path.name} for #REF! errors...")

    # Check for #REF! errors
    ref_errors = check_ref_errors(file_path)

    if ref_errors is None:
        sys.exit(1)
    elif len(ref_errors) > 0:
        print(f"❌ Found {len(ref_errors)} #REF! errors:")
        for error in ref_errors:
            sheet = error["sheet"]
            cell = error["cell"]
            formula = error["formula"]
            print(f"  - Sheet '{sheet}', Cell {cell}: {formula}")
        print("\n❌ Please fix broken references before merging.")
        sys.exit(1)
    else:
        print("✅ No #REF! errors found.")

    # Export sheets if requested
    if export_sheets:
        print("📊 Exporting sheets with formulas...")
        delete_existing_exploded()

        exploded_root = Path("exploded") / file_path.stem
        sheets_dir = exploded_root / "sheets"

        try:
            export_sheets_with_formulas(file_path, sheets_dir)
            print(f"✅ Sheets exported to: {sheets_dir}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to export sheets: {str(e)}")

    print("✅ Excel validation completed successfully.")
    sys.exit(0)


if __name__ == "__main__":
    main()
