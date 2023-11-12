from pyautocad import APoint


class Dimension:
    def __init__(self, File, layer, size=300):
        self.File = File
        self.layer = layer
        self.dimension = None
        self.size = size

    def Line_Dim(self, start_node, end_node, text_position=False):
        if text_position:
            self.dimension = self.File.file.model.AddDimAligned(
                start_node, end_node, text_position
            )
        else:
            self.dimension = self.File.file.model.AddDimAligned(
                start_node, end_node, (start_node + end_node) / 2 + APoint(0, self.size)
            )
        self.dimension.TextHeight = self.size
        self.dimension.ArrowheadSize = self.size
        self.dimension.Layer = self.File.layers["dimension"].name

    def Radial_Dim(self, Center, ChordPoint, LeaderLength):
        self.dimension = self.File.file.model.AddDimRadial(
            Center, ChordPoint, LeaderLength
        )
        self.dimension.TextHeight = self.size
        self.dimension.ArrowheadSize = self.size
        self.dimension.Layer = self.File.layers["dimension"].name

    def Arc_Dim(self, ArcCenter, FirstEndPoint, SecondEndPoint, ArcPoint):
        self.dimension = self.File.file.model.AddDimArc(
            ArcCenter, FirstEndPoint, SecondEndPoint, ArcPoint
        )
        self.dimension.TextHeight = self.size
        self.dimension.ArrowheadSize = self.size
        self.dimension.Layer = self.File.layers["dimension"].name
