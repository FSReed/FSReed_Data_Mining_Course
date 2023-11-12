from pyautocad import APoint


class Decorate:
    def __init__(self, File, layer):
        self.File = File
        self.layer = layer
        self.object = None

    def make_circle(self, center, radium):
        circle = self.File.file.model.AddCircle(center, radium)
        circle.Layer = self.layer.name
        self.object = circle

    def make_line(self, start_node, end_node):
        line = self.File.file.model.AddLine(start_node, end_node)
        line.Layer = self.layer.name
        self.object = line
