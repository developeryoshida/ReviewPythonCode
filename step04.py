# python Step04/step04_kurihara_v2.py Step04/input.txt "2022-04-01 00:00:00" "2022-12-30 00:00:00" Boston
import sys
from datetime import datetime
import re

def judge_epoch(date):
    '''
    日時がepoch秒でもYYYY型でもYYYY型に揃える関数

    Parameters
    ------------
    date: int/datetime
        エポック秒またはYYYY型で日時を表す。

    Returns
    ------------
    date: datetime
        YYYY型の日時を表す。
    '''

    if type(date) == int:
    # epoch秒の場合
        date = datetime.fromtimestamp(date)
    else:
    # YYYY-MM-DDでの入力の時
        date = datetime.strptime(date, "%Y-%m-%d %H:%M:%S")

    return date


def get_input_info(argvs):
    '''
    コマンドラインからの引数の情報を取得する関数

    Parameters
    ------------
    file_name: str
        読み込むファイルの名前
    start_input: datetime
        検索時に使う開始日時
    end_input: datetime   
        検索時に使う終了日時
    keywd: str/None
        検索時に使うキーワード(引数がない場合はNone)

    Returns
    ------------ 
    file_name: str
        読み込むファイルの名前
    start_input: datetime
        検索時に使う開始日時
    end_input: datetime   
        検索時に使う終了日時
    keywd: str/None
        検索時に使うキーワード(引数がない場合はNone)

    '''
    
    file_name = argvs[1]
    
    start_input = judge_epoch(argvs[2])
    
    end_input = judge_epoch(argvs[3])

    if len(argvs) == 5:
        keywd = argvs[-1]
    else:    
        keywd = None

    #startとendが逆転してたらエラー
    if str(start_input) > str(end_input):
        print("開始時刻と終了時刻が逆です。", file = sys.stderr)
        sys.exit(1)

    return file_name, start_input, end_input, keywd


def get_file_info(file_name):
    '''
    読み込んだファイルの内容を取得する関数

    Parameters
    ------------
    file_lines: list
        テキストファイルの1行を1つの要素として格納している
    file_texts: list
        一次元目:テキストファイルの1行を1つの要素として格納している
        二次元目:空白区切りで１つの単語を１つの要素として格納している

    Returns
    ------------
    file_lines: list
        テキストファイルの1行を1つの要素として格納している
    file_texts: list
        一次元目:テキストファイルの1行を1つの要素として格納している
        二次元目:空白区切りで１つの単語を１つの要素として格納している

    '''

    try:
        # 改行コードをLFにする
        with open(file_name, 'r', newline = None ) as f:
            # 行ごとに読み込む
            # 空白行は読み込まずにスキップする
            file_lines = list() 
            for i in f.readlines():
                # 連続する２つ以上のスペースは\nに置き換えられる
                i = re.sub('(  )+','\n', i)
                # スペース単体、または２つ以上のスペースだけの行は読み込まれずにスキップされる
                if i == "\n" or i == "\n\n":
                    pass
                else:
                    file_lines.append(i)

            # 「,」がキーワード検索のときに邪魔になるので空白と置換
            for i in range(len(file_lines)):
                file_lines[i] = file_lines[i].replace(',','')

            # 空白区切りで要素としてリストに格納
            file_texts = list()
            for i in file_lines:
                text = i.split()
                file_texts.append(text)
    except:
        print("ファイルの名前が正しくありません。または存在しません", file = sys.stderr)
        sys.exit(1)

    # ファイルの中身がからだったらエラー

    if len(file_lines) == 0:
        print("ファイルの中身が空です", file = sys.stderr)
        sys.exit(1)

    return file_lines, file_texts


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

def matching_ip_list(sorted_file_texts,start_input,end_input):
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
        if str(start_input) <= date and date <= str(end_input):
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

    argvs = sys.argv
    
    if len(argvs) < 4:
        print("引数の数が足りません。", file = sys.stderr)
        return 1
    # ファイル名、開始日時、終了日時、キーワードを取得
    file_name, start_input, end_input, keywd = get_input_info(argvs)

    # 行ごとのファイル内容と、単語ごとのファイルの内容を取得
    file_lines, file_texts = get_file_info(file_name)

    # 整形したファイルの内容と、ipアドレスのみのリストを取得する
    sorted_file_texts, ip_list = arranged_input_data(file_lines, file_texts)

    # 指定の日時が開始日時から終了日時までの範囲に該当するipアドレスのみを格納するリストを取得する
    matched_ip_list = matching_ip_list(sorted_file_texts,start_input,end_input)

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

       

