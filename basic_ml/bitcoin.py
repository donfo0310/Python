import pandas as pd
btc_price = pd.read_csv(r'data\coindesk-bpi-USD-close_data-2018-06-07_2018-06-27.csv')

btc_price.head()

# indexが1ズレたデータを持っている
# そうすることで、1時間後の値、という教師になることができる
X = btc_price.loc[0:500, ["Close Price"]]
y = btc_price.loc[1:501, ["Close Price"]]

# データを訓練データとテストデータに分ける
# 時系列でデータが並んでいるため、train_test_split() は使いません。
# 単純に500件あるうちの先頭400件を訓練データ、後ろ100件をテストデータとします。
import numpy as np
X_train = np.array(X[:400])
X_test  = np.array(X[400:])
y_train = np.array(y[:400])
y_test  = np.array(y[400:])

# make the model as regression
from sklearn import linear_model
model = linear_model.LinearRegression()
model.fit(X_train, y_train)

# make the predict
y_pred = model.predict(X_test)

print(y_pred)