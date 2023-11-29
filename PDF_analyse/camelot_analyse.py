import camelot


pdf_path = "../bs_challenge_financial_14b_dataset/pdf/3e0ded8afa8f8aa952fd8179b109d6e67578c2dd.PDF"
# 1.读取pdf
tables = camelot.read_pdf(pdf_path, flavor='stream')
# 2.导出pdf所有的表格为csv文件
tables.export('3e0ded8afa8f8aa952fd8179b109d6e67578c2dd.csv', f='csv') # json, excel, html, sqlite
