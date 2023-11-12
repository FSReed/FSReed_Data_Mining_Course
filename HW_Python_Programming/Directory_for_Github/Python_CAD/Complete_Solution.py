from File import Drawing
from Basic_shapes import beam_bottom_curve

#  如果运行出现问题请查看Readme.txt中的说明， 如果还不行， 文件内也包含了Complete_Solution.dwg, 是
#  用这些python文件画出的图纸成品

CAD_File = Drawing()
CAD_File.init_layers()
CAD_File.add_my_name()
CAD_File.get_blueprint()
CAD_File.get_steelbeams()
CAD_File.get_elevation()
CAD_File.get_section()

# 下面一行是展示本库中提供的抛物线的精确拟合画法的， 如果想看效果可以取消注释并运行(起初是想画变截面梁用的，后来发现不需要抛物线变截面)
# beam_bottom_curve(CAD_File.file.model, 30000, 0, 34000, 5000, 39000, 4000, 1000)
