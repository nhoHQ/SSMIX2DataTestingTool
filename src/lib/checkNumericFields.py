# coding: UTF-8
import codecs
import os
import re
import lib.setup as setup
#import setup #for debug

numericNg = []

#数値の判定
def checkNM(data):

    flag = True

    try:

        if data == '' or data == '""':
            flag = True

        else:
            flag = bool(re.compile("^(\-|\+)?\.?\d+\.?\d*\Z").match(data))

    except Exception as e:
        print("Unexpected error : ", sys.exc_info()[0])
        print(data)

    return flag

#NM型のフィールド・成分・副成分が数値かどうかチェックする
def checkNumericFields(filePath, fileStr):

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

                    #フィールドの型
                    fieldType = setup.HL7_SEGMENT[header][i]['type']

                    #OBX-5の型はOBX-2に定義されている
                    if header == 'OBX' and i == 5 and fieldType == '*':
                        if fields[2] == 'NM' and checkNM(fields[5]) == False:
                            numericNg.append('OBX-5: %s @ %s' % (fields[5], filePath))

                    #基本型
                    elif isinstance(setup.HL7_DATATYPE[fieldType], str) == True:
                        if setup.HL7_DATATYPE[fieldType] == 'num' and checkNM(fields[i]) == False:
                            numericNg.append('%s-%d: %s @ %s' % (header, i, fields[i], filePath))
                            
                    #拡張型
                    else:

                        #各成分
                        components = (fields[i] + '^' * len(setup.HL7_DATATYPE[fieldType])).split('^')
                        for j in range(0, len(setup.HL7_DATATYPE[fieldType])):

                            #成分の型
                            componentType = setup.HL7_DATATYPE[fieldType][j]['type']

                            #基本型
                            if isinstance(setup.HL7_DATATYPE[componentType], str) == True:
                                if setup.HL7_DATATYPE[componentType] == 'num' and checkNM(components[j]) == False:
                                    numericNg.append('%s-%d-%d: %s @ %s' % (header, i, j, components[j], filePath))

                            #拡張型
                            else:

                                #各副成分
                                subComponents = (components[j] + '&' * len(setup.HL7_DATATYPE[componentType])).split('&')
                                for k in range(0, len(setup.HL7_DATATYPE[componentType])):

                                    #副成分の型
                                    subComponentType = setup.HL7_DATATYPE[componentType][k]['type']

                                    #基本型
                                    if isinstance(setup.HL7_DATATYPE[subComponentType], str) == True:
                                        if setup.HL7_DATATYPE[subComponentType] == 'num' and checkNM(subComponents[j]) == False:
                                            numericNg.append('%s-%d-%d-%d: %s @ %s' % (header, i, j, k, subComponents[k], filePath))

                                    #拡張型…がなぜここに存在するんだろう？副成分を割るデリミタなんてあるの？
                                    else:
                                        print('%s-%d-%d-%d: %s' %(header,i,j,k,subComponentType))

            else:
                print('unknown segment [%s] @ %s' % (header, filePath))
            
    except Exception as e:
        print(str(e))

    return

#結果を出力する
def outputResults(outputFile):

    try:
        fout = codecs.open(outputFile, 'a', 'utf-8')

        fout.write('\r\n')
        fout.write('%d record failure\r\n\r\n' % len(numericNg))
        
        for n in numericNg:
            fout.write('%s\r\n' % n)

        fout.write('\r\n')

        fout.close()

        print('see %s' % outputFile)

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

    checkNumericFields('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1', fileStr)
    
    outputResults('%s.out' % os.getpid())
