# coding: UTF-8
import os
import codecs

notJIS = []

#JISとして読めなかったファイルを列挙する
def checkJIS(filePath):

    try:

        fin = codecs.open(filePath, 'r', 'iso-2022-jp')

        s = fin.read()

        fin.close()

    except:
        notJIS.append(filePath)
    
    return

#結果を出力する
def outputResults(outputFile):

    try:
        
        fout = codecs.open(outputFile, 'a', 'utf-8')

        fout.write('\r\n')
        fout.write('%d files failure\r\n\r\n' % len(notJIS))
        
        for n in notJIS:
            fout.write('%s\r\n' % n)

        fout.write('\r\n')

        fout.close()

        print('see %s' % outputFile)

    except Exception as e:
        print(str(e))

if __name__ == "__main__":
    
    import sys
    
    checkJIS('..\\sampleData\\000\\000\\0000001\\20000401\\notJIS.txt')

    outputResults('%s.out' % os.getpid())
