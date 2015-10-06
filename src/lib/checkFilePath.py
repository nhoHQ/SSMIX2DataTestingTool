# coding: UTF-8
import os
import codecs

locationNG = []

#ファイル名とディレクトリ名に矛盾があるファイルを列挙する
def checkFilePath(rootDir, fileName):

    try:

        #root = 0/1/2/3/4/5/6
        #0: other
        #1: ss-mix standard storage root
        #2: patient id 0,1,2
        #3: patient id 3,4,5
        #4: patient id full
        #5: - or medication date
        #6: file type
        f = fileName.split('_')
        
        #file = 0_1_2_3_4_5_6_7
        #0: patient id
        #1: - or medication date
        #2: file type
        #3: order number
        #4: file time stamp
        #5: department
        #6: condition flag
        l = os.path.join(f[0][0:3], f[0][3:6], f[0], f[1], f[2])

        if rootDir.endswith(l) == False:
            locationNG.append(os.path.join(rootDir,fileName))

    except Exception as e:
        print('exception @ %s\%s' % (rootDir, fileName))
        locationNG.append('%s\%s' % (rootDir, fileName))
        
        print(str(e))
    
    return

#結果を出力する
def outputResults(outputFile):

    try:

        fout = codecs.open(outputFile, 'a', 'utf-8')

        fout.write('\r\n#####checkFilePath result####\r\n')
        fout.write('%d files failure\r\n\r\n' % len(locationNG))
        
        for n in locationNG:
            fout.write('%s\r\n' % n)

        fout.write('\r\n')

        fout.close()

    except Exception as e:
        print(str(e))
    
    return

if __name__ == "__main__":
    
    import sys
    
    checkFilePath('..\\sampleData\\000\\000\\0000001\\20000401\\ADT-31\\', '..\\sampleData\\000\\000\\0000001\\20000401\\9999013_20110630_OMP-11_123456789012345_20110701113813225_01_1')

    outputResults('%s.out' % os.getpid())

