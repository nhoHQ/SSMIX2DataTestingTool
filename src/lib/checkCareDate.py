# coding: UTF-8
import codecs
import os
import re
import lib.setup as setup
#import setup #for debug

careDateNg = {}

#診療日とそれに対応するフィールドが一致しているかチェックする
def checkCareDate(filePath, fileDate, conditionFlag, dataType, fileStr):

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

        #診療日に対応するフィールドを得る
        dateSegment = ''
        dateIndex = -1
        if msgType in setup.SSMIX_CAREDATE:
            tmp = setup.SSMIX_CAREDATE[msgType].split('-')

            if len(tmp) == 2:
                dateSegment = tmp[0]
                dateIndex = int(tmp[1])
        else:
            print('unknown message type [%s] @ %s' % (msgType, filePath))

        #結果格納の準備
        key = '@@@'.join(['%s %s(%s-%d)' % (dataType, msgType, dateSegment, dateIndex), conditionFlag])
        if key not in careDateNg:
            careDateNg[key] = {}
            careDateNg[key]['total'] = 0
            careDateNg[key]['ok'] = 0
            careDateNg[key]['ngFile'] = ''
            careDateNg[key]['ngDate'] = ''
                
        careDateNg[key]['total'] = careDateNg[key]['total'] + 1

        #診療日をチェックする
        segmentCount = 0
        matchCount = 0
        date = ''
        if dateSegment != '':
            for line in alllines:
                if line[0:3] == dateSegment:
                    segmentCount += 1
                    
                    #時分以下があったら切る
                    date = (line + '|' * dateIndex).split('|')[dateIndex]
                    if len(date.strip()) >= 8:
                        date = date[0:8]

                    if fileDate == date:
                        matchCount += 1
                        
        #結果の格納
        #セグメントが出現しなかった
        if segmentCount == 0:
            careDateNg[key]['ngFile'] = filePath
            careDateNg[key]['ngDate'] = 'None'

        #全てのセグメントで一致した
        elif segmentCount == matchCount:
            careDateNg[key]['ok'] += 1

        #セグメントが出現したが、一部もしくは全ての日付が診療日と一致しなかった        
        elif segmentCount != matchCount:
            careDateNg[key]['ngFile'] = filePath
            careDateNg[key]['ngDate'] = date
    except Exception e:
        print(str(e))
        
    return

#結果を出力する
def outputResults(outputFile):

    try:

        fout = codecs.open(outputFile, 'a', 'utf-8')
        
        fout.write('\r\n#####checkDateTime result#####\r\n')

        for k,v in sorted(careDateNg.items()):
            kk = k.split('@@@')
            fout.write('%s - %s: %d / %d\r\n' % (kk[0], kk[1], v['ok'], v['total']))

            if v['ngFile'] != '':
                fout.write('%s @ %s\r\n' % (v['ngDate'], v['ngFile']))

            fout.write('\r\n')        

        fout.close()
    
    except Exception as e:
        print(str(e))

if __name__ == "__main__":

    import sys
    import codecs
    
    setup.loadIncludeFile_CAREDATE(os.path.join('..','..','include','SSMIX_CAREDATE.json'))
    
    fin = codecs.open('..\\..\\sampleData\\999\\901\\9999013\\20110630\\OMP-11\\9999013_20110630_OMP-11_123456789012345_20110701113813225_01_1', 'r', 'utf-8')
    fileStr = fin.read()
    fin.close()

    checkCareDate('..\\..\\sampleData\\999\\901\\9999013\\20110630\\OMP-11\\9999013_20110630_OMP-11_123456789012345_20110701113813225_01_1', '20110630', '1', 'OMP-11', fileStr)
    
    outputResults('%s.out' % os.getpid())
