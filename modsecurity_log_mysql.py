#!/usr/bin/python3
# -*- coding: UTF-8 -*-

import re
import pymysql
import datetime


# 打开数据库连接
db = pymysql.Connect(
  host='127.0.0.1',
  port=3360,
  user='waf',
  passwd='waf',
  db='waf',
  charset='utf8'
)

# 使用cursor()方法获取操作游标
cursor = db.cursor()

#打开日志
f = open('/var/log/modsec_audit.log')
log = f.read()

it = re.finditer(r"---[\da-zA-Z]{8}---A--[\s\S]*?---[\da-zA-Z]{8}---Z--",log)
for match in it:
    #m_original
    m_original = match.group()

    #日期时间
    m_datetime = re.search(r"\d\d/[a-zA-Z]{3}/\d{4}:\d{2}:\d{2}:\d{2}", match.group()).group()
    m_datetime = datetime.datetime.strptime(m_datetime, "%d/%b/%Y:%H:%M:%S").strftime("%Y-%m-%d %H:%M:%S")

    # host
    m_host = re.search(r"Host:.*", match.group()).group().replace('Host: ','')

    # id
    m_id = []
    it_kid = re.finditer('\[id\s"\d+?"\]', match.group())
    for match_kid in it_kid:
        m_id.append(match_kid.group().replace('[id "','').replace('"]',''))

    # hostname
    m_hostname = []
    it_kid = re.finditer('\[hostname\s".*?"\]', match.group())
    for match_kid in it_kid:
        m_hostname.append(match_kid.group().replace('[hostname "','').replace('"]',''))

    # uri
    m_uri = []
    it_kid = re.finditer('\[uri\s".*?"\]', match.group())
    for match_kid in it_kid:
        m_uri.append(match_kid.group().replace('[uri "','').replace('"]',''))
        
    # data
    m_data = []
    it_kid = re.finditer('\[data\s".*?"\]', match.group())
    for match_kid in it_kid:
        m_data.append(match_kid.group().replace('[data "','').replace('"]',''))

    # msg
    m_msg = []
    it_kid = re.finditer('\[msg\s".*?"\]', match.group())
    for match_kid in it_kid:
        m_msg.append(match_kid.group().replace('[msg "','').replace('"]',''))

    for index in range(len(m_id)):

        # SQL 插入语句
        sql = "INSERT INTO `log` (`id`, `m_datetime`, `m_host`, `m_id`, `m_hostname`, `m_uri`, `m_data`, `m_msg`, `m_original`) VALUES (NULL, %s, %s, %s, %s, %s, %s, %s, %s)"

        #print("sql:" + sql)

        try:
            # 执行sql语句
            cursor.execute(sql,(m_datetime, m_host, m_id[index], m_hostname[index], m_uri[index],m_data[index], m_msg[index], m_original))
            # 提交到数据库执行
            db.commit()
        except:
            # 发生错误时回滚
            print("发生错误sql:" + sql % (m_datetime, m_host, m_id[index], m_hostname[index], m_uri[index],m_data[index], m_msg[index], m_original))
            db.rollback()

# 关闭数据库连接
db.close()

# 清空日志
f.close()
f = open('/var/log/modsec_audit.log','w')
f.write('')
f.close()


