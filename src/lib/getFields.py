# coding: UTF-8
import os
import codecs
import lib.setup as setup
#import setup #for debug

result = {}

def getFields(filePath, dataType, fileStr):

    alllines = fileStr.strip().split('\r')

    for gf in setup.getField:
        key = '%s-%s@%s' % (gf['segmentHeader'], ','.join(map(str,gf['fieldIndex'])), ','.join(map(str,gf['exampleIndex'])))

        if key not in result:
            result[key] = {}

        for line in alllines:
            header = line[0:3]

            if header == gf['segmentHeader']:
                fields = (line + '|' * max(gf['fieldIndex'])).split('|')

                if dataType not in result[key]:
                    result[key][dataType] = {}

                #指定フィールドの取得
                tmpF = ''
                for f in sorted(gf['fieldIndex']):
                    tmpF = '%s%s\t' % (tmpF, fields[f])
                tmpF = tmpF[:-1]

                if tmpF not in result[key][dataType]:
                    result[key][dataType][tmpF] = {}
                    result[key][dataType][tmpF]['count'] = 0
                    
                #例示の取得
                for ei in sorted(gf['exampleIndex']):
                    result[key][dataType][tmpF]['example' + str(ei)] = fields[ei]

                #フィールド値の出現数
                result[key][dataType][tmpF]['count'] += 1

                #出現箇所の例
                result[key][dataType][tmpF]['file'] = filePath

    return
            
def outputResults(outputFile):

    fout = codecs.open(outputFile, 'a', 'utf-8')

    fout.write('\r\n#####getField result#####\r\n')
    for k,v in sorted(result.items()):
        fout.write('\r\n*%s==================\r\n' % k)
        
        for k2,v2 in sorted(v.items()):
            fout.write('\r\n*%s******************\r\n' % k2)

            s = ''
            for k3,v3 in sorted(v2.items()):
                s = k3

                tmp = k.split('@')
                if len(tmp) == 2:
                    exampleIndex = tmp[1]
                    exampleIndex = map(int,exampleIndex)
                        
                for ei in sorted(exampleIndex):
                    s = '%s\t%s' % (s, v3['example' + str(ei)])

                s = '%s\t%s\t%s\r\n' % (s, v3['count'], v3['file'])
                fout.write(s)
            
    fout.write('\r\n')

    fout.close()

    return

if __name__ == "__main__":
    
    import sys
    import codecs

    setup.getField.append({'segmentHeader':'OBX','fieldIndex':[3,6,7],'exampleIndex':[5]})

    fin = codecs.open('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1', 'r', 'utf-8')
    fileStr = fin.read()
    fin.close()

    getFields('..\\..\\sampleData\\000\\000\\0000001\\20000401\\OMP-11\\0000001_20000401_OMP-11_123456789012345_20110701113813225_01_1','OMP-11', fileStr)
    
    outputResults('%s.out' % os.getpid())

