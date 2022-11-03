import sys
from datetime import datetime
import re

def to_datatime(str_datetime):
    '''
    str型の日時情報をdatetime型に変換する関数

    Parameters
    ------------
    str_date: str
        エポック秒またはYYYY型で日時を表す。

    Returns
    ------------
    date: datetime
        YYYY型の日時を表す。
    '''

    if str_datetime.isdecimal():
    # epoch秒の場合
        date = datetime.fromtimestamp(int(str_datetime))
    else:
    # YYYY-MM-DDでの入力の時
        date = datetime.strptime(str_datetime, "%Y-%m-%d %H:%M:%S")

    return date

def read_file(filename):
    '''
    読み込んだファイルの内容を取得する関数

    Parameters
    ------------
    filename: str
        読み込み対象のファイル名を指定する

    Returns
    ------------
    file_lines: list
        テキストファイルの1行を1つの要素として格納している
    '''

    file_lines = list()

    # ファイルの空行を排除し、読み込む
    try:
        with open(filename, 'r', encoding = 'utf-8') as f:
            for line in f.readlines():
                if bool(line.strip()):
                    file_lines.append(line.strip())
    except:
        print("ファイルの名前が正しくありません。または存在しません", file = sys.stderr)
        sys.exit(1)

    # ファイルの中身がからだったらエラー
    if len(file_lines) == 0:
        print("ファイルの中身が空です", file = sys.stderr)
        sys.exit(1)

    return file_lines

def filter_log_datetime(log_lines, start_datetime, end_datetime):
    '''
    ファイルを日時情報で絞り込む関数

    Parameters
    ------------
    log_lines: list
        ログのリストデータ
    start_datetime: datetime
        絞り込みの開始時刻
    end_datetime: datetime
        絞り込みの終了時刻
    match_datetime: match
        対象のログに指定のフォーマットの時刻情報が存在しているかを確認したマッチオブジェクト
    log_datetime: datetime
        対象のログの日時情報

    Returns
    ------------
    filter_log_lines: list
        開始時刻と終了時刻の範囲内にあるログのリスト
    '''

    filter_log_lines = list()
    year_info = str(datetime.today().year)

    for line in log_lines:
        match_datetime = re.match('... ([1-9]|[12][0-9]|3[01]) ([01][0-9]|2[0-3]):[0-5][0-9]:[0-5][0-9]', line)
        if match_datetime:
            log_datetime=datetime.strptime(year_info+match_datetime.group(), '%Y%b %d %H:%M:%S')
            # 日時情報が指定の範囲内のログに絞り込む
            if start_datetime < log_datetime < end_datetime:
                filter_log_lines.append(line)

    return filter_log_lines

def fileter_log_keyword(log_lines, keyword):
    '''
    ファイルをキーワードで絞り込む関数

    Parameters
    ------------
    log_lines: list
        ログのリストデータ
    keyword: list
        ログを絞り込む文字列リスト
    match_keyword
        対象のログに指定のキーワードが存在しているかを確認したマッチオブジェクト

    Returns
    ------------
    filter_log_lines: list
        開始時刻と終了時刻の範囲内にあるログのリスト
    '''
    if keyword == None:
        return log_lines

    filter_log_lines = list()

    for line in log_lines:
        match_keyword = re.search(keyword, line)
        if match_keyword:
            filter_log_lines.append(line)

    return filter_log_lines

def count_IP(log_lines):
    '''
    ログのipアドレスを基準にカウント、ソートを行う関数

    Parameters
    ------------
    log_lines: list
        開始時刻と終了時刻の範囲内にあるipアドレスを格納

    Returns
    ------------
    IP_list: list
        開始時刻と終了時刻の範囲内にあるipアドレスを格納
    '''
    IP_list = list()
    IP_count_list = list()

    # ログファイルに存在するIPアドレスのリストを作成する
    for line in log_lines:
        match_IP = re.search('([0-9]{1,3}\.){3}([0-9]{1,3})', line)
        if match_IP:
            IP_list.append(match_IP.group())

    # IPアドレスとその個数のリストを作成する
    for IP in sorted(set(IP_list)):
        IP_count_list.append([IP, IP_list.count(IP)])

    return IP_count_list


def main():
    '''

    ipアドレスの降順になっているファイルの内容が格納されているリストから要素をひとつずつ取り出して条件に合うか確かめて、一致するものだけ出力する関数

    取得したipアドレスと同じものがいくつあるかカウントし、ipアドレスとともに出力する
    指定した日時が開始日時から終了日時までにある行だけを出力する
    キーワード指定がある場合はそのキーワードを含む行のみ出力する

    Parameters
    ------------
    ip: str
        ipアドレスを順番に格納
    other: list
        キーワード検索用に日時とipアドレス以外を格納
    cnt: int
        同一のipアドレスの数を順番に格納
    '''

    args = sys.argv

    if len(args) < 4:
        print("引数の数が足りません。", file = sys.stderr)
        sys.exit(1)

    # ファイル名、開始日時、終了日時、キーワードを取得
    logfile = args[1]
    start_datetime = to_datatime(args[2])
    end_datetime = to_datatime(args[3])

    # start_datetimeとend_datetimeが逆転してたらエラー
    if str(start_datetime) > str(end_datetime):
        print("開始時刻と終了時刻が逆です。", file = sys.stderr)
        sys.exit(1)

    if len(args) == 5:
        keywd = args[-1]
    else:
        keywd = None

    # ファイルの内容を取得
    log_lines = read_file(logfile)

    # ファイルの内容を日時で絞り込む
    filtered_log_datetime = filter_log_datetime(log_lines,start_datetime,end_datetime)

    # キーワードで絞り込む
    filtered_log_keyword = fileter_log_keyword(filtered_log_datetime, keywd)

    # IPアドレスのリストを作成
    log_IP_list = count_IP(filtered_log_keyword)

    # IPアドレスのリストを表示
    for IP, count in log_IP_list:
        print(IP.ljust(14) + ':' + str(count))

    sys.exit(0)


if __name__ == "__main__":
    main()



