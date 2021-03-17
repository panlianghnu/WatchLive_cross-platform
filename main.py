import douyu
import huya
import bilibili
import os
import threading
from pynput import keyboard

live = []
url = []
lock_url = threading.Lock()
name = []
lock_name = threading.Lock()
if_stop = ["run"]  # 可变全局变量才有意义
lock_if_stop = threading.Lock()


def handle_input(key):
    play_index = key
    length = -1
    lock_url.acquire()
    length = url.__len__()
    lock_url.release()
    if length == -1:
        print("获取length失败")
        return
    if play_index.isnumeric():
        play_index = int(play_index)
        if 0 < play_index <= length:
            lock_name.acquire()
            print("__进入" + name[play_index-1] + "的直播间")
            lock_name.release()
            open_app = "open -a /Applications/IINA.app"
            cmd = open_app + " '" + url[play_index - 1] + "'"
            os.system(cmd)


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
        # 读 if_stop
        lock_if_stop.acquire()
        if if_stop[0] == "stop":
            print("exit...")
            return
        lock_if_stop.release()
        if i[0] == '斗鱼':
            result = douyu.get_real_pc_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    # print(result)
                    lock_url.acquire()
                    url.append(result)
                    lock_url.release()

                    lock_name.acquire()
                    name.append(i[2][0:-1])
                    lock_name.release()
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    # print(result[7:])
                    lock_url.acquire()
                    url.append(result[7:])
                    lock_url.release()

                    lock_name.acquire()
                    name.append(i[2][0:-1])
                    lock_name.release()
        elif i[0] == '虎牙':
            result = huya.get_real_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    lock_url.acquire()
                    url.append(result)
                    lock_url.release()

                    lock_name.acquire()
                    name.append(i[2][0:-1])
                    lock_name.release()
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    lock_url.acquire()
                    url.append(result[7:])
                    lock_url.release()

                    lock_name.acquire()
                    name.append(i[2][0:-1])
                    lock_name.release()
        elif i[0] == 'bilibili':
            result = bilibili.get_real_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    lock_url.acquire()
                    url.append(result)
                    lock_url.release()

                    lock_name.acquire()
                    name.append(i[2][0:-1])
                    lock_name.release()
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    lock_url.acquire()
                    url.append(result[7:])
                    lock_url.release()

                    lock_name.acquire()
                    name.append(i[2][0:-1])
                    lock_name.release()
    print("没有更多主播了")


class liveThread(threading.Thread):
    def run(self):
        handle_live()


class inputThread(threading.Thread):
    def run(self):
        with keyboard.Listener(on_release=on_release) as listeners:
            listeners.join()


def on_release(key):
    try:
        key_ = str(key)
        if key_ == "'0'" or key == keyboard.Key.esc:
            lock_if_stop.acquire()
            if_stop[0] = "stop"
            lock_if_stop.release()
            print(":不再监听键盘...")
            return False
        handle_input(key_[1])
    except AttributeError:
        print("keyboard err")


if __name__ == '__main__':
    print("请输入播放序号:")
    print("以下是在线的主播：")
    print("0: 结束程序")
    thread1 = liveThread()
    thread2 = inputThread()
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
