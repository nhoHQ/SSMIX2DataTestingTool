# coding: UTF-8
import os
import codecs
import re
import lib.setup

segmentOrder = {}

#セグメントの組み合わせをチェックする
def checkSegmentOrder(filePath, dataType, conditionFlag, fileStr):

    try:
        
        #メッセージ型(MSH-9)を得る
        msgType = ''
        alllines = fileStr.strip().split('\r')
        for line in alllines:
            if line[0:3] == 'MSH':
                tmp = (line + '|' * 8).split('|')[8]
                tmp = (tmp + '^' * 2).split('^')
                msgType = '^'.join([tmp[0],tmp[1]])
                break

        #電文をチェック用に短くする
        checkStr = ''
        previousTag = ''
        for line in alllines:
            if line[0:3] != previousTag:
                checkStr = checkStr + line[0:3]
                previousTag = line[0:3]

        #結果格納の準備
        key = '@@@'.join([dataType, conditionFlag])
        if key not in segmentOrder:
            segmentOrder[key] = {}
            segmentOrder[key]['total'] = 0
            segmentOrder[key]['ok'] = 0
            segmentOrder[key]['ng'] = ''
            
        segmentOrder[key]['total'] = segmentOrder[key]['total'] + 1

        #セグメントの組み合わせをチェックする
        if msgType in lib.setup.HL7_SEGMENTORDER:
            if re.match(lib.setup.HL7_SEGMENTORDER[msgType], checkStr):
                segmentOrder[key]['ok'] = segmentOrder[key]['ok'] + 1
            else:
                segmentOrder[key]['ng'] = filePath
        else:
            print('unknown message type [%s] @ %s' % (msgType, filePath))

    except Exception as e:
        print(str(e))
        
    return

#結果を出力する
def outputResults(outputFile):

    try:

        fout = codecs.open(outputFile, 'a', 'utf-8')
        
        fout.write('\r\n#####checkSegmentOrder result#####\r\n')

        for k,v in sorted(segmentOrder.items()):
            kk = k.split('@@@')
            fout.write('%s - %s: %d / %d\r\n' % (kk[0], kk[1], v['ok'], v['total']))

            if v['ng'] != '':
                fout.write('ng @ %s\r\n' % v['ng'])

            fout.write('\r\n')        

        fout.close()
    
    except Exception as e:
        print(str(e))

    return

if __name__ == "__main__":
    
    import sys
    import codecs
    
    setup()

    fin = codecs.open('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1', 'r', 'utf-8')
    fileStr = fin.read()
    fin.close()

    checkSegmentOrder('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1', 'OMP-11', '1', fileStr)
    
    outputResults('%s.out' % os.getpid())

