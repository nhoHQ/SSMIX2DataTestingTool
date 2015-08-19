# SSMIX2DataTestingTool
SSMIX2DataTestingToolは、各種規約に則りSS-MIX2データをチェックするためのツール群です。

# 参照している規約
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

# includeフォルダ
* HL7_DATATYPE.json
HL7のデータ型を定義しています。基本型には文字列型(str)か数値型(num)かを、複合型には各成分の名称とデータ型を定義しています。

* HL7_SEGMENT.json
HL7のセグメントを定義しています。

* HL7_SEGMENTORDER.json
HL7のメッセージ型ごとに、セグメント構造を定義しています。

# srcフォルダ

# ライセンス
このリポジトリに含まれるコードはApache License 2.0に従って配布しています。
