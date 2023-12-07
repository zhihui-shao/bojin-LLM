import re

str1 = "我想了解(1)基金,在(2)年(3)季度的(4)第(5)大重股。该持仓股票当个季度的涨跌幅?请四舍五入保留百分比到小数点两位。"
str2 = "我想了解汇安信利债券A基金,在2020年二季度的季报第3大重股。该持仓股票当个季度的涨跌幅?请四舍五入保留百分比到小数点两位。"

p = re.compile(r'\(\d*?\)', re.S)
new_str1 = re.findall(p, str1)
print(new_str1)

str2_other = re.split(p, str1)
print(str2_other)
for i in str2_other:
    str2 = str2.replace(i, '@', 1)

str2 = str2.removeprefix('@')
str2 = str2.removesuffix('@')
new_str2 = str2.split('@')
print(new_str2)

