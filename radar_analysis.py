import numpy as np
import os
import seaborn as sns
import matplotlib.pyplot as plt
import argparse

plt.style.use('seaborn')


def parse_commandline():
    parser = argparse.ArgumentParser()
    parser.add_argument('--radar_type', '-rt',
                        choices=['new', 'old'], required=True)
    # parser.add_argument('--scheduler', '-s', type=str)
    args = parser.parse_args()
    return args


def main():
    args = parse_commandline()

    path = f"{args.radar_type}_radar"
    files = sorted([os.path.join(path, file) for file in os.listdir(path)])
    # fields = [x, y, z, rad_speed, RCS, Noise, Power, SNR]
    # Other things to check: No. of points, Flickering in the points

    snr = []
    noise = []
    power = []
    RCS = []
    rad_speed = []
    num_points = []

    for file in files:
        data = np.load(file)
        num_points.append(len(data))
        rad_speed.extend(data[:, 3])
        RCS.extend(data[:, 4])
        power.extend(data[:, 6])
        noise.extend(data[:, 5])
        snr.extend(data[:, 7])

    fig, axes = plt.subplots(2, 3, figsize=(16, 8))
    fig.suptitle(f"{args.radar_type} radars analysis")

    # first row
    sns.histplot(ax=axes[0, 0], data=np.array(rad_speed), bins=50)
    axes[0, 0].set_title("Rad speed")

    sns.kdeplot(ax=axes[0, 1], data=np.array(RCS), bw_adjust=0.7)
    axes[0, 1].set_title("RCS values")

    sns.kdeplot(ax=axes[0, 2], data=np.array(power), bw_adjust=0.9)
    axes[0, 2].set_title("power values")

    # Snd row
    sns.kdeplot(ax=axes[1, 0], data=np.array(noise), bw_adjust=0.5)
    axes[1, 0].set_title("Noise")

    sns.kdeplot(ax=axes[1, 1], data=np.array(snr), bw_adjust=0.5)
    axes[1, 1].set_title("snr values")

    sns.boxplot(ax=axes[1, 2], data=np.array(num_points))
    axes[1, 2].set_title("num-points")

    plt.show()
    # fig.savefig(f"{args.radar_type}_radar")


if __name__ == "__main__":
    main()
