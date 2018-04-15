# getbtcdatafrombitflyer
bitflyerからデータ取得開始日と終了日を指定してBTCデータを保存したりHLOCデータへ変換したり描画したりするスクリプトです。 <br>

# Requirements
`pip install pandas` <br>
`pip install progressbar2` <br>

# Usage
## getbtc.py
bitflyerからデータ取得開始日と終了日を指定してBTCデータを保存するスクリプトです。 <br>

 <br>
 
プロジェクト直下に`data`ディレクトリと`log`ディレクトリを作成してください。 <br>
それぞれ取得したデータとログが出力されます。 <br>

例えば、下記コマンドで実行します。 <br>

`python src/getbtc.py -s 2018-01-01-00:00:00 -f 2018-04-11-23:14:00` <br>

`-d`でデータ取得開始日を指定します。 <br>
`-f`はデータ取得終了日を指定できます。 <br>

上記のコマンドを実行することで2018年に入った瞬間から2018年4月11日23時14分までのデータを取得することができます。 <br>
終了日の方は「~分」の部分は含みません。 <br>
`-f 2018-04-11-23:14:00`という引数は23時13分台のデータが最後になります. <br>

また、終了日の引数`-f`は省略することが可能です。 <br>
省略した場合は開始日から実行時の日付（時間）までのデータを取得します。 <br>
例えば、<br>

 <br>
 
`python src/getbtc.py -s 2018-01-01-00:00:00` <br>

<br>

とすることで2018年に入ってから現在までのデータを取得することができます（４月１０日時点で約1.4GBほど）。 <br>

 <br>
 
`YYYY-MM-DD-HH-MM-SS`の形式ですが秒はどんな数字を入れても00として変換されます。 <br>

 <br>
 
一番古い日付で`2015-06-24 05:58:00`なので、これ以前を渡すとエラーが出ます。 <br>

 <br>
 
出力結果のファイルは一つのファイルで50万行約50MBに設定してあります。 <br>
必要に応じて変更してください。 <br>

## generatehloc.py
`getbtc.py`で取得したデータを指定した時間軸のHLOC（高値、安値、始値、終値）へ変換し保存するスクリプトです。出来高も保存されます。 <br>

<br>

プロジェクト直下に`log`ディレクトリ、`hloc`ディレクトリを作成してください。 <br>
`/hloc/`に変換後のデータが保存されます。 <br>
(注)`data`ディレクトリ直下に`hloc`ディレクトリを作成するとエラーが出るので気をつけてください。 <br>
<br>
下記コマンドで実行します。 <br>
 <br>
`python src/generatehloc.py -d ./data -t one_minute` <br>
 <br>
`-d`で変換させるファイルを含むディレクトリを指定します。 <br>
このディレクトリに含まれているファイルを一つずつ全てを読み込みHLOCへ変換します。 <br>
変換結果は読み込んだファイルが複数だとしても、50万行までは一つのファイルにまとめて出力されます。<br>

`-t`はHLOCへ変換する時間軸を指定できます。 <br>
<br>
上記コマンドでは、`data`ディレクトリに含まれているファイルを読み込み1分足に変換後、'/hloc/'へファイルが出力されます。 <br>

<br>

現バージョンでは、1分足、1時間足、日足が指定できます。 <br>
それぞれ、下記のようにしてください。 <br>
<br>

| 時間軸        | 指定方法          |
| --------------- |---------------|
| 1分足 | one_minute |
| 1時間足 | one_hour |
| 日足 | one_day |

## plotchart.py
引数で指定されたHLOCファイルを読み込み、描画するモジュールです。<br>
あまり使い所はありませんが、HLOCに変換したデータの確認等にお使いください。<br>

下記コマンドで実行します。 <br>
 <br>
`python ./src/plotchart.py -f ./hloc/hloc_one_day_2018-01-01-00:00:00_2018-04-09-00:00:00.csv` <br>
 <br>
`-f`でファイルのパスを指定します。<br>
上記のようにすることで、`generatehloc.py`で日足に変換し`hloc`ディレクトリに保存されているファイルを描画することができます。 <br>

## 参考
http://www.madopro.net/entry/bitcoin_chart



