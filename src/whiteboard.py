import tkinter as tk
from PIL import Image, ImageDraw


class Whiteboard:
    def __init__(self, master):
        self.master = master
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.setup_canvas()

        self.canvas.bind("<ButtonPress-1>", self.start_line)
        self.canvas.bind("<B1-Motion>", self.draw_line)
        self.canvas.bind("<ButtonRelease-1>", self.end_line)

        self.current_line = None
        self.current_line_points = []

        self.lines = []
        self.draw_actions = []

    def setup_canvas(self):
        self.master.update()
        self.width = self.master.winfo_width()
        self.height = self.master.winfo_height()
        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.draw = ImageDraw.Draw(self.image)

    def start_line(self, event):
        self.current_line = self.canvas.create_line(event.x, event.y, event.x, event.y,
                                                    width=2, fill="black", capstyle=tk.ROUND, smooth=tk.TRUE)
        self.current_line_points = [(event.x, event.y)]

    def draw_line(self, event):
        self.current_line_points.append((event.x, event.y))
        self.canvas.coords(self.current_line, *[coord for point in self.current_line_points for coord in point])

    def end_line(self, event):
        if len(self.current_line_points) > 1:
            self.lines.append(self.current_line)
            self.draw_actions.append(self.current_line_points)
            self.draw.line(self.current_line_points, fill="black", width=2)
        self.current_line = None
        self.current_line_points = []

    def clear_canvas(self):
        self.canvas.delete("all")
        self.setup_canvas()
        self.lines = []
        self.draw_actions = []

    def undo(self):
        if self.lines:
            last_line = self.lines.pop()
            self.canvas.delete(last_line)
            self.draw_actions.pop()
            self.redraw_image()

    def redraw_image(self):
        self.setup_canvas()
        for action in self.draw_actions:
            self.draw.line(action, fill="black", width=2)

    def save_canvas(self, filename):
        self.image.save(filename)