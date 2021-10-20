from openpyxl import load_workbook

def delete_rows(num, file_path):
    filename = file_path
    wb = load_workbook(filename)
    ws = wb.active
    ws.delete_rows(1, num)
    wb.save(filename)
