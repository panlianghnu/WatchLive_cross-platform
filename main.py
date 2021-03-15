import douyu
import huya
import bilibili
import os
import threading


live = []
out = []
lock_out = threading.Lock()


def handle_input():
    while True:
        play_index = input("")
        length = -1
        lock_out.acquire()
        length = out.__len__()
        lock_out.release()
        if length == -1:
            print("获取锁失败")
            continue
        if play_index.isnumeric():
            play_index = int(play_index)
            if play_index == 0:
                break
            if 0 < play_index <= length:
                open_app = "open -a /Applications/IINA.app"
                cmd = open_app + " '" + out[play_index - 1] + "'"
                os.system(cmd)
            else:
                print("请输入正确数字")
                continue
        else:
            print("请输入数字")
            continue


def handle_live():
    file = open("/Users/panliang/real-url/dict.txt")
    while 1:
        line = file.readline()
        if not line or len(line) < 3:
            break
        live.append(line.split(' '))
    file.close()
    index = 0
    for i in live:
        if i[0] == '斗鱼':
            result = douyu.get_real_pc_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    # print(result)
                    lock_out.acquire()
                    out.append(result)
                    lock_out.release()
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    # print(result[7:])
                    lock_out.acquire()
                    out.append(result)
                    lock_out.release()
        elif i[0] == '虎牙':
            result = huya.get_real_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    lock_out.acquire()
                    out.append(result)
                    lock_out.release()
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    lock_out.acquire()
                    out.append(result)
                    lock_out.release()
        elif i[0] == 'bilibili':
            result = bilibili.get_real_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    lock_out.acquire()
                    out.append(result)
                    lock_out.release()
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    lock_out.acquire()
                    out.append(result)
                    lock_out.release()


class liveThread(threading.Thread):
    def run(self):
        handle_live()


class inputThread(threading.Thread):
    def run(self):
        handle_input()


if __name__ == '__main__':
    print("请输入播放序号:")
    print("以下是在线的主播：")
    print("0: 结束程序")
    thread1 = liveThread()
    thread2 = inputThread()
    thread1.start()
    thread2.start()
