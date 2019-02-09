import urllib
import urllib.request
import pandas as pd
import lib.Util as u

# read appId from textfile
with open('api_setting/appid.txt', mode='r', encoding='utf-8') as f:
    appId = f.read()

# base url
url = r'http://api.e-stat.go.jp/rest/2.1/app/json/getStatsData?'

# query param setting
keys = {
        "appId"            : appId,
        "lang"             : "J" ,
        "statsDataId"      : "0003143513" ,
        "metaGetFlg"       : "Y" ,
        "cntGetFlg"        : "N",
        "sectionHeaderFlg" : "1"
}

# get json-data
query_param = urllib.parse.urlencode(keys)
res = pd.read_json(urllib.request.urlopen(url + query_param).read(), orient='records')

# translation to dataframe from json-data 
data = pd.DataFrame(res['GET_STATS_DATA']['STATISTICAL_DATA']['DATA_INF']['VALUE'])
area = pd.DataFrame(res['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ'][2]['CLASS'])
category = pd.DataFrame(res['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ'][1]['CLASS'])
tab = pd.DataFrame(res['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ'][0]['CLASS'])
time = pd.DataFrame(res['GET_STATS_DATA']['STATISTICAL_DATA']['CLASS_INF']['CLASS_OBJ'][3]['CLASS'])

# name change before joining
area = area.rename(columns={'@name': 'area'})
category = category.rename(columns={'@name': 'category'})
tab = tab.rename(columns={'@name': 'tab'})
time = time.rename(columns={'@name': 'time'})

# edit text to '201901' from '2019年1月'
time['yyyy'] = time['time'].str.split('年', expand=True)[0]
time['mm'] = time['time'].str.split('年', expand=True)[1].str.strip('月').str.zfill(2)
time['yyyymm'] = time['yyyy'] + time['mm']
# If there is 'A' in the middle, it means 'city'
area['city_flag'] = area['@code'].str.contains('..A..')
area['area'] = area['area'].str.split(' ', expand=True)[1]

# extract only necessary rows before joining
# For details, output it to csv and check it
time = time.where(time['@level'] == '4')
area = area.where(area['city_flag'] == True)

# delete unnecessary columns before joining
area = area.drop(columns=['@level','city_flag'])
category = category.drop(columns=['@level','@parentCode'])
tab = tab.drop(columns=['@level','@unit'])
time = time.drop(columns=['@level','@parentCode','time','yyyy','mm'])

# inner join
joined = data.set_index('@area').join(area.set_index('@code'), how='inner')
joined = joined.set_index('@cat01').join(category.set_index('@code'), how='inner')
joined = joined.set_index('@tab').join(tab.set_index('@code'), how='inner')
joined = joined.set_index('@time').join(time.set_index('@code'), how='inner')

# Query: Cleaning
SQL_TEMPLATE = "DELETE FROM [dbo].[e_Stat]"
editSql = SQL_TEMPLATE
u.ExecuteSQLBySQLServer(editSql)

# Query: Insert
SQL_TEMPLATE = "INSERT INTO [dbo].[e_Stat]([yyyymm],[category],[area],[amount]) VALUES ({0},'{1}','{2}',{3})"
for line in joined.values:
    editSql = SQL_TEMPLATE
    editSql = editSql.replace('{0}',line[4])
    editSql = editSql.replace('{1}',line[2])
    editSql = editSql.replace('{2}',line[1])
    editSql = editSql.replace('{3}',line[0])
    u.ExecuteSQLBySQLServer(editSql)

# Query: Select
SQL_TEMPLATE = "SELECT TOP(30) CONVERT(VARCHAR(6), [yyyymm]) yyyymm, category, area, CONVERT(VARCHAR(10), [amount] ) amount FROM [db].[dbo].[e_Stat]"
editSql = SQL_TEMPLATE
df = u.ReadQueryBySQLServer(editSql)
for line in df.values:
    print(','.join(line))