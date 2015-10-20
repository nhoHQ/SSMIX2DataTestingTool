# SSMIX2DataTestingTool
SSMIX2DataTestingToolは、各種規約に則りSS-MIX2データをチェックするためのツール群です。

## 実行環境
* python3.x  
python3.4.0で動作を確認しています。
* nkf  
windows機では[こちら](http://www.vector.co.jp/soft/win95/util/se295331.html?ds)で配布されているnkf32.exeで動作を確認しています。

## 使い方
* コマンドライン引数で各種指定をする場合  
  python testStandardStrage.py   
  -callFunction checkFilePath|countFiles|checkJIS|checkCareDate|checkRequiredFields|checkNumericFields|checkSegmentOrder|countFields|getFields  
  -rootDir 標準化ストレージのルートディレクトリ  
  [-outputFile 結果出力ファイルパス]
  [-conditionFlag 0|1|2]  
  [-timeStampStart yyyyMMddHHmmssfff]  
  [-timeStampEnd yyyyMMddHHmmssfff]  
  [-firstN N]  
  [-getField セグメントヘッダ-フィールド,...[@例示取得フィールド,...]]  
  
  []内は省略可能
* iniファイルで各種指定をする場合  
  引数と同様に指定する

## 参照している規約
* SS-MIX2 標準化ストレージ 構成の説明と構築ガイドライン Ver.1.2c
* SS-MIX2 拡張ストレージ 構成の説明と構築ガイドライン Ver.1.2c
* SS-MIX2 標準化ストレージ仕様書 Ver.1.2c データ格納方法およびデータ定義 および、仕様書が参照する以下の規約
    * HL7 Ver.2.5
    * JAHIS 処方データ交換規約 Ver.2.0
    * JAHIS 注射データ交換規約 Ver.1.0
    * JAHIS 臨床検査データ交換規約 Ver.3.1
    * JAHIS 放射線データ交換規約 Ver.2.2
    * JAHIS 病名情報データ交換規約 Ver.3.0C
    * JAHIS 生理検査データ交換規約 Ver.2.0
    * JAHIS 内視鏡データ交換規約 Ver.2.0
    * JAHIS データ交換規約(共通編) Ver.1.0
* SS-MIX2 標準化ストレージ仕様書 Ver.1.2c 別紙：コード表

### etcフォルダ  
* standard.ini  
標準化ストレージをチェックするための設定ファイルです。

### includeフォルダ
* HL7_DATATYPE.json  
HL7のデータ型を定義しています。基本型には文字列型(str)か数値型(num)かを、複合型には各成分の名称とデータ型を定義しています。  
基本的にJAHISデータ交換規約(共通編)ver.1.0を参照し定義しています。共通編に定義がないものは、それぞれ次のように定義しています。
    * AD型(LA1型に出現)はHL7 ver2.5を参照し定義しています。
    * CE型(TQ型に出現)はHL7 ver2.5を参照し定義しています。
    * TQ型(ORC-7、RXE-1、OBR-27に出現)はHL7 ver2.5を参照し定義しています。
    * ZRD型(ZE1-9に出現)はJAHIS内視鏡データ交換規約Ver.2.2を参照し定義しています。

* HL7_SEGMENT.json  
HL7のセグメントを定義しています。ssmix2-requiredは『"OML-01":"R", "OML-11":"R", "\*":N』のようにデータ種別ごとにオプション指定を定義しています。これは、OML-01とOML-11の時はR、**それ以外の時**はNと読んでください。基本的にHL7 Ver.2.5を参照し定義しています。HL7 Ver.2.5に定義がないものは、それぞれ次のように定義しています。
    * ZE1セグメント(OMI^Z33に出現)はJAHIS放射線データ交換規約Ver.2.2、およびJAHIS内視鏡データ交換規約Ver.2.2を参照して定義しています。
    * ZE2セグメント(OMI^Z33に出現)はJAHIS放射線データ交換規約Ver.2.2を参照して定義しています。
    * ZPDセグメント(PPR^ZD1に出現)はJAHIS病名情報データ交換規約Ver.3.0Cを参照して定義しています。

* HL7_SEGMENTORDER.json  
HL7のメッセージ型ごとに、セグメント構成を定義しています。

* SSMIX_CAREDATE.json  
HL7のメッセージ型ごとに、SS-MIX2の診療日に対応するフィールドを定義しています。

### srcフォルダ
* testStandardStrage.py...後述のlibフォルダ内の関数を呼び出し、標準化ストレージの各種チェックを行います。
* libフォルダ...チェックを行うための関数群を格納しています。
    * setup.py ...定義や設定を読み込みます。
    * checkFilePath.py...ファイルパスをチェックします。
    * countFiles.py...ファイルをデータ種別等ごとに数えます。
    * checkJIS.py...ファイル内のデータがJISX0208で出力されているかをチェックします。
    * checkCareDate.py...ファイルパスとファイル内の診療日が一致しているかをチェックします。
    * checkRequiredFields.py...必須箇所に空欄がないかチェックします。
    * checkNumericFields.py...NM型のフィールドに数値以外の出力がないかチェックします。
    * checkSegmentOrder.py...セグメント構成をチェックします。
    * countFields.py...何らかの出力があるフィールドを数えます。
    * getFields.py...指定したフィールドを一意に抽出します。

### sampleDataフォルダ
サンプルファイルを置いています。多くはSS-MIX2 標準化ストレージ 構成の説明と構築ガイドライン Ver.1.2cに掲載されているサンプル電文です。

## ライセンス
このリポジトリに含まれるコードはApache License 2.0に従って配布しています。
