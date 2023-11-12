from pyautocad import Autocad, APoint
from Layer import Layer
from Paper import BluePrint
from Elevation import Elevation
from Steel_beam import SteelBeam
from Cross_section import TBeamSection


class Drawing:
    def __init__(self):
        acad = Autocad(create_if_not_exists=True)
        self.file = acad
        self.layers = {}
        self.blueprint = None
        self.elevation = None
        self.section = {}
        self.steelbeams = {}  # 储存各个钢束的块名称，便于插入立面图中

    def init_layers(self):  # 用于初始化图层
        self.layers["blueprint"] = Layer(self, "BluePrint")
        self.layers["steel"] = Layer(self, "SteelBeams")
        self.layers["bridge"] = Layer(self, "BridgeOutline")
        self.layers["dimension"] = Layer(self, "Dimensions")
        self.layers["decorate"] = Layer(self, "Decorates")

    def get_blueprint(self):  # 画出一张空白图纸
        self.blueprint = BluePrint(self, self.layers["blueprint"])
        self.blueprint.make_outline()
        self.blueprint.make_inner_table(4, 15, 350, 1000)
        self.blueprint.make_cost_table(7, 15, 350, 800, fix=1.9)

    def get_steelbeams(self):
        for i in range(1, 5):
            new_steel = SteelBeam(self, self.layers["steel"], i)
            new_steel.make_on_number()

    def get_elevation(self):
        self.elevation = Elevation(self)
        self.elevation.draw_bridge()
        self.elevation.add_steelbeam()
        self.elevation.add_decorator()

    def get_section(self):
        self.section[1] = TBeamSection(self, 1)
        self.section[1].make_section()
        self.section[2] = TBeamSection(self, 2)
        self.section[2].make_section()

    def add_my_name(self):
        name = self.file.model.AddText("FSReed.", APoint(17000, 5000), 500)
        name.Layer = self.layers["blueprint"].name
