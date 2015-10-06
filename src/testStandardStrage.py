# coding: UTF-8
import os
import codecs
import datetime
import socket
import lib.setup
import lib.checkFilePath
import lib.countFiles
import lib.checkJIS
import lib.checkRequiredFields
import lib.checkNumericFields
import lib.checkSegmentOrder
import lib.countFields
import lib.getFields

count = 0

#使い方の表示
def printUsage():

    print('printUsage')
    
    return

#処理振り分け
def callFunction():

    global count

    try:

        for root, dirs, files in os.walk(lib.setup.rootDir):
            for file in files:

                #先頭N件のみチェック
                if lib.setup.firstN != -1 and count >= lib.setup.firstN:
                    return

                #file = 0_1_2_3_4_5_6
                #0: 患者ID
                #1: -/診療日
                #2: データ種別
                #3: オーダーNo
                #4: 発生日時
                #5: 診療科コード
                #6: コンディションフラグ
                f = file.split('_')

                #コンディションフラグの制限
                if lib.setup.conditionFlag != '' and lib.setup.conditionFlag != f[6]:
                    continue

                #チェック対象ファイルのパス
                filePath = os.path.join(root, file)

                #チェック対象ファイルの中身
                if lib.setup.callFunction not in ['checkFilePath','countFiles','checkJIS']:
                    f_utf8 = '%s.utf8' % os.getpid()
                    f_utf8 = os.path.join(os.path.abspath(os.path.dirname(__file__)), f_utf8)
                    os.system('nkf -w %s > %s' % (filePath, f_utf8))

                    fin = codecs.open(f_utf8, 'r', 'utf-8')
                    fileStr = fin.read()
                    fin.close()
                    
                if lib.setup.callFunction in ['checkFilePath','checkAll']:
                    lib.checkFilePath.checkFilePath(root, file)

                if lib.setup.callFunction in ['countFiles', 'checkAll']:
                    lib.countFiles.countFiles(file)
                
                if lib.setup.callFunction in ['checkJIS', 'checkAll']:                    
                    lib.checkJIS.checkJIS(filePath)

                if lib.setup.callFunction in ['checkRequiredFields', 'checkAll']:
                    lib.checkRequiredFields.checkRequiredFields(filePath, f[2], fileStr)

                if lib.setup.callFunction in ['checkNumericFields', 'checkAll']:
                    lib.checkNumericFields.checkNumericFields(filePath, fileStr)

                if lib.setup.callFunction in ['checkSegmentOrder', 'checkAll']:
                    lib.checkSegmentOrder.checkSegmentOrder(filePath, f[2], f[6], fileStr)
                    
                if lib.setup.callFunction in ['countFields', 'checkAll']:
                    lib.countFields.countFields(filePath, f[2], fileStr)

                if lib.setup.callFunction in ['getFields', 'checkAll']:
                    lib.getFields.getFields(filePath, f[2], fileStr)
                    
                count += 1

    except Exception as e:
        print(str(e))

    return

#結果出力
def outputResults():

    try:

        if lib.setup.callFunction in ['checkFilePath', 'checkAll']:
            lib.checkFilePath.outputResults(lib.setup.outputFile)

        if lib.setup.callFunction in ['countFiles', 'checkAll']:
            lib.countFiles.outputResults(lib.setup.outputFile)
            
        if lib.setup.callFunction in ['checkJIS', 'checkAll']:
            lib.checkJIS.outputResults(lib.setup.outputFile)

        if lib.setup.callFunction in ['checkRequiredFields', 'checkAll']:
            lib.checkRequiredFields.outputResults(lib.setup.outputFile)

        if lib.setup.callFunction in ['checkNumericFields', 'checkAll']:
            lib.checkNumericFields.outputResults(lib.setup.outputFile)

        if lib.setup.callFunction in ['checkSegmentOrder', 'checkAll']:
            lib.checkSegmentOrder.outputResults(lib.setup.outputFile)
            
        if lib.setup.callFunction in ['countFields', 'checkAll']:
            lib.countFields.outputResults(lib.setup.outputFile)
                    
        if lib.setup.callFunction in ['getFields', 'checkAll']:
            lib.getFields.outputResults(lib.setup.outputFile)

    except Exception as e:
        print(str(e))

def main(argv):

    #python checkStandardStrage
    #[
    #  countFiles |
    #  checkJIS |
    #  checkMessageOrder |
    #  checkNumericFields |
    #  checkRequiredFields |
    #  countFields |
    #  getFields
    #] 
    #-rootDir ディレクトリ #チェックの対象となるディレクトリの名前 必ずしも標準化ストレージのルートディレクトリでなくても構わない
    #[-outputFile ファイル名] #結果を出力するファイルの名前 指定なし/allの時pid.outとなる
    #[-conditionFlag (0|1|2)] #指定したコンディションフラグのみ対象とする 指定なしで全件
    #[-first N] #最初に見つかったN件までチェック対象とする 1以上の数を指定
    #[-field セグメント インデックスリスト] #取得フィールドの指定 getFieldsのみ有効 -field OBX 3,6,7のように指定
    #[-example インデックスリスト] #例示取得フィールドの指定 getFieldsのみ有効 -example 5,6のように指定
    #[-help] #使い方の表示

    global count

    try:
        pwd = os.path.abspath(os.path.dirname(__file__))

        #使い方の表示
        if len(argv) > 1 and argv[1] == '-help':
            printUsage()
            return

        #引数なし
        if len(argv) == 1:
            #iniファイルを参照
            ret = lib.setup.loadStandardIni(os.path.join(pwd, '..', 'etc', 'standard.ini'))

        #引数あり
        else:
            #引数を取得
            ret = lib.setup.getArgv(argv)

        if ret == False:
            printUsage()
            return

        fout = codecs.open(lib.setup.outputFile, 'a', 'utf-8')
        fout.write('%s\r\n' % datetime.datetime.now())
        fout.write('[python %s] @ %s\r\n' % (' '.join(argv), socket.gethostname()))

        #設定を結果ファイルに出力＋プリント
        fout = codecs.open(lib.setup.outputFile, 'a', 'utf-8')
        fout.write('\r\n#####setup#####\r\n')
        fout.write('callFunction: %s\r\n' % lib.setup.callFunction)
        fout.write('rootDir: %s\r\n' % lib.setup.rootDir)
        fout.write('outputFile: %s\r\n' % lib.setup.outputFile)
        fout.write('conditionFlag: %s\r\n' % lib.setup.conditionFlag)
        fout.write('firstN %d\r\n' % lib.setup.firstN)
        if len(lib.setup.getField) != 0:
            fout.write('getFields\r\n')
            for gf in lib.setup.getField:
                fout.write('%s -%s @%s\r\n' % (gf['segmentHeader'], gf['fieldIndex'], gf['exampleIndex']))    
                
        fout.close()

        #セットアップ
        lib.setup.loadIncludeFile(os.path.join(pwd, '..', 'include', 'HL7_SEGMENT.json'),os.path.join(pwd, '..', 'include', 'HL7_DATATYPE.json'),os.path.join(pwd, '..', 'include', 'HL7_SEGMENTORDER.json'))
        
        #処理振り分け
        callFunction()

        #結果出力
        outputResults()

        fout = codecs.open(lib.setup.outputFile, 'a', 'utf-8')
        fout.write('\r\n%d file check complete\r\n' % count)
        fout.write('%s\r\n' % datetime.datetime.now())
        fout.close()

        print('see %s' % lib.setup.outputFile)
        
    except Exception as e:
        print(str(e))
        printUsage()
        
    return

if __name__ == "__main__":
    
    import sys
    
    main(sys.argv)
