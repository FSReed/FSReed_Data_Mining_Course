from pyautocad import Autocad, APoint, aDouble
from Basic_shapes import *


class TBeamSection:
    def __init__(self, File, number):
        self.File = File
        self.number = number

    # 梁截面数据格式为：
    # [
    # 0.块名称，
    # 1.上翼缘宽度，
    # 2.上翼板厚度，
    # 3.上翼板外凸长度
    # 4.腹板宽度，
    # 5.腹板上端距顶部距离，
    # 6.腹板下端距顶部距离，
    # 7.下翼缘宽度，
    # 8.下翼缘厚度，
    # 9.梁高度
    # 10.是否有肋板
    # ]
    Section_Data = {
        1: ["Section_1", 1500, 180, 180, 180, 340, 890, 500, 200, 1250, True],
        2: ["Section_2", 1500, 180, 340, 180, 314, 870, 500, 300, 1250, False],
    }

    bias_distance = 2000

    def make_section(self):
        Data = self.Section_Data[self.number]
        block = self.File.file.ActiveDocument.Blocks.Add(APoint(0, 0), Data[0])
        outline_seq = aDouble(
            Data[1] / 2,
            0,
            0,
            0,
            0,
            0,
            0,
            -Data[2],
            0,
            Data[3],
            -Data[2],
            0,
            (Data[1] - Data[4]) / 2,
            -Data[5],
            0,
            (Data[1] - Data[4]) / 2,
            -Data[6],
            0,
            (Data[1] - Data[7]) / 2,
            -(Data[9] - Data[8]),
            0,
            (Data[1] - Data[7]) / 2,
            -Data[9],
            0,
            Data[1] / 2,
            -Data[9],
            0,
        )
        axial_points = [
            APoint(Data[1] / 2, 0),
            APoint(Data[1] / 2, -100),
        ]
        outline = block.AddPolyLine(outline_seq)
        outline.mirror(axial_points[0], axial_points[1])
        if Data[10]:
            rib_seq = aDouble(
                0,
                -Data[2],
                0,
                0,
                -(Data[9] - Data[8]),
                0,
                (Data[1] - Data[7]) / 2,
                -(Data[9] - Data[8]),
                0,
            )
            rib_line = block.AddPolyLine(rib_seq)
            rib_line.mirror(axial_points[0], axial_points[1])
        section = self.File.file.model.InsertBlock(
            self.File.blueprint.section_point
            + APoint(self.bias_distance * (self.number - 1), 0),
            Data[0],
            1,
            1,
            1,
            0,
        )
        section.Layer = self.File.layers["bridge"].name
