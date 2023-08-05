# this file datafile.py has the same filename to datafile.xlsx (but different extension)
# if xlwings addin is installed, press button "run main" in the Microsoft Excel tab 'xlwings'
# this file will be load, and the function main() will be called by xlwings.
#
import office
import pandas


def main():
    book = office.Excel()  # if xlwings called, get the active workbook
    # book['Sales!A12'].value = "abb"
    # book['Sales!A12'].value = book['Sales'].name
    # book.move_sheet('Sales', 88)
    # book.active.unprotect("123")
    # book.unprotect("123")
    sheet = book.sheets.active
    # sheet['A10'].value = str(sheet.max_row) + ', ' + str(sheet.max_column)
    # print(sheet['A1'].value)

    df = pandas.DataFrame(columns=["Name", "Age"], data=[["Peter", 18], ["Sam", 19]])

    # sheet.write_dataframe('A11', df)
    sheet['A11'].value = book.filename
    book.save()
    book.close()
    # sheet['A12'].value = str(type(office.excel))
    # sheet['A13'].value = str(type(office.excel.Excel))


if __name__ == "__main__":
    # if run in command line, call main()
    main()
