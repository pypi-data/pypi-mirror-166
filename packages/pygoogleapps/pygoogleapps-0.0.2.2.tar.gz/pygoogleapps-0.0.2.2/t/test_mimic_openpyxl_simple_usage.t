import pytest
import os,sys,shutil
sys.path.append('.')
import GoogleApps.Service
import GoogleApps.Sheets

class TestSimple():
    service = None
    service.api_key = 'AIzaSyCNHuPIUrHGfwJObsSMm_gYJ4CneK2ESQA'

    def setup_class(cls):
        cls.service = GoogleApps.Service(api_key=cls.api_key)
        cls.sheets = GoogleApps.Sheets.Spreadsheet(cls.service)

    def teardown_class(cls):
        cls.workbook.delete_workbook()
        # disconnect?
        pass

    def test_workbook_create(self):
        wb = cls.sheets.create_workbook('test_mimic_openpyxl_simple_usage')
        ws1 = wb.active
        ws1.title("range names")

        for row in range(1, 40):
            ws1.append(range(20))

        ws2 = wb.create_sheet(title="Pi")
        ws2['F5'] = 3.14

        ws3 = wb.create_sheet(title="Data")
        for row in range(10, 20):
            for col in range(27, 54):
                ws3.cell(column=col, row=row, value="{0}".format(get_column_letter(col)))

        wb.save()

        verify_wb = cls.sheets.load_workbook(wb.id)
        assert wb.active.title == 'range names'
        for row in (1,10,20,30,40):
            assert wb.active['A' + str(row)] == 0
            assert wb.active['D' + str(row)] == 3
            assert wb.active['Z' + str(row)] == 25
            assert wb.active['AA' + str(row)] == 26
            assert not wb.active['B41']

        ws2 = wb['Pi']
        assert ws2['F5'] == 3.14


def woof:
        # set date using a Python datetime
        ws['A1'] = datetime.datetime(2010, 7, 21)

        ws['A1'].number_format
        #'yyyy-mm-dd h:mm:ss'
        # You can enable type inference on a case-by-case basis
        wb.guess_types = True
        # set percentage using a string followed by the percent sign
        ws['B1'] = '3.14%'
        wb.guess_types = False
        ws['B1'].value
        #0.031400000000000004

        ws['B1'].number_format
        #'0%'

        from openpyxl import Workbook
        wb = Workbook()
        ws = wb.active
        # add a simple formula
        ws["A1"] = "=SUM(1, 1)"
        wb.save("formula.xlsx")

        #Merge / Unmerge cells
        #When you merge cells all cells but the top-left one are removed from the worksheet. See Styling Merged Cells for information on formatting merged cells.

        from openpyxl.workbook import Workbook

        wb = Workbook()
        ws = wb.active

        ws.merge_cells('A2:D2')
        ws.unmerge_cells('A2:D2')

        # or equivalently
        ws.merge_cells(start_row=2,start_column=1,end_row=2,end_column=4)
        ws.unmerge_cells(start_row=2,start_column=1,end_row=2,end_column=4)

        wb.save('group.xlsx')
