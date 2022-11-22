import xlrd


def read_excel(file_name):
    return (file_name,0)

def read_excel(file_name,sheet_index):
    # 打开excel表格
    try:
        data_excel = xlrd.open_workbook(file_name)

        # 获取所有sheet名称
        names = data_excel.sheet_names()

        # # 获取book中的sheet工作表的三种方法,返回一个xlrd.sheet.Sheet()对象
        table = data_excel.sheet_by_index(sheet_index)  # 通过名称获取

        # # excel工作表的行列操作
        n_rows = table.nrows  # 获取该sheet中的有效行数
        # n_cols=table.ncols  # 获取该sheet中的有效列数
        # for i in range(1, n_rows):
        #     row = table.row(i)
        #     type = row[6].value + ' ' + row[7].value + ' ' + row[11].value
        #     type = type.strip()

        #     if SHANGHAI.get(type) != None:
        #         print(str(SHANGHAI.get(type)))
        #     else:
        #         print("epmty")

       
    except Exception as e:
        print("error " + file_name + " "+ e)
    else:
        pass
    finally:
        pass