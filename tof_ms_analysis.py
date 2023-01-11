import h5py
import numpy as np
import matplotlib.pyplot as plt

from scipy import optimize
from jcamp import jcamp_readfile


def reduce_res(array, factor):
    """
    Reduce tof histogram resolution by binning.
    Takes a data array and integer factor.
    Returns a 1D array.
    """
    counts = []
    count_sum = 0
    for i in range(len(array)):
        if (i % factor) == 0:
            counts.append(count_sum)
            count_sum = 0
        count_sum = count_sum + array[i]
    return np.array(counts)


def read_jdx(filename):
    """
    Reads a jdx file downloaded from the nist database.
    Takes a filename.
    Returns the mz and amplitude values.
    """
    data = jcamp_readfile(filename)
    return data["x"], data["y"]


def mz_parabola(x, factor, offset):
    """
    Defines a parabola for bin-to-mz calibration fits.
    Takes bin (x), factor and offset.
    Returns the mz (y value).
    """
    y = factor * (x - offset) ** 2
    return y


def mz_calibration(histo, bins, masses, plot=True, p0=[1e-6, 0]):
    """
    Generates a mz axis by fitting the given data points.
    Takes histogram array, lists of bins and masses (data points to fit).
    A plot is generated as default. Initial fit parameters can be defined.
    """
    popt, pcov = optimize.curve_fit(mz_parabola, bins, masses, p0)
    mz_axis = mz_parabola(np.arange(0, len(histo), 1), popt[0], popt[1])
    if plot:
        fig, ax = plt.subplots(figsize=(9, 5))
        ax.plot(mz_axis, histo, '-', color='k')
        ax.set(xlabel='m/z', ylabel='Counts', xlim=[np.min(mz_axis), np.max(mz_axis)])
        ax.text(0.8, 0.9, f'a = {popt[0]:.3E}\nb = {popt[1]:.3E}', transform=ax.transAxes)
    return mz_axis


def tof_select(loc, ix):
    with h5py.File(loc, 'r') as f:
        tof_list = list(f.keys())[0]

        # Creating a list for the files in TOF
        x = []
        for _ in f[tof_list]:
            x.append(_)

        tof_nr = f[tof_list][x[abs(round(ix))]]
        tof_spectrum = np.squeeze(tof_nr['TOF0'])
        lr_spec = reduce_res(tof_spectrum, 30)
        mz = mz_calibration(lr_spec, bins=[10235, 11087, 15182], masses=[69, 81, 152], plot=False)

        ampl = lr_spec / np.max(lr_spec)
        nist_data = []
        mz_jdx, ampl_jdx = read_jdx('Data/nist_data.jdx')
        ampl_jdx = ampl_jdx / np.max(ampl_jdx)
        nist_data.append((mz_jdx, ampl_jdx))

        return mz, ampl, nist_data
