# coding: UTF-8
import os
import codecs
import lib.setup as setup
#import setup #for debug

fields = {}

#各フィールドに値が入っていたらカウントする
def countFields(filePath, dataType, fileStr):

    tmp = {}

    try:
        alllines = fileStr.strip().split('\r')
        for line in alllines:
            header = line[0:3]

            #MSH-1は自身がフィールド区切りなので後の処理のためにNULLフィールドを１つ入れておく
            if header == 'MSH':
                line = '|""'.join([line[:3],line[3:]])

            if header not in setup.HL7_SEGMENT:
                print('unknown segment [%s] @ %s' % (header, filePath))
                continue

            if header not in tmp:
                tmp[header] = [0] * len(setup.HL7_SEGMENT[header])

            #各フィールドに値が入っていたらカウントする
            l = line.split('|')
            for i in range(0,len(l)):
                if l[i] != '':
                    tmp[header][i] = tmp[header][i] + 1

        if dataType not in fields:
            fields[dataType] = {}

        #統合
        if fields[dataType] == None:
            fields[dataType] = tmp

        else:
            for k,v in tmp.items():
                if k in fields[dataType]:
                    for i in range(0,len(fields[dataType][k])):
                        fields[dataType][k][i] = fields[dataType][k][i] + v[i]
                else:
                    fields[dataType][k] = v

    except Exception as e:
        print(str(e))

    return

#結果を出力する
def outputResults(outputFile):

    try:
        
        fout = codecs.open(outputFile, 'a', 'utf-8')

        fout.write('\r\n#####countFields result#####\r\n')
        for k,v in sorted(fields.items()):
            fout.write('\r\n')
            fout.write('*%s*****************************************\r\n' % k)

            for k2,v2 in sorted(v.items()):
                fout.write('#%s:\r\n' % k2)

                for i in range(0,len(v2)):
                    v2[i] = str(v2[i])

                fout.write(', '.join(v2))
                fout.write('\r\n')

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

    countFields('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1','OMP-11', fileStr)
    
    outputResults('%s.out' % os.getpid())
