from pyautocad import APoint
from math import pi
from Dimension import Dimension
from Decorate import Decorate


class SteelBeam:
    def __init__(self, File, layer, number):
        self.File = File
        self.layer = layer
        self.number = number
        self.blockname = None

    Size_data = {
        1: [-4101, 10000, 250, 270, -1210, 440, -5000],
        2: [-5966, 10000, 250, 270, -1600, 580, -8000],
        3: [-6634, 10000, 260, 270, -4747, 837, -11000],
        4: [-8028, 20000, 265, 270, -3356, 294, -14000],
    }

    def make_on_number(self):  # 钢束做好后，会将钢束块的名称储存起来方便插入
        name = "Length_25_Number_" + str(self.number)
        steel = self.File.file.ActiveDocument.Blocks.Add(APoint(0, 0), name)
        data = self.Size_data[self.number]
        steel.AddLine(APoint(0, 0), APoint(data[0], 0))
        arc = steel.AddArc(
            APoint(data[0], data[1]), data[1], data[2] / 180 * pi, data[3] / 180 * pi
        )
        start_point = APoint(arc.StartPoint)
        bias_point = start_point + APoint(data[4], data[5])
        steel.AddLine(start_point, bias_point)

        # 接下来制作钢束的尺寸标注

        origin_point = APoint(self.File.blueprint.bridge_point + APoint(0, data[6]))
        arc_start_point = origin_point + start_point
        arc_end_point = origin_point + APoint(data[0], 0)
        arc_center = origin_point + APoint(data[0], data[1])
        line_end_point = arc_start_point + APoint(data[4], data[5])
        dim_1 = Dimension(self.File, self.File.layers["dimension"])
        dim_1.Line_Dim(origin_point, arc_end_point)
        dim_2 = Dimension(self.File, self.File.layers["dimension"])
        dim_2.Radial_Dim(arc_center, arc_end_point, -700)
        dim_3 = Dimension(self.File, self.File.layers["dimension"])
        dim_3.Arc_Dim(
            arc_center,
            arc_start_point,
            arc_end_point,
            arc_start_point - APoint(0, 700),
        )
        dim_4 = Dimension(self.File, self.File.layers["dimension"])
        dim_4.Line_Dim(arc_start_point, line_end_point)

        decrt_1 = Decorate(self.File, self.File.layers["decorate"])
        decrt_1.make_circle(arc_start_point, 50)
        decrt_2 = Decorate(self.File, self.File.layers["decorate"])
        decrt_2.make_circle(line_end_point, 50)
        # 注意尺寸标注与修饰并不是钢束块的一部分

        steelbeam = self.File.file.model.InsertBlock(
            self.File.blueprint.bridge_point + APoint(0, data[6]), name, 1, 1, 1, 0
        )

        steelbeam.layer = self.layer.name
        self.File.steelbeams[self.number] = name  # 注意这里已经将对应块的名称存入了File的字典中
        self.blockname = name
