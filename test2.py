import h5py
import matplotlib.pyplot as plt
import numpy as np

filename1 = "example.h5"

with h5py.File(filename1, "r") as f:
    # get first object name/key; may or may NOT be a group
    electron_list = list(f.keys())[0]
    tof_list = list(f.keys())[1]

    # preferred methods to get dataset values:
    electron_images = f[electron_list][()]  # returns as a numpy array
    tof_spectrum = f[tof_list][()]

    tof = np.squeeze(tof_spectrum)

    plt.plot(tof)
    plt.show()

    for i in range(10):
        plt.subplot(2, 5, 1 + i)
        plt.imshow(electron_images[i])
    plt.show()

filename2 = "scan_example.h5"

with h5py.File(filename2, "r") as f:
    # get first object name/key; may or may NOT be a group
    a_group_key = list(f.keys())[0]

    # preferred methods to get dataset values:
    ds_arr = f[a_group_key]['data_point_000001']  # returns as a numpy array
    print(len(f[a_group_key]))

    x = []
    for _ in f[a_group_key]:
        x.append(_)
        # if _ == 'scan_data':
        #     break
        #     # plt.plot(f[a_group_key][_])
        #     # plt.show()
        # else:
        #     ds_arr = f[a_group_key][_]
        #     test = np.squeeze(ds_arr['TOF0'])
        #     plt.plot(test)
    # plt.show()
    print(x)
