import sys
from datetime import datetime
import re

def to_datatime(input_datetime):
    '''
    str型の日時情報をdatetime型に変換する関数

    Parameters
    ------------
    input_date: str
        エポック秒またはYYYY型で日時を表す。

    Returns
    ------------
    date: datetime
        YYYY型の日時を表す。
    '''

    if input_datetime.isdecimal():
    # epoch秒の場合
        date = datetime.fromtimestamp(int(input_datetime))
    else:
    # YYYY-MM-DDでの入力の時
        date = datetime.strptime(input_datetime, "%Y-%m-%d %H:%M:%S")

    return date

def read_file(filename):
    '''
    読み込んだファイルの内容を取得する関数

    Parameters
    ------------
    file_lines: list
        テキストファイルの1行を1つの要素として格納している

    Returns
    ------------
    file_lines: list
        テキストファイルの1行を1つの要素として格納している

    '''

    file_lines = list() 
    try:
        with open(filename, 'r', encoding='utf-8') as f:
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

def arranged_input_data(file_lines, file_texts):
    '''
    読み込んだファイルの情報を整形する関数

    月を数字に揃える(例　Janを1にする)
    年の情報がないので2022とする
    ipアドレスの降順に出力するのでipアドレスをキーとして辞書型のデータを作成する

    Parameters
    ------------
    months: list
        初めの要素は空白で英語の短縮表記の月名が格納されている。インデックス番号と月名が一致する。
    ip_list: list
        ipアドレスのみのリスト
    date_list: list
        日時のみのリスト
    others: list
        テキストからipアドレスと日時を抜いたデータ。キーワード検索の検索対象になる
    arrenged_texts: list
        整形したテキストを再度合わせたデータ(ipアドレス、整形した日時、その他の順) 
    log: dict
        key: ip_list
        value: arrenged_texts
        ipアドレスをキーとした辞書型データ
    sorted_log: list
        logをkeyであるipアドレスの降順に並び替えたデータ


    Returns
    ------------
    sorted_log: list
        logをkeyであるipアドレスの降順に並び替えたデータ
    ip_list: list

    '''

    # 月を数字にそろえる
    months = (' ','Jan', 'Feb', 'Mar', 'Apr',
           'May', 'Jun', 'Jul', 'Aug',
           'Sep', 'Oct',  'Nov', 'Dec' )

    for i in range(len(file_lines)):
        for j in range(1,13): #1~12のjが月と一致
            if file_texts[i][0] == months[j]:
                file_texts[i][0] = str(j) 

    # ファイルの日時を抽出して、YYYY型に整形する
    date_list = list()
    for i in file_texts: 
        if len(i[0]) == 1 and len(i[1]) == 1: 
            date_list.append("2022" + "-" + "0" + i[0] + "-" + "0" + i[1] + " " + i[2] )
        elif len(i[0]) == 2 and len(i[1]) == 1: 
            date_list.append("2022" + "-" + i[0] + "-" + "0" + i[1] + " " + i[2] )
        elif len(i[0]) == 1 and len(i[1]) == 2:
            date_list.append("2022" + "-" + "0" + i[0] + "-" + i[1] + " " + i[2] )    
        else:
            date_list.append("2022" + "-" + i[0] + "-" + i[1] + " " + i[2] )  

    # date_listをfile_textsに戻す
    for i in range(len(file_texts)):
        del file_texts[i][0:3]
        file_texts[i].insert(0,date_list[i])
    
    # リストの1番目の要素（ipアドレス）を基準に並び替える
    sorted_file_texts = sorted(file_texts, reverse = False, key = lambda x:x[1]) 

    # ipアドレスのみ格納するリストの作成
    ip_list = list()
    for i in sorted_file_texts :
        ip_list.append(i[3])

    return sorted_file_texts, ip_list

def matching_ip_list(sorted_file_texts,start_datetime,end_datetime):
    '''
    ipアドレス基準でソート済みのテキストから指定の日時に合致するipアドレスを抽出する関数

    Parameters
    ------------
    matched_ip_list: list
        開始時刻と終了時刻の範囲内にあるipアドレスを格納
    date: str
        日時を順番に格納
    ip: str
        ipアドレスを順番に格納

    Returns
    ------------
    matched_ip_list: list
        開始時刻と終了時刻の範囲内にあるipアドレスを格納
    '''

    matched_ip_list = list()
    
    for i in range(len(sorted_file_texts)):
        date, ip = sorted_file_texts[i][0],sorted_file_texts[i][1]
        if str(start_datetime) <= date and date <= str(end_datetime):
            matched_ip_list.append(ip)

    return matched_ip_list


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
    file_name = args[1]
    start_datetime = toDatatime(args[2])
    end_datetime = toDatatime(args[3])
    
    #sstart_datetimeとend_datetimeが逆転してたらエラー
    if str(start_datetime) > str(end_datetime):
        print("開始時刻と終了時刻が逆です。", file = sys.stderr)
        sys.exit(1)

    if len(args) == 5:
        keywd = args[-1]
    else:    
        keywd = None

    # 行ごとのファイル内容と、単語ごとのファイルの内容を取得
    file_lines, file_texts = get_file(file_name)

    # 整形したファイルの内容と、ipアドレスのみのリストを取得する
    sorted_file_texts, ip_list = arranged_input_data(file_lines, file_texts)

    # 指定の日時が開始日時から終了日時までの範囲に該当するipアドレスのみを格納するリストを取得する
    matched_ip_list = matching_ip_list(sorted_file_texts,start_datetime,end_datetime)

    # ソート済みのipアドレス
    for i in range(len(matched_ip_list)):
        # 開始時刻と終了時刻に合致するipを順番に取得
        ip = matched_ip_list[i]
        # 日時とipアドレス以外をその他としてキーワード検索に使う
        other = sorted_file_texts[i][2:]
        
        # 同じipアドレスがいつくあるかカウント
        # 重複しないために同じipアドレスは一度しかカウントされない（一度カウントされたアドレスは２度目以降０としてカウントされる）
        cnt = 0
        for j in matched_ip_list:
            if not ip in matched_ip_list[:i]:
                if ip == j:
                    cnt += 1

        # ipアドレスをその数と一緒に出力する
        # キーワードが指定されている場合はキーワードを含むもののみ出力する
        if cnt >= 1:
            # キーワード指定なしの場合
            if keywd == None:
                    print(ip,":", cnt)
            # キーワード指定ありの場合    
            else:
                if keywd in other:
                    print(ip,":", cnt)
    
    sys.exit(0)
                          
   
if __name__ == "__main__":
    main()

       

