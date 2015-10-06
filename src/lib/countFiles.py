# coding: UTF-8
import os
import codecs

count_by_datakind = {}
count_by_medication_month = {}
count_by_timestamp_month = {}
count_by_department = {}

#データ種別・診療月・タイムスタンプ月・診療科ごと・コンディションフラグごとにファイル数を数える
def countFiles(fileName):

    try:
        
        #file = 0_1_2_3_4_5_6_7
        #0: patient id
        #1: - or medication date
        #2: data kind
        #3: order number
        #4: file time stamp
        #5: department
        #6: condition flag
        f = fileName.split('_')

        #データ種別ごと・コンディションフラグごとに数える
        countByDataKind(f[2], f[6], f[1], f[4])

        #診療月ごと・コンディションフラグごとに数える
        countByMedicationMonth(f[1][:6], f[6])

        #タイムスタンプごと・コンディションフラグごとに数える
        countByTimestampMonth(f[4][:6], f[6])

        #診療科ごと・コンディションフラグごとに数える
        countByDepartment(f[5], f[6])
            
    except Exception as e:
        print(str(e))

    return

#データ種別ごと・コンディションフラグごとに数える
def countByDataKind(dataKind, conditionFlag, medicationMonth, timestampMonth):

    try:
            
        key = '@@@'.join([dataKind, conditionFlag])

        if key not in count_by_datakind:
            count_by_datakind[key] = {}
            count_by_datakind[key]['minMM'] = medicationMonth
            count_by_datakind[key]['maxMM'] = medicationMonth
            count_by_datakind[key]['minTS'] = timestampMonth
            count_by_datakind[key]['maxTS'] = timestampMonth
            count_by_datakind[key]['count'] = 1

        else:
            if count_by_datakind[key]['minMM'] > medicationMonth:
                count_by_datakind[key]['minMM'] = medicationMonth
            
            if count_by_datakind[key]['maxMM'] < medicationMonth:
                count_by_datakind[key]['maxMM'] = medicationMonth
            
            if count_by_datakind[key]['minTS'] > timestampMonth:
                count_by_datakind[key]['minTS'] = timestampMonth
            
            if count_by_datakind[key]['maxTS'] < timestampMonth:
                count_by_datakind[key]['maxTS'] = timestampMonth
            
            count_by_datakind[key]['count'] = count_by_datakind[key]['count'] + 1

    except Exception as e:
        print(str(e))    

    return

#診療月・コンディションフラグごとに数える
def countByMedicationMonth(medicationMonth, conditionFlag):

    try:
        
        key = '@@@'.join([medicationMonth, conditionFlag])

        if key not in count_by_medication_month:
            count_by_medication_month[key] = 1

        else:
            count_by_medication_month[key] = count_by_medication_month[key] + 1

    except Exception as e:
        print(str(e))

    return

#タイムスタンプ月・コンディションフラグごとに数える
def countByTimestampMonth(timestampMonth, conditionFlag):

    try:
        
        key = '@@@'.join([timestampMonth, conditionFlag])

        if key not in count_by_timestamp_month:
            count_by_timestamp_month[key] = 1

        else:
            count_by_timestamp_month[key] = count_by_timestamp_month[key] + 1

    except Exception as e:
        print(str(e))
        
    return

#診療科ごと・コンディションフラグごとに数える
def countByDepartment(department, conditionFlag):

    try:

        key = '@@@'.join([department, conditionFlag])

        if key not in count_by_department:
            count_by_department[key] = 1

        else:
            count_by_department[key] = count_by_department[key] + 1

    except Exception as e:
        print(str(e))

    return

#結果を出力する
def outputResults(outputFile):

    try:

        fout = codecs.open(outputFile, 'a', 'utf-8')

        fout.write('\r\n#####countFiles result#####\r\n')
        fout.write('*data kind*************************************************\r\n\r\n')

        fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\r\n' % ('data kind', 'condition flag', 'min medication date', 'max medication date', 'min timestamp', 'max timestamp', 'count'))

        for k,v in sorted(count_by_datakind.items()):

            kk = k.split('@@@')
            
            fout.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\r\n' % (kk[0], kk[1], v['minMM'], v['maxMM'], v['minTS'], v['maxTS'], v['count']))

        fout.write('\r\n')

        fout.write('*medication month*************************************************\r\n\r\n')

        fout.write('%s\t%s\t%s\t\r\n' % ('medication month', 'condition flag', 'count'))

        for k,v in sorted(count_by_medication_month.items()):

            kk = k.split('@@@')

            fout.write('%s\t%s\t%s\t\r\n' % (kk[0], kk[1], v))

        fout.write('\r\n')

        fout.write('*timestamp month*************************************************\r\n\r\n')

        fout.write('%s\t%s\t%s\t\r\n' % ('timestamp month', 'condition flag', 'count'))

        for k,v in sorted(count_by_timestamp_month.items()):

            kk = k.split('@@@')

            fout.write('%s\t%s\t%s\t\r\n' % (kk[0], kk[1], v))    

        fout.write('\r\n')

        fout.write('*department*************************************************\r\n\r\n')

        fout.write('%s\t%s\t%s\t\r\n' % ('department', 'condition flag', 'count'))

        for k,v in sorted(count_by_department.items()):

            kk = k.split('@@@')

            fout.write('%s\t%s\t%s\t\r\n' % (kk[0], kk[1], v))    

        fout.write('\r\n')

        fout.close()

    except Exception as e:
        print(str(e))

    return

if __name__ == "__main__":
    
    import sys
    
    countFiles('..\\sampleData\\000\\000\\0000001\\20000401\\9999013_20110630_OMP-11_123456789012345_20110701113813225_01_1')

    outputResults('%s.out' % os.getpid())
