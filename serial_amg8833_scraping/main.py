import os
import pandas as pd
import seaborn as sns
import serial.tools.list_ports
import matplotlib.pyplot as plt
from datetime import datetime
from rich.console import Console
from rich.prompt import Prompt

console = Console()
sns.set_style({'font.family': 'Times New Roman'})

class detectSerial:
    def __init__(self):
        self.serialList = []

    def get_serial_list(self):
        for port, desc, hwid in sorted(serial.tools.list_ports.comports()):
            self.serialList.append(port)
        if len(self.serialList) > 1:
            console.print("Serial ports found:", style="bold green")
            for i in range(len(self.serialList)):
                console.print(str(i + 1) + ": " + self.serialList[i])
            return Prompt.ask("[bold cyan]Select serial port[/bold cyan] ", style="bold green")
        elif len(self.serialList) == 1:
            return self.serialList[0]
        else:
            console.print("No serial ports found.", style="bold red")
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
    def __init__(self, data, timeNow, name, roundLoop):
        self.data = data
        self.time = int(datetime.timestamp(timeNow))
        self.roundLoop = roundLoop
        self.address = "./data/" + name + "/images/" + str(self.time) + str(self.roundLoop) + ".png"

    def processPlot(self):
        frame = [float(x) for x in self.data.split(',')]
        frame2D = []
        for h in range(8):
            frame2D.append([])
            for w in range(8):
                t = frame[h * 8 + w]
                frame2D[h].append(t)
        sns.heatmap(frame2D, annot=True, cmap="coolwarm", linewidths=.1, annot_kws={"size":6}, yticklabels=False, xticklabels=False, vmin=41, vmax=42)
        plt.title("Heatmap of AMG8833 data: " + str(self.time) + str(self.roundLoop))
        plt.savefig(self.address)
        plt.close()

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
            if count >= 48 and count < 51:
                a += 1
            elif count >= 45 and count < 48:
                b += 1
            elif count >= 42 and count < 45:
                c += 1
            elif count >= 39 and count < 42:
                d += 1
            elif count >= 36 and count < 39:
                e += 1
            elif count >= 33 and count < 36:
                f += 1
            elif count >= 30 and count < 33:
                g += 1
            elif count >= 27 and count < 30:
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
            name = Prompt.ask("[bold cyan]Enter name of file[/bold cyan] ")
            if name in os.listdir("data"):
                console.print("File already exists.", style="bold red")
                continue
            else:
                os.mkdir("./data/" + name)
                os.mkdir("./data/" + name + "/images")
                df = pd.DataFrame([["48-50", "45-47", "42-44", "39-41", "36-38", "33-35", "30-32", "27-29", "Error", "Total"]])
                df.to_csv("./data/" + name + "/count.csv", mode="a", header=False, index=False, sep="\t")
                break
        number = int(Prompt.ask("[bold cyan]Enter number of frames[/bold cyan] [bold green][DEFAULT[/bold green] [bold red]1000[/bold red] [bold green]FRAME][/bold green] ", default=1000))
        roundLoop = 1
        with console.status("[bold cyan]Scraping on tasks...", spinner="bouncingBar") as status:
            for i in range(number):
                data = str(serialRead.readline())
                data = data.replace("bytearray(b'[", "")
                data = data.replace("]\\r\\n')", "")
                timeNow = datetime.now()
                plot(data, timeNow, name, roundLoop).processPlot()
                roundLoop += 1
                csvWrite(data, address="./data/" + name + "/raw.csv").processRaw()
                csvWrite(data, address="./data/" + name + "/count.csv").processCount()
                console.log("Frame [green]" + str(i + 1) + "[/green] of [bold green]" + str(number) + "[/bold green] processed.")

if __name__ == '__main__':
    try:
        scraping().process()
    except:
        console.print("Error", style="bold red")
        scraping().process()