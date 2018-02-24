__author__ = 'linux vfast'

'''
工资管理系统
Alex 100000
Rain 80000
Egon 50000
Yuan 30000
-----以上是info.txt文件-----
实现效果：
从info.txt文件中读取员工及其工资信息，最后将修改或增加的员工工资信息也写入原info.txt文件。
效果演示：
1. 查询员工工资
2. 修改员工工资
3. 增加新员工记录
4. 退出
>>:1
请输入要查询的员工姓名（例如：Alex）：Alex
Alex的工资是：100000。
1. 查询员工工资
2. 修改员工工资
3. 增加新员工记录
4. 退出
>>:2
请输入要修改的员工姓名和工资，用空格分隔（例如：Alex 10）：Alex 10
修改成功！
1. 查询员工工资
2. 修改员工工资
3. 增加新员工记录
4. 退出
>>:3
请输入要增加的员工姓名和工资，共空格分割（例如：Eric 100000）：Eric 100000
增加成功！
1. 查询员工工资
2. 修改员工工资
3. 增加新员工记录
4. 退出
>>:4
'''

import re
def select_wage():
    '''查询操作'''
    username = input('请输入要查询的员工姓名(例如：Alex):')
    with open('info.txt', 'r', encoding='utf-8') as r_file:
        r_file.seek(0)
        for line in r_file:
            line = line.strip().split()
            if username == line[0]:
                print('%s的工资是:%s.' % (username, line[1]))
            continue

def add_new_person():
    '''添加员工操作'''
    new_user = input('请输入要增加的员工姓名和工资,共空格分割(例如：Eric 100000):')
    with open('info.txt', 'a', encoding='utf-8') as r_file:
        r_file.seek(0)
        r_file.writelines('\n' + new_user.strip())
    print('添加成功')

def run_wage():
    '''工资系统操作'''
    print('欢迎登陆工资系统'.center(50,'*'))
    while True:
        date = [('查询员工工资'), ('修改员工工资'), ('增加新员工记录'), ('退出')]
        for index,line in enumerate(date,start=1):
            print(index,line)
        choose = input('请选择>>>:')
        if choose.isdigit():
            choose = int(choose)
            if choose < len(date) + 1 and choose >= 0:
                if choose == 1:
                    select_wage()
                elif choose == 2:
                    change = input('请输入要修改的员工姓名和工资,用空格分隔(例如：Alex 10):')
                    with open('info.txt', 'r', encoding='utf-8') as r_file:
                        r_file.seek(0)
                        read_info = []
                        for line in r_file:
                            if re.match('%s' % change.strip().split()[0], line):
                                continue
                            else:
                                read_info.append(line)
                        read_info.append(change)
                        with open('info.txt', 'w', encoding='utf-8') as f_file:
                            f_file.seek(0)
                            for line in read_info:
                                f_file.write(line)
                            print('修改成功')
                elif choose == 3:
                    add_new_person()
                else:
                    print('退出成功')
                    break
            else:
                print('输入的[%s]不存在!'% choose)
                continue
        else:
            print('输入的[%s]错误,请重新输入!'% choose)
            continue

run_wage()

