from pyautocad import APoint, aDouble
from Decorate import Decorate


class Elevation:
    def __init__(self, File):
        self.File = File
        self.bridge = None

    # Database中各个位置数据的意义：
    # 0. 桥梁立面图图块名称
    # 1. 桥梁立面图长度
    # 2. 桥梁立面图梁高
    # 3. 各个支点处肋板左端与跨中的距离(List),注意第一个元素为0，是为了方便迭代作图
    # 4. 肋板厚度
    # 5. T梁上翼缘的厚度
    # 6. T梁腹板上端距离桥面的距离
    # 7. T梁腹板下端距离桥面的距离
    # 8. T梁下翼缘的厚度
    # 9. T梁边跨变截面起点距离桥面的距离
    Database = [
        "Bridge_Elevation_Outline",
        12480,
        1250,
        [0, 2600, 7600, 12249.6],
        200,
        180,
        340,
        890,
        200,
        750.4,
    ]

    def draw_bridge(self):
        Data = self.Database
        name = Data[0]
        block = self.File.file.ActiveDocument.Blocks.Add(APoint(0, 0), name)
        outline_seq = aDouble(
            0, 0, 0, -Data[1], 0, 0, -Data[1], -Data[2], 0, 0, -Data[2], 0
        )
        block.AddPolyLine(outline_seq)
        point_set = []
        num_of_ribs = len(Data[3])
        position = 1
        while position < num_of_ribs:
            tmp_lst = [
                -Data[3][position - 1],
                -Data[5],
                0,
                -(Data[3][position] - Data[4]),
                -Data[5],
                0,
                -(Data[3][position] - Data[4]),
                -(Data[2] - Data[8]),
                0,
                -Data[3][position],
                -(Data[2] - Data[8]),
                0,
            ]
            point_set.extend(tmp_lst)
            # 以上添加了肋板关键点序列
            # -----------------------------
            if position != num_of_ribs - 1:
                block.AddLine(
                    APoint(-Data[3][position - 1], -Data[6]),
                    APoint(-(Data[3][position] - Data[4]), -Data[6]),
                )
                block.AddLine(
                    APoint(-Data[3][position - 1], -Data[7]),
                    APoint(-(Data[3][position] - Data[4]), -Data[7]),
                )
                block.AddLine(
                    APoint(-Data[3][position - 1], -(Data[2] - Data[8])),
                    APoint(-(Data[3][position] - Data[4]), -(Data[2] - Data[8])),
                )
            # 如果没到边跨，添加三条直线
            position += 1
        block.AddLine(
            APoint(-(Data[3][-1] - Data[4]), -Data[9]), APoint(-Data[3][-2], -Data[7])
        )
        block.AddLine(
            APoint(-(Data[3][-1] - Data[4]), -Data[9]),
            APoint(-Data[3][-2], -(Data[2] - Data[8])),
        )
        # 添加了两条变截面直线
        point_set.extend([-Data[3][-1], -Data[5], 0, -Data[1], -Data[5], 0])
        inside_seq = aDouble(point_set)
        block.AddPolyLine(inside_seq)
        # ---------以上用于添加轮廓线-------------------------------------------
        bridge = self.File.file.model.InsertBlock(
            self.File.blueprint.bridge_point, name, 1, 1, 1, 0
        )
        bridge.Layer = self.File.layers["bridge"].name
        self.bridge = bridge
        return bridge

    Position_data = {1: -890, 2: -890 - 140, 3: -890 - 140 - 120, 4: -890 - 140 - 120}
    # 这一项是各个钢束在桥梁立面图中的插入位置

    def add_steelbeam(self):
        for i in range(1, 5):
            bias_point = APoint(0, self.Position_data[i])
            steel = self.File.file.model.InsertBlock(
                self.File.blueprint.bridge_point + bias_point,
                self.File.steelbeams[i],
                1,
                1,
                1,
                0,
            )
            steel.Layer = self.File.layers["steel"].name

    def add_decorator(self):
        origin_point = self.File.blueprint.bridge_point
        Position = self.Database[3]
        for position in Position:
            if position == 0:
                dec = Decorate(self.File, self.File.layers["decorate"])
                dec.make_line(
                    origin_point + APoint(0, 200),
                    origin_point + APoint(0, -self.Database[2] - 200),
                )
                dec.object.Linetypescale = 0.01
            else:
                dec = Decorate(self.File, self.File.layers["decorate"])
                dec.make_line(
                    origin_point + APoint(-(position - self.Database[4] / 2), 200),
                    origin_point
                    + APoint(
                        -(position - self.Database[4] / 2), -self.Database[2] - 200
                    ),
                )
                dec.object.Linetypescale = 0.01
