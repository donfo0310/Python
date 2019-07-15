"""
    SQLServerに接続します（固定値なので適宜書き換えてください）
    接続db: (localhostの)SQLExpress
    接続db: db
    UID: python
    PWD: python
"""
import datetime
import pandas as pd
import pyodbc

def execute_sql_by_sqlserver(sql):
    """Action Query"""
    con_text = r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=db;UID=python;PWD=python;'
    con = pyodbc.connect(con_text)
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def read_query_by_sqlserver(sql):
    """Read Query"""
    con_text = r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=db;UID=python;PWD=python;'
    con = pyodbc.connect(con_text)
    df = pd.io.sql.read_sql(sql, con)
    con.close()
    return df

def convert_iso_to_ymdhms(iso_ymdhms):
    """タイムゾーンつきの文字列のフォーマットを変える 2019-02-06T06:00:00+09:00 -> 2019/02/06 06:00:00"""
    return datetime.datetime.fromisoformat(iso_ymdhms).strftime("%Y/%m/%d %H:%M:%S")
