__author__ = 'progress'

'''
要求除了查询之外都是以字典的形式来实现，
就是直接输入字典进行添加，修改，和删除操作
'''

import re,json,os
filename = 'haproxy.conf'

def search(args):
    '''查找域名对应的信息'''
    result_info = []  # 保存查询到域名下的服务信息
    data = "backend %s" % args
    tags = False
    with open(filename, "r",encoding='utf-8') as f:
        for line in f:
            if line.strip() == data:
                tags = True
                continue
            if tags and line.startswith('backend'):
                break
            if tags and line:
                result_info.append(line.strip())
        for line in result_info:
            print(line)
    return result_info

def file_write_flags(backend_data,result_info):  #代码重用
    with open(filename, 'r', encoding='utf-8') as f, \
            open('haproxy2.conf', 'w', encoding='utf-8') as w:
        tags = False  # 标记修改的域名
        has_write = False  # 标记result_info是否写到新文件
        for line in f:
            if line.strip() == backend_data:
                tags = True
                continue
            if tags and line.startswith('backend'):
                tags = False
            if not tags:
                w.write(line)
            else:
                if not has_write:
                    for new_line in result_info:
                        if new_line.startswith('backend'):
                            w.write(new_line + '\n')
                        else:
                            w.write('%s%s\n' % (' ' * 8, new_line))
                    has_write = True

def add_backend(args):
    '''添加域名对应的信息'''
    backend = args['backend']   #获取字典中的域名
    result_info = search(backend)  #获取字典对应的信息
    backend_data = 'backend %s'%backend
    server_data = 'server %s weight %s maxconn %s'%(args['record']['server'],\
                                                       args['record']['weight'],\
                                                       args['record']['maxconn'])

    if not result_info:
        if '' in result_info: result_info.pop()
        result_info.append(backend_data)
        result_info.append(server_data)
        with open(filename,'r',encoding='utf-8') as f,\
            open('haproxy2.conf','w',encoding='utf-8') as w:
            for line in f:
                w.write(line)
            for new_line in result_info:  #遍历需要添加的内容
                if new_line.startswith('backend'):
                    w.write(new_line+'\n')
                else:
                    w.write('%s%s\n'%(' '*8,new_line))
    else:
        if '' in result_info: result_info.pop()
        result_info.insert(0,backend_data)
        if server_data not in result_info:
            result_info.append(server_data)
            file_write_flags(backend_data,result_info)

        ''' 
        with open(filename, 'r', encoding='utf-8') as r_file, \
                open('haproxy2.conf', 'w', encoding='utf-8') as w_file:
            tags = False
            has_write = False
            for line in r_file:
                if line.strip() == backend_data:
                    tags = True
                    continue
                if tags and line.startswith('backend'):
                    tags = False
                if not tags:
                    w_file.write(line)
                else:
                    if not has_write:
                        for line_info in result_info:
                            if line_info.startswith('backend'):
                                w_file.write(line_info+'\n')
                            elif line_info != '':
                                w_file.write('%s%s\n' % (' '*8,line_info))
                        has_write = True
                        '''
    os.rename('haproxy.conf','haproxy_bak.conf')
    os.rename('haproxy2.conf','haproxy_new.conf')

def delete_daemon(args):
    '''删除指定的信息'''
    backend = args['backend']
    result_info = search(backend)
    backend_data = 'backend %s' % backend
    server_data = 'server %s weight %s maxconn %s' % (args['record']['server'], \
                                                      args['record']['weight'], \
                                                      args['record']['maxconn'])
    if not result_info or server_data not in result_info:
        print('没有当前查找的记录')
    else:
        if len(result_info) == 1:
            if '' in result_info: result_info.pop()
            result_info.remove(server_data)
            file_write_flags(backend_data,result_info)
            '''  
            with open(filename, 'r', encoding='utf-8') as f, \
                    open('haproxy2.conf', 'w', encoding='utf-8') as w:
                tags = False  # 标记修改的域名
                has_write = False  # 标记result_info是否写到新文件
                for line in f:
                    if line.strip() == backend_data:
                        tags = True
                        continue
                    if tags and line.startswith('backend'):
                        tags = False
                    if not tags:
                        w.write(line)
                    else:
                        if not has_write:
                            for new_line in result_info:
                                if new_line.startswith('backend'):
                                    w.write(new_line + '\n')
                                else:
                                    w.write('%s%s\n' % (' ' * 8, new_line))
                            has_write = True
                            '''
        else:
            if '' in result_info: result_info.pop()
            result_info.insert(0,backend_data)
            result_info.remove(server_data)
            file_write_flags(backend_data,result_info)
    os.rename('haproxy.conf', 'haproxy_bak.conf')
    os.rename('haproxy2.conf', 'haproxy_new.conf')

def change_backend(args):
    '''修改域名对应的信息'''
    backend = args[0]['backend']
    result_info = search(backend)
    backend_data = 'backend %s' % backend
    server_data1 = 'server %s weight %s maxconn %s' % (args[0]['record']['server'],\
                                                      args[0]['record']['weight'],\
                                                      args[0]['record']['maxconn'])

    server_data2 = 'server %s weight %s maxconn %s' % (args[1]['record']['server'],\
                                                       args[1]['record']['weight'],\
                                                       args[1]['record']['maxconn'])
    if not result_info or server_data1 not in result_info:
        print('修改的记录不存在')
        return
    else:
        if '' in result_info: result_info.pop()
        result_info.insert(0, backend_data)
        result_info.remove(server_data1)
        result_info.append(server_data2)
        file_write_flags(backend_data, result_info)
    ''' 
        with open(filename, 'r', encoding='utf-8') as r_file, \
                open('haproxy2.conf', 'w', encoding='utf-8') as w_file:
            tags = False
            has_write = False
            for line in r_file:
                if line.strip() == backend_data:   #匹配到当前的域名做标记
                    tags = True
                    continue
                if tags and line.strip() == server_data:  #匹配要删除的server信息做标记
                    tags = False
                if not tags:
                    w_file.write(line)
                else:
                    if not has_write:
                        for line_info in result_info:
                            if line_info.startswith('backend'):
                                w_file.write(line_info+'\n')
                            elif line_info != '':
                                w_file.write('%s%s\n' % (' '*8,line_info))
                        has_write = True
                        '''
    os.rename('haproxy.conf', 'haproxy_bak.conf')
    os.rename('haproxy2.conf', 'haproxy_new.conf')

if __name__ == '__main__':
    flags = '''
    1:查询数据
    2:添加数据
    3:删除数据
    4:修改数据
    5:退出
    '''
    flags_menu = {
        '1':search,
        '2':add_backend,
        '3':delete_daemon,
        '4':change_backend,
        '5':exit

    }

    while True:
        print('欢迎登陆配置文件操作系统')
        print(flags)
        choise = input("请选择需要的操作>>>").strip()
        if choise == '5':
            break
        if len(choise) == 0 or choise not in flags_menu:
            continue
        args = input("Input daemon name:").strip()
        if choise != '1':
            args = eval(args)   #将字符串转换为字典
        flags_menu[choise](args)  #公共接口
