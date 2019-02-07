import pyodbc
import pandas as pd
import lib.Util

# データ削除クエリを発行
SQL_TEMPLATE = "DELETE FROM [dbo].[顧客]"       # SQL原本
editSql = SQL_TEMPLATE                          # SQL原本に置換をかける
lib.Util.ExecuteSQLBySQLServer(editSql)      # DELETE文の発行

# dbに突っ込むデータが入っているCSVはUTF-8
df = pd.read_csv(r"data\customer.csv")

##################################
# ここで pandas でデータ加工します #
##################################

# データ追加クエリを発行
SQL_TEMPLATE = "INSERT INTO [dbo].[顧客]([所属],[氏名],[氏名（かな）],[メールアドレス],[住所],[誕生日]) VALUES ('{0}','{1}','{2}','{3}','{4}','{5}')"
for line in df.values:
    editSql = SQL_TEMPLATE                      # SQL原本
    for i,col in enumerate(line):               # SQL原本に置換をかける
        editSql = editSql.replace('{' + str(i) + '}', col)
    lib.Util.ExecuteSQLBySQLServer(editSql)  # INSERT文の発行

# 選択クエリを発行
SQL_TEMPLATE = "SELECT * FROM [dbo].[顧客]"     # SQL原本
editSql = SQL_TEMPLATE                          # SQL原本に置換をかける
df = lib.Util.ReadQueryBySQLServer(editSql)  # SELECT文の発行
for line in df.values:
    print(','.join(line))                       # SQL結果を調理して提供