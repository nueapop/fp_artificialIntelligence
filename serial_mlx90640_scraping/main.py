import os
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import serial.tools.list_ports
from datetime import datetime

sns.set_style({'font.family': 'Times New Roman'})

class detectSerial:
    def __init__(self):
        self.serialList = []

    def get_serial_list(self):
        for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
            self.serialList.append(port)
        if len(self.serialList) > 1:
            print("Serial ports found:")
            for i in range(len(self.serialList)):
                print(str(i + 1) + ": " + self.serialList[i])
            return input("Select serial port: ")
        elif len(self.serialList) == 1:
            return self.serialList[0]
        else:
            print("No serial ports found.")
            exit()

class ReadLine:
    def __init__(self, s):
        self.buf = bytearray()
        self.s = s

    def readline(self):
        i = self.buf.find(b"\n")
        if i >= 0:
            r = self.buf[:i+1]
            self.buf = self.buf[i+1:]
            return r
        while True:
            i = max(1, min(2048, self.s.in_waiting))
            data = self.s.read(i)
            i = data.find(b"\n")
            if i >= 0:
                r = self.buf + data[:i+1]
                self.buf[0:] = data[i+1:]
                return r
            else:
                self.buf.extend(data)

class plot:
    def __init__(self, data, timeNow, name):
        self.data = data
        self.time = int(datetime.timestamp(timeNow))
        self.address = "./data/" + name + "/images/" + str(self.time) + ".png"

    def processPlot(self):
        frame = [float(x) for x in self.data.split(',')]
        frame2D = []
        for h in range(24):
            frame2D.append([])
            for w in range(32):
                t = frame[h * 32 + w]
                frame2D[h].append(t)
        sns.heatmap(frame2D, annot=True, cmap="coolwarm", linewidths=.1, annot_kws={"size":6}, yticklabels=False, xticklabels=False, vmin=27, vmax=28)
        plt.title("Heatmap of MLX90640 data: " + str(self.time))
        plt.savefig(self.address)
        plt.close()
        time.sleep(0.5)

class csvWrite:
    def __init__(self, data, address):
        self.data = data
        self.address = address

    def processRaw(self):
        frame = [int(x) for x in self.data.split(',')]
        df = pd.DataFrame(frame)
        df.T.to_csv(self.address, mode="a", header=False, index=False)

    def processCount(self):
        a = 0
        b = 0
        c = 0
        d = 0
        e = 0
        f = 0
        g = 0
        h = 0
        error = 0
        total = 0
        for i in self.data.split(','):
            count = int(i)
            if count >= 38 and count < 40:
                a += 1
            elif count >= 36 and count < 38:
                b += 1
            elif count >= 34 and count < 36:
                c += 1
            elif count >= 32 and count < 34:
                d += 1
            elif count >= 30 and count < 32:
                e += 1
            elif count >= 28 and count < 30:
                f += 1
            elif count >= 26 and count < 28:
                g += 1
            elif count >= 24 and count < 26:
                h += 1
            else:
                error += 1
            total += 1
        df = pd.DataFrame([[a, b, c, d, e, f, g, h, error, total]])
        df.to_csv(self.address, mode="a", header=False, index=False, sep="\t")

class scraping:
    def __init__(self):
        self.port = detectSerial().get_serial_list()

    def process(self):
        serialRead = ReadLine(serial.Serial(self.port, 115200))
        while True:
            name = input("Enter name of file: ")
            if name in os.listdir("data"):
                print("File already exists.")
                continue
            else:
                os.mkdir("./data/" + name)
                os.mkdir("./data/" + name + "/images")
                df = pd.DataFrame([["38-39", "36-37", "34-35", "32-33", "30-31", "28-29", "26-27", "24-25", "Error", "Total"]])
                df.to_csv("./data/" + name + "/count.csv", mode="a", header=False, index=False, sep="\t")
                break
        number = int(input("Enter number of frames: "))
        for i in range(number):
            data = str(serialRead.readline())
            data = data.replace("bytearray(b'[", "")
            data = data.replace("]\\r\\n')", "")
            timeNow = datetime.now()
            plot(data, timeNow, name).processPlot()
            csvWrite(data, address="./data/" + name + "/raw.csv").processRaw()
            csvWrite(data, address="./data/" + name + "/count.csv").processCount()
            print("Frame " + str(i + 1) + " of " + str(number) + " processed.")

if __name__ == '__main__':
    try:
        scraping().process()
    except:
        print("Error")
        scraping().process()