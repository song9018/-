#!/usr/bin/env python
# coding=utf-8
import os, ctypes
import glob


def judge(pathDir):
    file = open(pathDir, 'r')
    list = file.readlines()

    for i in range(len(list) - 1):
        if "0e8000" not in list[i]:
            time = int(list[i].split(":")[0], base=16)
            time1 = int(list[i + 1].split(":")[0], base=16)
            if time1 - time != 18:
                print("数据丢失：%s\n%s" % (time1, time))


def handle(pathDir, time):
    o_fd = open('%s_处理后数据.txt' % time, 'w', encoding="utf-8")
    o_fd.write('ax ay az m_step m_step_fq heart_rate 0x00 0x00 0x00\n'.replace(' ', ' ' * 3))

    flash_addr = 0xE8000
    for line in open(pathDir, 'r'):
        line = line.strip()
        if not len(line):
            continue

        sp = line.split(':')
        if len(sp) < 2:
            continue
        cur_addr = int(sp[0], base=16)
        if cur_addr != flash_addr:
            print('数据有丢失', line, hex(cur_addr), hex(flash_addr))

        flash_addr = cur_addr + 18

        if sp[1] == 'f' * 36:
            continue

        u16s = [0] * 9
        for i in range(9):
            u16s[i] = int(sp[1][i * 4:i * 4 + 4], base=16)

        if 0xdcba == u16s[0] and 0x9876 == u16s[1]:
            sec = (u16s[2] + (u16s[3] << 16)) % (24 * 60 * 60)
            minute = sec / 60
            hour = minute / 60
            o_fd.write(u'开始时间:%d:%02d:%02d\t' % (hour, minute % 60, sec % 60))
            o_fd.write('\n')

        elif 0xdcba == u16s[0] and 0x4321 == u16s[1]:
            sec = (u16s[2] + (u16s[3] << 16)) % (24 * 60 * 60)
            minute = sec / 60
            hour = minute / 60
            o_fd.write('time %d:%02d:%02d\t' % (hour, minute % 60, sec % 60))
            o_fd.write(
                'strokes=%d\tlaps=%d\tstyle=%d\n' % (u16s[4] + (u16s[5] << 16), u16s[6] + (u16s[7] << 16), u16s[8]))


        elif 0x4321 != u16s[1] and 0x9876 != u16s[1]:
            for i in range(9):
                o_fd.write('%d ' % ctypes.c_short(u16s[i]).value)
            o_fd.write('\n')
    o_fd.close()


def get_data(time):
    file = open("%s_处理后数据.txt" % time, 'r', encoding="utf-8")
    k = 0
    list1 = []
    time_list = 0
    list = file.readlines()
    for i in range(len(list)):
        if "开始时间" in list[i]:
            k += 1
            list1.append(i)
    list1.append(len(list) - 1)
    s = 0
    while k > time_list:

        o_fd = open('./拆分数据文件/分段数据__%s_%s.txt' % (time, time_list), 'w', encoding="utf-8")
        for i in range(len(list) - (list1[s]) - 1):
            o_fd.write(list[i + (list1[s])])
            if i + (list1[s]) + 1 == list1[s + 1]:
                break

        o_fd.close()
        s += 1
        time_list += 1


def get_time():
    file = glob.glob(".\\拆分数据文件\\*.txt")
    for i in range(len(file)):
        file1 = open(file[i], 'r', encoding="utf-8")
        list = file1.readlines()
        list1 = []
        list1.append(list[0] + "ax  ay  az\n")
        path = file[i].split(".")[1].split("__")[1]
        file2 = open(os.path.join(os.getcwd(), "拆分数据文件\三轴数据\三轴数据%s.txt" % path), 'w', encoding="utf-8")
        for i in range(len(list)):
            if "开始时间" not in list[i]:
                l=list[i].split()
                list1.append(l[0]+" ")
                list1.append(l[1]+" ")
                list1.append(l[2]+"\n")
        file2.writelines(list1)


def run():
    file = glob.glob("*.log")

    for i in range(len(file)):
        time = file[i].split("RTT_Terminal_")[1].split(".")[0]

        judge(file[i])
        handle(file[i], time)
        get_data(time)


def rm_file():
    for file in glob.glob(os.path.join(r'拆分数据文件\\', '*.txt')):
        os.remove(file)
    for file in glob.glob(os.path.join(r'拆分数据文件\三轴数据', '*')):
        os.remove(file)
    for file in glob.glob(os.path.join(os.getcwd(), '*.txt')):
        os.remove(file)


if __name__ == '__main__':
    rm_file()
    run()
    get_time()
