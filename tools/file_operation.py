import xlrd


def open_excel(file, colnameindex=0, by_index=0):
    data = xlrd.open_workbook(file)
    table = data.sheets()[by_index]
    nrows = table.nrows  # 行数
    ncols = table.ncols  # 列数
    colnames = table.row_values(colnameindex)  # 某一行数据
    list = []
    for rownum in range(1, nrows):
        row = table.row_values(rownum)
        if row:
            app = {}
            for i in range(len(colnames)):
                ctype = table.cell(rownum, i).ctype  # 表格的数据类型
                print(ctype, row[i], type(row[i]))
                if ctype == 2 and row[i] % 1 == 0.0:
                    row[i] = int(row[i])
                    print(row[i])
                app[colnames[i]] = row[i]
            list.append(app)
    return list  # 返回元素为字典的列表