import pyodbc
import pandas as pd
import datetime

# Action Query
def ExecuteSQLBySQLServer(sql):
    con = pyodbc.connect(r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=db;UID=python;PWD=python;')
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

# Read Query
def ReadQueryBySQLServer(sql):
    con = pyodbc.connect(r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=db;UID=python;PWD=python;')
    df = pd.io.sql.read_sql(sql,con)
    con.close()
    return(df)

# 2019-02-06T06:00:00+09:00 > 2019/02/06 06:00:00
def ConvertIso2YMDHMS(v):
    return(datetime.datetime.fromisoformat(v).strftime("%Y/%m/%d %H:%M:%S"))