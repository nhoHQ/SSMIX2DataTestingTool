# coding: UTF-8
import os
import codecs
import re
import json

callFunction = '' #呼ぶ関数

rootDir = '' #チェック対象となるディレクトリ
outputFile = '' #チェック結果出力ファイル
conditionFlag = '' #チェック対象となるコンディションフラグ
firstN = -1 #チェック対象となるファイル数
getField = [] #getFieldsで取得対象となるセグメント、フィールド、例示取得対象となるフィールド

HL7_SEGMENT = {} #セグメントの定義
HL7_DATATYPE = {} #データ型の定義
HL7_SEGMENTORDER = {} #セグメントの順序・繰り返しの定義

#iniファイルの読み込み
def loadStandardIni(iniFile):

    ret = False

    global callFunction
    global rootDir
    global outputFile
    global conditionFlag
    global firstN
    global getField
    
    try:
        
        fin = codecs.open(iniFile,'r','utf-8')
        
        for line in fin.read().split('\r\n'):
            
            #[-項目]:内容 #コメント
            l = re.match('.*\[(.*)\]:(.*)(#?.*)',line)
            
            if l != None:
                item = l.groups(0)[0]

                #呼ぶ関数
                if item == '-callFunction':
                    callFunction = l.groups(0)[1].strip()

                #チェック対象となるディレクトリ
                if item == '-rootDir':
                    rootDir = l.groups(0)[1].strip()

                #チェック結果出力ファイル
                if item == '-outputFile':
                    outputFile = l.groups(0)[1].strip()

                #チェック対象となるコンディションフラグ
                if item == '-conditionFlag':
                    conditionFlag = l.groups(0)[1].strip()

                #チェック対象となるファイル数
                if item == '-firstN':
                    if l.groups(0)[1].strip() == '':
                        firstN = -1
                    else:
                        firstN = int(l.groups(0)[1].strip())
                        
                #getFieldsで取得対象となるセグメント、フィールド、例示取得対象となるフィールド
                #OBX-3,6,7@5
                if item == '-getField':
                    tmp = l.groups(0)[1].strip().split('-')

                    #セグメント
                    segment = tmp[0]

                    #フィールド
                    tmp_field = tmp[1].split('@')[0].split(',')
                    for i in range(len(tmp_field)):
                        tmp_field[i] = int(tmp_field[i])

                    #サンプル
                    tmp_sample = []
                    if len(tmp[1].split('@')) == 2:
                        tmp_sample = tmp[1].split('@')[1].split(',')
                        for i in range(len(tmp_sample)):
                            tmp_sample[i] = int(tmp_sample[i])

                    getField.append({'segmentHeader':segment, 'fieldIndex':tmp_field, 'exampleIndex':tmp_sample})

        fin.close()

        print('callFunction: %s' % callFunction)
        print('rootDir: %s' % rootDir)
        print('outputFile: %s' % outputFile)
        print('conditionFlag: %s' % conditionFlag)
        print('firstN %d' % firstN)
        print('getFields')
        for gf in getField:
            print('%s -%s @%s' % (gf['segmentHeader'], gf['fieldIndex'], gf['exampleIndex']))

        ret = True
        
    except Exception as e:
        print(str(e))

    return ret

#引数の取得
def getArgv(argv):

    ret = False

    global callFunction
    global rootDir
    global outputFile
    global conditionFlag
    global firstN
    global getField

    try:

        #呼ぶ関数
        callFunction = argv[1]

        for i in range(2,len(argv)):

            #チェック対象となるディレクトリ
            if argv[i] == '-rootDir':
                rootDir = argv[i+1]

            #チェック結果出力ファイル
            if argv[i] == '-outputFile':
                outputFile = argv[i+1]

            #チェック対象となるコンディションフラグ
            if argv[i] == '-conditionFlag':
                conditionFlag = argv[i+1]

            #チェック対象となるファイル数
            if argv[i] == '-firstN':
                firstN = int(argv[i+1])

            #getFiledsで取得対象となるセグメント、フィールド、例示取得対象となるフィールド
            #OBX-3,6,7@5
            if argv[i] == '-getField':
                tmp = argv[i+1].split('-')

                #セグメント
                segment = tmp[0]

                #フィールド
                tmp_field = tmp[1].split('@')[0].split(',')
                for i in range(len(tmp_field)):
                    tmp_field[i] = int(tmp_field[i])

                #サンプル
                tmp_sample = []
                if len(tmp[1].split('@')) == 2:
                    tmp_sample = tmp[1].split('@')[1].split(',')
                    for i in range(len(tmp_sample)):
                        tmp_sample[i] = int(tmp_sample[i])

                getField.append({'segmentHeader':segment, 'fieldIndex':tmp_field, 'exampleIndex':tmp_sample})
                
        ret = True

    except Exception as e:

        print(str(e))

    return ret

#定義の読み込み
def loadIncludeFile(f_segment, f_dataType, f_segmentOrder):

    ret = False

    global HL7_SEGMENT
    global HL7_DATATYPE
    global HL7_SEGMENTORDER 
    
    try:
        
        ret = True

        fin = codecs.open(f_segment, 'r', 'utf-8')
        HL7_SEGMENT = json.load(fin)
        fin.close()

        #ZI1はIN1と同じ 定義ファイルに同じ内容を書くか悩む
        HL7_SEGMENT['ZI1'] = HL7_SEGMENT['IN1']

        fin = codecs.open(f_dataType, 'r', 'utf-8')
        HL7_DATATYPE = json.load(fin)
        fin.close()

        fin = codecs.open(f_segmentOrder, 'r', 'utf-8')
        HL7_SEGMENTORDER = json.load(fin)
        fin.close()
        
    except Exception as e:
        print(str(e))
    
    return ret

if __name__ == "__main__":
    
    import sys
    
    loadStandardIni(os.path.join('..','..','etc','standard.ini'))