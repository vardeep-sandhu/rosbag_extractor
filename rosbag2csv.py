#!/usr/bin/env python # [1]
"""\
This script converts the rosbag files which are captured for radars and 
converts them to the numpy arrays for each time stamp of the radar point cloud.

Usage: python rosbag2csv.py -rt [old, new]

"""
from pathlib import Path
import numpy as np
from rosbags.highlevel import AnyReader
import sensor_msgs_py.point_cloud2 as pc2
import argparse
import os


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('--radar_type', '-rt',
                        choices=['new', 'old'], required=True)
    # parser.add_argument('--scheduler', '-s', type=str)
    args = parser.parse_args()
    return args


def main():
    args = parse_commandline()

    curr_path = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(curr_path, f"{args.radar_type}_radar")
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    elif len(os.listdir(save_path)) != 0:
        for file_ in os.listdir(save_path):
            os.remove(os.path.join(save_path, file_))

    with AnyReader([Path(f'bags/{args.radar_type}_radar_bag')]) as reader:

        connections = [x for x in reader.connections]
        length_counter = 0
        for connection, timestamp, rawdata in reader.messages(connections=connections):
            msg = reader.deserialize(rawdata, connection.msgtype)
            num_points = msg.width

            columns = len(msg.fields)  # num fields
            names_fileds = [field.name for field in msg.fields]

            data = np.empty([num_points, len(names_fileds)])

            # data_list = pc2.read_points_list(msg)
            data_generator = pc2.read_points(msg)
            for idx, row in enumerate(data_generator):
                data[idx] = np.array(row)

            np.save(os.path.join(save_path, str(timestamp)), data)
            length_counter += 1
            print("*******************************")
            # break
        print("Number of point clouds saved: ", length_counter)
        print("cloud saved")


if __name__ == "__main__":
    main()
