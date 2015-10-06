# coding: UTF-8
import codecs
import os
import lib.setup as setup
#import setup #for debug

requiredNg = {}

def checkRequiredFields(filePath, dataType, fileStr):

    try:
            
        alllines = fileStr.strip().split('\r')
        for line in alllines:
            header = line[0:3]

            #MSH-1は自身がフィールド区切りなので後の処理のためにNULLフィールドを１つ入れておく
            if header == 'MSH':
                line = '|""'.join([line[:3],line[3:]])

            if header in setup.HL7_SEGMENT:

                #各フィールド
                fields = (line + '|' * len(setup.HL7_SEGMENT[header])).split('|')
                for i in range(1, len(setup.HL7_SEGMENT[header])):

                    #SS-MIX2としての必須/非必須
                    ssmix2_required = setup.HL7_SEGMENT[header][i]['ssmix2-required']

                    #当該データ種別に指定がある
                    if dataType in ssmix2_required:
                        r = ssmix2_required[dataType]

                    #当該データ種別に指定がない、もしくは全て共通
                    else:
                        r = ssmix2_required['*']

                    #必須箇所がカラ
                    if r == 'R' and fields[i] == '':

                        key = '@@@'.join([dataType, header, str(i)])

                        if key in requiredNg:
                            requiredNg[key]['count'] = requiredNg[key]['count'] + 1
                            requiredNg[key]['file'] = filePath

                        else:
                            requiredNg[key] = {}
                            requiredNg[key]['count'] = 1
                            requiredNg[key]['file'] = filePath
                
            else:
                print('unknown segment [%s] @ %s' % (header, filePath))

    except Exception as e:
        print(str(e))
        
    return

#結果を出力する
def outputResults(outputFile):

    try:

        fout = codecs.open(outputFile, 'a', 'utf-8')

        fout.write('\r\n#####checkRequiredField result#####\r\n')
        fout.write('%d fields failure\r\n\r\n' % len(requiredNg))

        for k,v in sorted(requiredNg.items()):
            key = k.split('@@@')
            fout.write('%s %s-%s %d %s\r\n' % (key[0], key[1], key[2], v['count'], v['file']))

        fout.write('\r\n')

        fout.close()
        
    except Exception as e:
        print(str(e))

    return

if __name__ == "__main__":
    
    import sys
    import codecs
    
    setup.loadIncludeFile(os.path.join('..','..','include','HL7_SEGMENT.json'),os.path.join('..','..','include','HL7_DATATYPE.json'),os.path.join('..','..','include','HL7_SEGMENTORDER.json'))

    fin = codecs.open('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1', 'r', 'utf-8')
    fileStr = fin.read()
    fin.close()

    checkRequiredFields('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1', 'OMP-11', fileStr)
    
    outputResults('%s.out' % os.getpid())


