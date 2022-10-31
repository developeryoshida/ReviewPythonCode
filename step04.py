from cmath import log
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

def filter_log(log_lines, start_datetime, end_datetime):
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

#def matching_ip_list(sorted_file_texts,start_datetime,end_datetime):
#    '''
#    ipアドレス基準でソート済みのテキストから指定の日時に合致するipアドレスを抽出する関数
#
#    Parameters
#    ------------
#    matched_ip_list: list
#        開始時刻と終了時刻の範囲内にあるipアドレスを格納
#    date: str
#        日時を順番に格納
#    ip: str
#        ipアドレスを順番に格納
#
#    Returns
#    ------------
#    matched_ip_list: list
#        開始時刻と終了時刻の範囲内にあるipアドレスを格納
#    '''
#
#    matched_ip_list = list()
#
#    for i in range(len(sorted_file_texts)):
#        date, ip = sorted_file_texts[i][0],sorted_file_texts[i][1]
#        if str(start_datetime) <= date and date <= str(end_datetime):
#            matched_ip_list.append(ip)
#
#    return matched_ip_list


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

    #sstart_datetimeとend_datetimeが逆転してたらエラー
    if str(start_datetime) > str(end_datetime):
        print("開始時刻と終了時刻が逆です。", file = sys.stderr)
        sys.exit(1)

    if len(args) == 5:
        keywd = args[-1]
    else:
        keywd = None

    # ファイルの内容を取得
    file_lines = read_file(logfile)

    # ファイルの内容を日時で絞り込む
    filetered_log = filter_log(file_lines,start_datetime,end_datetime)

#    # 指定の日時が開始日時から終了日時までの範囲に該当するipアドレスのみを格納するリストを取得する
#    matched_ip_list = matching_ip_list(sorted_file_texts,start_datetime,end_datetime)
#
#    # ソート済みのipアドレス
#    for i in range(len(matched_ip_list)):
#        # 開始時刻と終了時刻に合致するipを順番に取得
#        ip = matched_ip_list[i]
#        # 日時とipアドレス以外をその他としてキーワード検索に使う
#        other = sorted_file_texts[i][2:]
#
#        # 同じipアドレスがいつくあるかカウント
#        # 重複しないために同じipアドレスは一度しかカウントされない（一度カウントされたアドレスは２度目以降０としてカウントされる）
#        cnt = 0
#        for j in matched_ip_list:
#            if not ip in matched_ip_list[:i]:
#                if ip == j:
#                    cnt += 1
#
#        # ipアドレスをその数と一緒に出力する
#        # キーワードが指定されている場合はキーワードを含むもののみ出力する
#        if cnt >= 1:
#            # キーワード指定なしの場合
#            if keywd == None:
#                    print(ip,":", cnt)
#            # キーワード指定ありの場合
#            else:
#                if keywd in other:
#                    print(ip,":", cnt)
#
    sys.exit(0)


if __name__ == "__main__":
    main()



