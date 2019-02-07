import pyodbc
import pandas as pd

def ExecuteSQLBySQLServer(sql):
    con = pyodbc.connect(r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=db;UID=python;PWD=python;')
    cur = con.cursor()
    cur.execute(sql)
    con.commit()
    con.close()

def ReadQueryBySQLServer(sql):
    con = pyodbc.connect(r'DRIVER={SQL Server};SERVER=localhost\SQLExpress;DATABASE=db;UID=python;PWD=python;')
    df = pd.io.sql.read_sql(sql,con)
    con.close()
    return(df)