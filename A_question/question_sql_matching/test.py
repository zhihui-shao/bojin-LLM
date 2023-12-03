import re

str1 = "(1)年(2)季度，有多少家基金发生了净赎回?总共赎回了多少份额?记得给我四舍五入到小数点后两位哦。"
str2 = "2021年三季度，有多少家基金发生了净赎回?总共赎回了多少份额?记得给我四舍五入到小数点后两位哦。"

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

