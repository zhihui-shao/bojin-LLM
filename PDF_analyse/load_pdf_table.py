import pdfplumber

with pdfplumber.open('path/to/your/file.pdf') as pdf:
    # 获取第一页的所有表格
    tables = pdf.pages[0].extract_tables()
    for table in tables:
        print(table)
