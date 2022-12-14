import xlrd



def read_excel(file_name,sheet_index):
    try:
        data_excel = xlrd.open_workbook(file_name)
        names = data_excel.sheet_names()
        table = data_excel.sheet_by_index(sheet_index)
        n_rows = table.nrows
        result = []
        for i in range(0, n_rows):
            row = table.row(i)
            # type = row[6].value + ' ' + row[7].value + ' ' + row[11].value
            # type = type.strip()
            result.append(row)
        return result
       
    except Exception as e:
        print("error " + file_name + " "+ e)
    else:
        pass
    finally:
        pass

if __name__ == '__main__':
    read_excel('aws_ec2.xlsx',0)