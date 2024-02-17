import numpy as np
from numpy.fft import fft, fftfreq
import scipy.stats
from scipy.signal import butter, lfilter, welch, square  # for signal filtering
from modules.cont_utils import *
import sys


def to_PSD(frame, samplerate = 1000):
    frequencies, psd = welch(frame, fs = samplerate,
                             window = 'hanning',  # apply a Hanning window before taking the DFT
                             nperseg = 256,  # compute periodograms of 256-long segments of x
                             detrend = 'constant', scaling = "spectrum")  # detrend x by subtracting the mean
    return psd, frequencies


def to_updatedPSD(frame, samplerate = 1000, output_length = 256):
    frequencies, psd = welch(frame, fs = samplerate,
                             window = 'hanning',  # apply a Hanning window before taking the DFT
                             nperseg = 2048,  # compute periodograms of 256-long segments of x
                             # noverlap = 512,
                             detrend = 'constant', scaling = "spectrum")  # detrend x by subtracting the mean

    return psd, frequencies


def splitFreqBandLimit(rawEMGPowerSpectrum, frequencies, bandLimitDict):
    splitDict = dict()
    i = 0

    for key in bandLimitDict:
        splitDict[i] = dict()
        splitDict[i]['emgPS'] = rawEMGPowerSpectrum[
                                int(len(frequencies) * bandLimitDict[key][0] / 500) + 1:int(
                                    len(frequencies) * bandLimitDict[key][1] / 500) + 1]
        splitDict[i]['freq'] = frequencies[
                               int(len(frequencies) * bandLimitDict[key][0] / 500) + 1:int(
                                   len(frequencies) * bandLimitDict[key][1] / 500) + 1]

        i += 1

    return splitDict


def to_BL_MNF(rawEMGPowerSpectrum, frequencies):
    a = []
    for i in range(0, len(frequencies)):
        a.append(frequencies[i] * rawEMGPowerSpectrum[i])
    b = sum(rawEMGPowerSpectrum)
    MNF = sum(a) / b
    return MNF


def to_MNF(frame):
    """
    Obtain the mean frequency of the EMG signal, evaluated as the sum of
    product of the EMG power spectrum and the frequency divided by total sum of the spectrum intensity:
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    a = []
    for i in range(0, len(frequencies)):
        a.append(frequencies[i] * rawEMGPowerSpectrum[i])
    b = sum(rawEMGPowerSpectrum)

    MNF = sum(a) / b
    return MNF


def to_MDF(frame):
    """
    Obtain the Median Frequency of the PSD.
    MDF is a frequency at which the spectrum is divided into two regions with equal amplitude, in other words, MDF is half of TTP feature
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    MDF = sum(rawEMGPowerSpectrum) * (1 / 2)
    for i in range(1, len(rawEMGPowerSpectrum)):
        if (sum(rawEMGPowerSpectrum[0:i]) >= MDF):
            return frequencies[i]
    return np.NaN


def mdf_calc_inside(rawEMGPowerSpectrum, frequencies):
    MDF = sum(rawEMGPowerSpectrum) * (1 / 2)
    for i in range(1, len(rawEMGPowerSpectrum)):
        if (sum(rawEMGPowerSpectrum[0:i]) >= MDF):
            return frequencies[i]


def to_PKF(frame):
    """
    Obtain the frequency at which the maximum peak occur.
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    peakFrequency = frequencies[np.argmax(rawEMGPowerSpectrum)]
    return peakFrequency


def to_MNP(frame):
    """
    This functions evaluate the mean power of the spectrum.
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    MNP = np.mean(rawEMGPowerSpectrum)
    return MNP


def to_TTP(frame):
    """
    This functions evaluate the aggregate of the EMG power spectrum (aka Zero Spectral Moment)
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    TTP = sum(rawEMGPowerSpectrum)
    return TTP


def to_SM(frame, order = 1):
    """
    Get the spectral moment of a spectrum.
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    SMo = []
    for j in range(0, len(frequencies)):
        SMo.append(frequencies[j] * (rawEMGPowerSpectrum[j] ** order))
    SMo = sum(SMo)
    return (SMo)


def to_FR(frame, llc = 30, ulc = 250, lhc = 250, uhc = 500):
    """
    This functions evaluate the frequency ratio of the power spectrum.
    Cut-off value can be decidec experimentally or from the MNF Feature See: Oskoei, M.A., Hu, H. (2006). GA-based feature subset selection for myoelectric classification.
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    frequencies = list(frequencies)
    # First we check for the closest value into the frequency list to the cutoff frequencies
    llc = min(frequencies, key = lambda x: abs(x - llc))
    ulc = min(frequencies, key = lambda x: abs(x - ulc))
    lhc = min(frequencies, key = lambda x: abs(x - lhc))
    uhc = min(frequencies, key = lambda x: abs(x - uhc))

    LF = sum(
        [P
         for P in rawEMGPowerSpectrum
         [frequencies.index(llc): frequencies.index(ulc)]])
    HF = sum(
        [P
         for P in rawEMGPowerSpectrum
         [frequencies.index(lhc): frequencies.index(uhc)]])
    FR = LF / HF
    return FR


def to_PSR(frame, n = 20, fmin = 0, fmax = 500):
    """
    This function computes the Power Spectrum Ratio of the signal, defined as:
    Ratio between the energy P0 which is nearby the maximum value of the EMG power spectrum and the energy P which is the whole energy of the EMG power spectrum
    """
    rawEMGPowerSpectrum, frequencies = to_PSD(frame)
    frequencies = list(frequencies)

    # The maximum peak and frequencies are evaluate using the getPeakFrequency functions
    # First we check for the closest value into the frequency list to the cutoff frequencies
    peakFrequency = to_PKF(frame)
    f0min = peakFrequency - n
    f0max = peakFrequency + n
    f0min = min(frequencies, key = lambda x: abs(x - f0min))
    f0max = min(frequencies, key = lambda x: abs(x - f0max))
    fmin = min(frequencies, key = lambda x: abs(x - fmin))
    fmax = min(frequencies, key = lambda x: abs(x - fmax))

    # here we evaluate P0 and P
    P0 = sum(
        rawEMGPowerSpectrum
        [frequencies.index(f0min): frequencies.index(f0max)])
    P = sum(
        rawEMGPowerSpectrum
        [frequencies.index(fmin): frequencies.index(fmax)])
    PSR = P0 / P

    return PSR


def to_VCF(SM0, SM1, SM2):
    """
    This function evaluate the variance of the central freuency of the PSD.
    """
    VCF = (SM2 / SM0) - (SM1 / SM0) ** 2
    return VCF
