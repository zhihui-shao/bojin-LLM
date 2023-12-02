import re

str1 = "在(1)年报中，(2)基金第(3)大重仓股的代码和股票名称是什么？"
str2 = "在2020年报中，招商沪深300高贝塔指数基金第三大重仓股的代码和股票名称是什么？"

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

