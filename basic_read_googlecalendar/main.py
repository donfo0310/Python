import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import lib.PyUtils
import pandas as pd

# If modifying these scopes, delete the file token.pickle.
# SCOPESを変える必要があるときは 'token.pickle' を消してね（すぐ下で初回認証時に勝手に作られるファイル）
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    10日先の予定を表示する
    """
    # The file 'token.pickle' stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
    # 'token.pickle' は初回認証時に勝手に作られる。
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    # If there are no (valid) credentials available, let the user log in.
    # 利用可能な（有効な）認証情報がない場合は、ユーザーにログインさせます。
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            # 認証情報アリ
            creds.refresh(Request())
        else:
            # 認証情報ナシ（credentials.jsonから作成する）
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        # 認証情報を保存する
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Call the Calendar API
    # Google カレンダーでは、夏時間による問題を回避するため、協定世界時（UTC）を採用しています。
    # 作成した予定は UTC に変換されますが、常にそのユーザーの現地時刻で表示されます。
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                        maxResults=10, singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    df = pd.DataFrame(index=[], columns=['ymdhms', 'summary'])
    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        series = pd.Series([lib.PyUtils.ConvertIso2YMDHMS(start), event['summary']], index=df.columns)
        df = df.append(series, ignore_index = True)

    # データ削除クエリを発行
    SQL_TEMPLATE = "DELETE FROM [dbo].[Calendar]"   # SQL原本
    editSql = SQL_TEMPLATE                          # SQL原本に置換をかける
    lib.PyUtils.ExecuteSQLBySQLServer(editSql)      # DELETE文の発行

    # データ追加クエリを発行
    SQL_TEMPLATE = "INSERT INTO [dbo].[Calendar]([ymdhms],[summary]) VALUES ('{0}','{1}')"
    for line in df.values:
        editSql = SQL_TEMPLATE                      # SQL原本
        for i,col in enumerate(line):               # SQL原本に置換をかける
            editSql = editSql.replace('{' + str(i) + '}', col)
        lib.PyUtils.ExecuteSQLBySQLServer(editSql)  # INSERT文の発行

    # 選択クエリを発行
    SQL_TEMPLATE = "SELECT FORMAT(A.ymdhms,'yyyy-MM-dd HH:mm') AS ymdhms, A.summary FROM [dbo].[Calendar] AS A" # SQL原本
    editSql = SQL_TEMPLATE                          # SQL原本に置換をかける
    df = lib.PyUtils.ReadQueryBySQLServer(editSql)  # SELECT文の発行
    for line in df.values:
        print(','.join(line))                       # SQL結果を調理して提供

if __name__ == '__main__':
    main()