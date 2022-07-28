import os
import cv2
from rich.console import Console
from rich.prompt import Prompt

console = Console()

class searchPath:
    def __init__(self):
        pass

    def process(self):
        console.print("Folder Scraping Lists:", style="bold Yellow")
        for i in os.listdir("../"):
            if "scraping" in i:
                console.print(i, style="green")
        mainPath = "../" + Prompt.ask("[bold cyan]Select path[/bold cyan] ") + "/data/"
        for i in os.listdir(mainPath):
            console.print(i, style="green")
        childPath = Prompt.ask("[bold cyan]Select path[/bold cyan] ") + "/images"
        return mainPath + childPath

class imageToVideo:
    def __init__(self):
        self.path = searchPath().process()
        self.videoName = "data/" + self.path.replace("../", "").replace("/data/", "_").replace("/images", "") + ".mp4"
        self.framerate = int(Prompt.ask("[bold cyan]Framerate[/bold cyan] "))
        self.images = [img for img in os.listdir(self.path) if img.endswith(".png")]
        self.frame = cv2.imread(os.path.join(self.path, self.images[0]))
        self.height, self.width, self.channels = self.frame.shape
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        self.out = cv2.VideoWriter(self.videoName, self.fourcc, self.framerate, (self.width, self.height))

    def process(self):
        for i in self.images:
            self.out.write(cv2.imread(os.path.join(self.path, i)))
            console.print("Processing: " + i, style="green")
        self.out.release()

if __name__ == "__main__":
    try:
        imageToVideo().process()
    except:
        console.print("Error", style="bold red")
        imageToVideo().process()