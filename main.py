import douyu
import huya
import bilibili
import os

# douyu.get_real_url(r)
# huya.get_real_url(r)

live = []
out = []

if __name__ == '__main__':
    file = open("./dict.txt")
    print("以下是在线的主播：")
    while 1:
        line = file.readline()
        if not line or len(line) < 3:
            break
        live.append(line.split(' '))
    index = 0
    for i in live:
        if i[0] == '斗鱼':
            result = douyu.get_real_pc_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    # print(result)
                    out.append(result)
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    # print(result[7:])
                    out.append(result[7:])
        elif i[0] == '虎牙':
            result = huya.get_real_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    out.append(result)
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    out.append(result[7:])
        elif i[0] == 'bilibili':
            result = bilibili.get_real_url(i[1])
            if result != '未开播':
                index = index + 1
                if 'replay>' not in result:
                    print("%d: %s" % (index, i[2][0:-1]))
                    out.append(result)
                else:
                    print("%d: %s(重播)" % (index, i[2][0:-1]))
                    out.append(result[7:])
    while True:
        play_index = input("请输入播放序号:")
        if play_index.isnumeric():
            play_index = int(play_index)
            if 0 < play_index <= index:
                cmd = "open -a /Applications/IINA.app '" + out[play_index - 1] + "'"
                os.system(cmd)
                break
            else:
                continue
        else:
            print("请输入正确数字")
            continue
