# 用于数据处理与画图的模块

import numpy as np
import matplotlib.pyplot as plt
from Basic_Configuration import *


def Get_Origin_Data(database, boat_num, source, detect_range):
    assert boat_num > 0 and boat_num <= len(categories), "No such boat in the database."
    assert detect_range in Ranges, "No such detect_range in Basic_Configuration."
    boat = f"boat{boat_num}"
    boundary = Ranges[detect_range]
    (min_detect_range, max_detect_range) = boundary
    coordinates = database.execute(
        f"SELECT x, y FROM {Name_Of_Database} WHERE BoatName = '{boat}' and Source = '{source}' and x >= {min_detect_range} and x < {max_detect_range};"
    ).fetchall()
    return np.array(coordinates)


def Get_Fixed_Data(database, boat_num):
    assert boat_num > 0 and boat_num <= len(categories), "No such boat in the database."
    boat = f"boat{boat_num}"
    coordinates = database.execute(
        f"SELECT avg(x), avg(y) FROM Boatdata WHERE boatname = '{boat}' GROUP BY timestamp;"
    ).fetchall()
    return np.array(coordinates)


def Draw_Track_From(database, boat_num, detect_range, show_fixed_track=False):
    boat = f"boat{boat_num}"
    sources = categories[boat]
    fig, ax = plt.subplots()
    for point_of_view in sources:
        lst = Get_Origin_Data(database, boat_num, point_of_view, detect_range)
        if lst.shape[0] == 0:
            continue
        style = Track_Line_Config[point_of_view]
        ax.plot(lst[:, 0], lst[:, 1], style, label=point_of_view)
        ax.set_xlabel("X/(m)")
        ax.set_ylabel("Y/(m)")
        ax.set_xlim(Ranges[detect_range])
        ax.set_ylim(Y_Limit[detect_range])
        ax.set_title(f"{boat}: {detect_range}")
    if show_fixed_track:
        lst = Get_Fixed_Data(database, boat_num)
        ax.plot(lst[:, 0], lst[:, 1], Fixed_Line_Config, label="Fixed_Track")
    plt.legend()


def Get_Pictures(
    database, Interested_boat, Interested_spectrum, show_fixed_track=False
):
    boat_nums = [boat for boat in Interested_boat if Interested_boat[boat]]
    spectrums = [spec for spec in Interested_spectrum if Interested_spectrum[spec]]
    for boat in boat_nums:
        for spec in spectrums:
            Draw_Track_From(database, boat, spec, show_fixed_track)
