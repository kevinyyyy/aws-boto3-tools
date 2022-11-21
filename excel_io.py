import xlsxwriter

def write_to_excel(FILE_NAME,RESOURCE_SHEET,FILE_ROWS):
    workbook = xlsxwriter.Workbook(FILE_NAME)
    worksheet = workbook.add_worksheet(RESOURCE_SHEET)
    worksheet.set_column('A:AZ', 15)
    worksheet.set_row(0, 75)
    wrap = workbook.add_format({'text_wrap': True,'align':'center','valign':'vcenter'})
    row = 0
    for item in FILE_ROWS:
        column = 0
        for rowItem in item:
            worksheet.write(row,column,rowItem,wrap)
            column += 1
        row += 1
    
    workbook.close()