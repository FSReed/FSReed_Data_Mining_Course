class Layer:
    def __init__(self, File, name):
        self.File = File
        self.layer = File.file.ActiveDocument.Layers.Add(name)
        self.name = self.layer.name
