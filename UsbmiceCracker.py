import os, sys, argparse
import numpy as np
import matplotlib.pyplot as plt

class usbmicecrack:

    def __init__(self):
        #声明变量
        pass
        
    def tshark_do(self,pcapfile, fieldvalue):
        if os.name == "nt":
            command = "tshark -r %s -T fields -e %s > %s" % (pcapfile,fieldvalue,MiceDatafile)
            try:
                os.system(command)
                print("tshark执行语句：" + command)
                print("[+] Found : tshark导出数据成功")
            except:
                print("tshark执行语句：" + command)
                print("[+] Found : tshark导出数据失败")
            
        if os.name == "posix":
            #sed '/^\s*$/d' 主要是去掉空行
            command = "tshark -r %s -T fields -e %s | sed '/^\s*$/d' > %s" % (pcapfile,fieldvalue,MiceDatafile)
            try:
                os.system(command)
                print("tshark执行语句：" + command)
                print("[+] Found : tshark导出数据成功")
            except:
                print("tshark执行语句：" + command)
                print("[+] Found : tshark导出数据失败")

    #筛掉无用数据，改变数据格式
    def formatmicedata(self, file="formatmicedatafile.txt"):

        formatfile = open(file,"w")

        with open(MiceDatafile, "r") as f:
            for i in f:
                if len(i.strip("\n")) == 8:
                    Bytes = [i[j:j+2] for j in range(0, len(i.strip("\n")), 2)]
                    data = ":".join(Bytes)
                    formatfile.writelines(data+"\n")
                if len(i.strip("\n")) == 16:
                    Bytes = [i[j:j+2] for j in range(0, len(i.strip("\n")), 2)]
                    data = ":".join(Bytes)
                    formatfile.writelines(data+"\n")

        formatfile.close()


    def to_photo(self, formatmicedatafile):
        global mousePositionX
        global mousePositionY

        action = arg.action

        #LEFT左击 ALL双击 RIGHT右击 MOVE 移动 
        #默认打印全部行为
        # if action != "LEFT" and action != "ALL" and action != "RIGHT" and action != "MOVE":
        #     action = "LEFT"

        # 读取鼠标数据
        with open(formatmicedatafile, "r") as f:
            for line in f:
                #去掉\n
                data.append(line[0:-1])

        # 鼠标移动 逐行处理数据
        for i in data:
            Bytes = i.split(":")
            if len(Bytes) == 8:
                horizontal = 2  # -
                vertical = 4  # |
            elif len(Bytes) == 4:
                horizontal = 1  # -
                vertical = 2  # |
            else:
                continue
            offsetX = int(Bytes[horizontal], 16)
            offsetY = int(Bytes[vertical], 16)
            if offsetX > 127:
                offsetX -= 256
            if offsetY > 127:
                offsetY -= 256
            mousePositionX += offsetX
            mousePositionY += offsetY
            if Bytes[0] == "01":
                print("[+] Left butten.")
                if action == "LEFT":
                    # draw point to the image panel
                    X.append(mousePositionX)
                    Y.append(-mousePositionY)
            elif Bytes[0] == "02":
                print("[+] Right Butten.")
                if action == "RIGHT":
                    # draw point to the image panel
                    X.append(mousePositionX)
                    Y.append(-mousePositionY)
            elif Bytes[0] == "00":
                print("[+] Move.")
                if action == "MOVE":
                    # draw point to the image panel
                    X.append(mousePositionX)
                    Y.append(-mousePositionY)
            else:
                print("[-] Known operate.")
                pass
            if action == "ALL":
                # draw point to the image panel
                X.append(mousePositionX)
                Y.append(-mousePositionY)

        #画图
        fig = plt.figure(figsize=(10, 8.5))
        ax1 = fig.add_subplot(111)

        ax1.set_title('[%s]-[%s] remix by : may' % (arg.pcapfile, action))
        ax1.scatter(X, Y, c='r', marker='o')
        plt.show()

        # 删除提取数据文件
        rm_stat = eval(input(f"-----是否删除tshark导出的文件 \"{arg.pcapfile}\", 1 or 0-----\n"))
        if rm_stat == 1:
            os.remove(MiceDatafile)
    
    def main(self):

        self.tshark_do(pcapfile=arg.pcapfile, fieldvalue=arg.fieldvalue)
        
        self.formatmicedata()

        self.to_photo(formatmicedatafile=formatmicedatafile)


if __name__ == "__main__":
    
    mousePositionX = 0
    mousePositionY = 0

    X = []
    Y = []

    MiceDatafile = "micedata.txt"
    formatmicedatafile="formatmicedatafile.txt"
    data = []


    BANNER = r"""                                                                                                                                
        //   / / //   ) )  //   ) )                                           
    //   / / ((        //___/ /   ___      __      ___      ___     / ___  
    //   / /    \\     / __  (   //   ) ) //  ) ) //   ) ) //   ) ) //\ \   
    //   / /       ) ) //    ) ) //       //      //   / / //       //  \ \  
    ((___/ / ((___ / / //____/ / ((____   //      ((___( ( ((____   //    \ \ 
                                                                    @MAY1AS
    """


    argobject = argparse.ArgumentParser(prog="UsbMiceDataExp", description="This is a tool for decrypt UsbMiceData")
    argobject.add_argument('-f', "--pcapfile", required=True, help="here is you pcapdatafile")
    argobject.add_argument('-e', "--fieldvalue", required=True, help="here is your output_format")
    argobject.add_argument('-a', "--action", help="here is the action you want to draw", default="ALL")

    arg = argobject.parse_args()   

    app = usbmicecrack()
    app.main()


 


