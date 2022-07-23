import seaborn as sns
import matplotlib.pyplot as plt
import serial.tools.list_ports

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
    def __init__(self, data):
        self.data = data

    def processPlot(self):
        frame = [float(x) for x in self.data.split(',')]
        frame2D = []
        for h in range(24):
            frame2D.append([])
            for w in range(32):
                t = frame[h * 32 + w]
                frame2D[h].append(t)
        sns.heatmap(frame2D, annot=True, cmap="coolwarm", linewidths=.1, annot_kws={"size":6}, yticklabels=False, xticklabels=False, vmin=28, vmax=35)
        plt.show()

class scraping:
    def __init__(self):
        self.port = detectSerial().get_serial_list()

    def process(self):
        serialRead = ReadLine(serial.Serial(self.port, 115200))
        name = input("Enter name of file: ")
        number = int(input("Enter number of frames: "))
        for i in range(number):
            data = str(serialRead.readline())
            data = data.replace("bytearray(b'[", "")
            data = data.replace("]\\r\\n')", "")
            plot(data).processPlot()

if __name__ == '__main__':
    scraping().process()