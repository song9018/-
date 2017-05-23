#!/usr/bin/env python
# coding=utf-8
import os
import xlrd, xlsxwriter
from xlutils import copy
import glob


class PPG:
    def time_change(self, s_time):
        s_time = s_time.split(":")
        if s_time[2] == "0":
            s_time[2] = '00'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "1":
            s_time[2] = '01'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "2":
            s_time[2] = '02'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "3":
            s_time[2] = '03'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "4":
            s_time[2] = '04'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "5":
            s_time[2] = '05'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "6":
            s_time[2] = '06'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "7":
            s_time[2] = '07'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "8":
            s_time[2] = '08'
            date = (":").join(s_time)
            return date
        elif s_time[2] == "9":
            s_time[2] = '09'
            date = (":").join(s_time)
            return date
        else:
            date = (":").join(s_time)
            return date

    def PPG1(self, index, file, excel_file):
        try:
            file1 = glob.glob(file)
            for i in range(len(file1)):
                file = open(file1[i], "r", encoding="utf-8")
                path = file1[i].split(".")[1].split("\\")[2]
                workbook = xlsxwriter.Workbook(excel_file + '%s.xls' % path)  # 创建一个excel文件
                workbook.close()
                line = file.readline()
                list = line.strip().split(',')
                i = 0
                j = 0
                k = 1
                while i < 5:
                    if list[i] == " Pol":
                        break
                    else:
                        i += 1
                while j < 5:
                    if list[j] == "Time":
                        break
                    else:
                        j += 1
                s = file.readlines()

                excel = xlrd.open_workbook(excel_file + '%s.xls' % path, 'wb')
                wb = copy.copy(excel)
                ws = wb.get_sheet(index)
                ws.write(0, 0, "心率带采集时间")
                ws.write(0, 1, "心率带心率值")
                for line1 in s:
                    list1 = line1.strip().split(',')
                    if k < len(s):
                        ws.write(k, 0, list1[0])
                        ws.write(k, 1, int(list1[3]))
                        k += 1
                wb.save(excel_file + '%s.xls' % path)

        except Exception as e:
            print(e)
        finally:
            wb.save(excel_file + '%s.xls' % path)


def get_garmin(file, file_path):
    file1 = glob.glob(file)
    excel1 = glob.glob(file_path)

    for i in range(len(file1)):

        list_heart = []
        list_spm = []

        file2 = open(file1[i], "r", encoding="utf-8")
        lines = file2.readlines()
        excel_file = xlrd.open_workbook(excel1[i], 'wb')
        wb = copy.copy(excel_file)
        ws = wb.get_sheet(0)
        ws.write(0, 4, "garmin心率")
        ws.write(0, 5, "garmin步频")
        for j in range(len(lines)):
            if "<Time>" in lines[j] and "Z" in lines[j]:
                if "<Value>" in lines[j + 3]:
                    heart = lines[j + 3].split("<Value>")[1].split("</Value>")[0]
                    list_heart.append(heart)

                if "<RunCadence>" in lines[j + 8]:
                    spm = lines[j + 8].split("<RunCadence>")[1].split("</RunCadence>")[0]
                    list_spm.append(spm)

        for k in range(len(list_heart)):
            ws.write(k + 1, 4, int(list_heart[k]))
        for l in range(len(list_spm)):
            ws.write(l + 1, 5, (int(list_spm[l]))*2)
        wb.save(excel1[i])

def get_garmin_speed(file, file_path,path1):
    file1 = glob.glob(file)

    for i in range(len(file1)):
        path = file1[i].split(".")[1].split("\\")[2]
        workbook = xlsxwriter.Workbook(path1 + '%s.xls' % path)  # 创建一个excel文件
        workbook.close()

    excel1 = glob.glob(file_path)
    for i in range(len(file1)):
        path = file1[i].split(".")[1].split("\\")[2]
        list_speed = []

        file2 = open(file1[i], "r", encoding="utf-8")
        lines = file2.readlines()

        excel_file = xlrd.open_workbook(excel1[i], 'wb')
        wb = copy.copy(excel_file)
        ws = wb.get_sheet(0)
        #ws.write(0, 0, "garmin时间")
        ws.write(0, 0, "garmin速度")
        for j in range(len(lines)):
            #if "<Time>" in lines[j] and "Z" in lines[j]:
            if "<Speed>" in lines[j]:
                heart = lines[j].split("<Speed>")[1].split("</Speed>")[0]

                list_speed.append(heart)

        for k in range(len(list_speed)):
            ws.write(k + 1, 0, float(list_speed[k]))

        wb.save(excel1[i])


def XH3_heart(file, file_path,path1):
    try:
        file1 = glob.glob(file)
        excel1 = glob.glob(file_path)
        for i in range(len(file1)):
            path = file1[i].split(".")[1].split("\\")[2]
            workbook = xlsxwriter.Workbook(path1 + '%s.xls' % path)  # 创建一个excel文件
            workbook.close()
        for i in range(len(file1)):
            list_heart = []
            list_spm = []
            heart1 = []
            spm1 = []
            file2 = open(file1[i], "r", encoding="utf-8")
            lines = file2.readlines()
            excel_file = xlrd.open_workbook(excel1[i], 'wb')
            wb = copy.copy(excel_file)
            ws = wb.get_sheet(0)
            ws.write(0, 0, "XH3心率")
            ws.write(0, 1, "XH3步频")
            for j in range(len(lines)):
                if "开始时间" not in lines[j]:
                    heart = lines[j].split()[5]
                    spm = lines[j].split()[4]
                    list_heart.append(heart)
                    list_spm.append(spm)

            for k in range(len(list_heart)):
                if list_heart[k] != "":
                    ii = k
                    break
            for l in range(len(list_spm)):
                if list_spm[l] != "":
                    jj = l
                    break
            for k in range(len(list_heart) - ii):
                heart1.append(int(list_heart[k + ii]))
            for l in range(len(list_spm) - jj):
                spm1.append(int(list_spm[l + jj]))

            ws.write(1, 0, heart1[0])
            ws.write(1, 1, spm1[0])
            for k in range(int(len(heart1) / 25)):
                ws.write(k + 2, 0, heart1[k * 25])
                if len(heart1) - k < 26:
                    break

            for l in range(int(len(spm1) / 25)):
                ws.write(l + 2, 1, spm1[l * 25])
                if len(spm1) - l < 26:
                    break
            wb.save(excel1[i])
    except Exception as e:
        print(e)
    finally:
        wb.save(excel1[i])


def remove_file():
    for file in glob.glob(os.path.join(r'.\\excel_1#\\', '*.xls')):
        os.remove(file)
    for file in glob.glob(os.path.join(r'.\\excel_2#\\', '*.xls')):
        os.remove(file)


if __name__ == "__main__":
    #remove_file()
    #ppg = PPG()
    #ppg.PPG1(0, ".\\心率带1#\\pixart_ble*.txt", ".\\excel_1#\\")
    #ppg.PPG1(0, ".\\心率带2#\\pixart_ble*.txt", ".\\excel_2#\\")
    #get_garmin(".\\garmin_1#\\*.tcx", ".\\excel_1#\\*.xls")
    #get_garmin(".\\garmin_2#\\*.tcx", ".\\excel_2#\\*.xls")
    XH3_heart(".\\garmin_1#\\*.txt", ".\\excel_1#\\*.xls",".\\excel_1#\\")
    #XH3_heart(".\\garmin_2#\\*.txt", ".\\excel_2#\\*.xls")
    #get_garmin_speed(".\\garmin_1#\\*.tcx", ".\\excel_1#\\*.xls",".\\excel_1#\\")
