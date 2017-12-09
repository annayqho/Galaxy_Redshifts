""" Compare photo-z to spec-z in the redshift regime 0.1-0.3 """

import matplotlib.pyplot as plt
from matplotlib import rc
import h5py
rc("text", usetex=True)
rc("font", family="serif")
import numpy as np
import glob
from pandas.io.parsers import read_csv
import pandas as pd
from corner import hist2d
from matplotlib.colors import LogNorm


def load_data():
    """ load data """
    files = glob.glob("../data/0.1_0.3/*.csv")
    photoz = []
    photoz_err = []
    specz = []

    for ii,f in enumerate(files):
        print(f)
        df = pd.read_csv(f, usecols=['photo_z', 'spec_z', 'photo_z_err'],
            dtype={'photo_z': np.float64, 'spec_z': np.float64},
            na_values=['null'])
        photoz.extend(df['photo_z'].values)
        photoz_err.extend(df['photo_z_err'].values)
        specz.extend(df['spec_z'].values)

    photoz = np.array(photoz)
    photoz_err =np.array(photoz_err)
    specz = np.array(specz)
    choose = ~np.isnan(specz)
    return photoz, photoz_err, specz


def hist_specz(specz):
    # Histogram of z_s
    plt.hist(
            specz, color='k', histtype='step', 
            bins=10, range=(0,0.4))
    plt.yscale('log')
    plt.xlabel("Spec-z", fontsize=16)
    plt.ylabel("Num. Galaxies", fontsize=16)
    plt.tick_params(axis='both', labelsize=14)
    plt.show()


def hist_photoz():
    # Histogram of z_ph
    plt.hist(
            photoz, color='k', histtype='step', 
            bins=10, range=(0.1,0.3))
    plt.yscale('log')
    plt.xlabel("photo-z", fontsize=16)
    plt.ylabel("Num. Galaxies", fontsize=16)
    plt.tick_params(axis='both', labelsize=14)
    #plt.show()


def hist_photoz_err():
    # Histogram of z_ph err
    plt.hist(
            photoz_err, color='k', histtype='step', 
            bins=10)#, range=(0.1,0.3))
    plt.yscale('log')
    plt.xlabel("err in photo-z", fontsize=16)
    plt.ylabel("Num. Galaxies", fontsize=16)
    plt.tick_params(axis='both', labelsize=14)
    #plt.show()


def hist_compare(photoz, specz, choose):
    diff = (photoz[choose] - specz[choose])/specz[choose]
    plt.hist(
            diff, color='k', histtype='step',
            bins=20, range=(-1,1))
    plt.yscale('log')
    plt.xlabel("\% Diff: (photo-z -- spec-z)/spec-z", fontsize=16)
    plt.ylabel("Num. Galaxies", fontsize=16)
    plt.tick_params(axis='both', labelsize=14)


def plot_against(photoz, specz, choose):
    """ plot photoz and specz against each other """
    hist2d(photoz[choose], specz[choose], range=([0.1,0.3],[0.1,0.3]),
            bins=[100,100])
    plt.xlabel("Photometric Redshift", fontsize=16)
    plt.ylabel("Spec-z", fontsize=16)


if __name__=="__main__":
    photoz, photoz_err, specz = load_data()
    choose = photoz_err/(1+photoz) < 0.02
    has_specz = np.logical_and(choose, ~np.isnan(specz))
    plot_against(photoz, specz, has_specz)
