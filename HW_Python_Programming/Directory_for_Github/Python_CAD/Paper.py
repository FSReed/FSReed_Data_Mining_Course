from pyautocad import APoint
from Basic_shapes import *
from math import pi


class BluePrint:
    def __init__(
        self,
        File,
        layer,
        width=28000,
        height=20000,
        lower_left=APoint(0, 0),
    ):
        self.File = File
        self.layer = layer
        self.width = width
        self.height = height
        self.lower_left = lower_left
        self.bridge_point = lower_left + APoint(width / 2, height * 0.8)
        self.section_point = self.bridge_point + APoint(width / 10, 0)

    def make_outline(self, bias_x=1500, bias_y=1000):  # 制作图纸的外轮廓
        """Create the frame of the paper."""
        name = "Frame"
        frame = self.File.file.ActiveDocument.Blocks.Add(APoint(0, 0), name)
        make_rectangle(frame, self.width, self.height, fixlineweight=40)
        make_rectangle(
            frame,
            self.width + 2 * bias_x,
            self.height + 2 * bias_y,
            -bias_x,
            -bias_y,
            fixlineweight=False,
        )
        outline = self.File.file.model.InsertBlock(self.lower_left, name, 1, 1, 1, 0)
        outline.Layer = self.layer.name
        return outline

    def make_inner_table(self, num_of_rolls, num_of_cols, row_height, col_length):
        # 制作图纸底部的表格
        name = "Blueprint's inner table."
        table = self.File.file.ActiveDocument.Blocks.Add(APoint(0, 0), name)
        table.AddTable(APoint(0, 0), num_of_rolls, num_of_cols, row_height, col_length)
        bias_point = APoint(-num_of_cols * col_length, num_of_rolls * row_height)
        inner_table = self.File.file.model.InsertBlock(
            self.lower_left + APoint(self.width, 0) + bias_point, name, 1, 1, 1, 0
        )
        inner_table.Layer = self.layer.name
        return inner_table

    def make_cost_table(
        self, num_of_rolls, num_of_cols, row_height, col_length, fix=1.9
    ):
        # 制作内部工程量表格, fix用于调整图表的位置而非大小
        name = "Blueprint's cost table."
        table = self.File.file.ActiveDocument.Blocks.Add(APoint(0, 0), name)
        table.AddTable(APoint(0, 0), num_of_rolls, num_of_cols, row_height, col_length)
        bias_point = APoint(self.width / fix, self.height / fix)
        inner_table = self.File.file.model.InsertBlock(
            self.lower_left + bias_point, name, 1, 1, 1, 0
        )
        inner_table.Layer = self.layer.name
        return inner_table
