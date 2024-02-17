import numpy as np
import math
from scipy.signal import square
import peakutils


def to_ZCR(frame):  # zcr hesaplama
    asign = np.sign(frame)
    signchange = ((np.roll(asign, 1) - asign) != 0).astype(int)
    zcr = 0
    for k in range(1, frame.shape[0]):

        zcr = zcr + np.abs(signchange[int(k)]-signchange[int(k)-1])

    zcr = zcr/(2*frame.shape[0])
    return zcr


def to_MCR(frame):
    mean_crossing_indices = np.nonzero(
        np.diff(np.array(frame) > np.nanmean(frame)))[0]
    no_mean_crossings = len(mean_crossing_indices)
    return no_mean_crossings


def to_RMS(frame):
    """ 
    Get the root mean square of a signal.
    """
    RMS = np.sqrt(np.mean(np.square(frame)))
    return RMS


def to_MAV(frame):
    """ 
    This functions compute the  average of EMG signal Amplitude.
    """
    MAV = np.nanmean(np.absolute(frame))
    return MAV


def to_MAV1(frame):
    """ 
    This functoin evaluate Average of EMG signal Amplitude, using the modified version n°.1.
    """
    wIndexMin = int(0.25 * len(frame))
    wIndexMax = int(0.75 * len(frame))
    absoluteSignal = [abs(x) for x in frame]
    IEMG = 0.5 * np.sum([x for x in absoluteSignal[0: wIndexMin]]) + np.sum([x
                                                                             for x in absoluteSignal[wIndexMin: wIndexMax]]) + 0.5 * np.sum([x
                                                                                                                                             for x in absoluteSignal[wIndexMax:]])
    MAV1 = IEMG / len(frame)
    return MAV1


def to_MAV2(frame):
    """ 
    This functoin evaluate Average of EMG signal Amplitude, using the modified version n°.2.
    """
    N = len(frame)
    wIndexMin = int(0.25 * N)  # get the index at 0.25N
    wIndexMax = int(0.75 * N)  # get the index at 0.75N

    temp = []  # create an empty list
    for i in range(0, wIndexMin):  # case 1: i < 0.25N
        x = abs(frame[i] * (4*i/N))
        temp.append(x)
    for i in range(wIndexMin, wIndexMax+1):  # case2: 0.25 <= i <= 0.75N
        x = abs(frame[i])
        temp.append(x)
    for i in range(wIndexMax+1, N):  # case3; i > 0.75N
        x = abs(frame[i]) * (4*(i - N) / N)
        temp.append(x)

    MAV2 = np.sum(temp) / N
    return MAV2


def to_SSI(frame):
    """ 
    This function compute the summation of square values of the EMG signal.
    """
    SSI = np.sum(np.square(frame))
    return SSI


def to_VAR(frame):
    """ 
    Summation of average square values of the deviation of a variable.
    """
    SSI = to_SSI(frame)
    N = len(frame)
    VAR = SSI * (1 / (N - 1))
    return VAR


def to_TM(frame, order):
    """ 
    This function compute the Temporal Moment of order X of the EMG signal.
    """
    N = len(frame)
    TM = abs((1/N) * np.sum([x**order for x in frame]))
    return TM


def to_LOG(frame):
    """     
    # LOG is a feature that provides an estimate of the muscle contraction force.
    """
    LOG = math.exp(np.mean(np.abs(frame)))
    return LOG


def to_IEMG(frame):
    """     
    This function compute the sum of absolute values of EMG signal Amplitude.
    """
    IEMG = np.sum(np.abs(frame))
    return IEMG


def to_WL(frame):
    """     
    Get the waveform length of the signal, a measure of complexity of the EMG Signal.
    """
    L = len(frame)
    WL = 0
    for i in range(1, L):
        WL += np.abs(frame[i] - frame[i-1])
    return WL


def to_AAC(frame):
    """     
    Get the Average amplitude change.
    """
    N = len(frame)
    WL = to_WL(frame)
    AAC = 1/N * WL
    return AAC


def to_DASDV(frame):
    """ 
    Get the standard deviation value of the the wavelength.
    """
    N = len(frame)
    temp = []
    for i in range(0, N-1):
        temp.append((frame[i+1] - frame[i])**2)
    DASDV = (1 / (N - 1)) * sum(temp)
    return DASDV


def to_AFB(frame, samplerate, windowSize=32):
    """ 
    Get the amplitude at first Burst.
    """
    squaredSignal = square(frame)  # squaring the signal
    # get the number of samples for each window
    windowSample = int((windowSize * 1000) / samplerate)
    w = np.hamming(windowSample)
    # From: http://scipy-cookbook.readthedocs.io/items/SignalSmooth.html
    filteredSignal = np.convolve(w/w.sum(), squaredSignal, mode='valid')
    peak = peakutils.indexes(filteredSignal)[0]
    AFB = filteredSignal[peak]
    return AFB


def to_ZC(frame, threshold):
    """ 
    How many times does the signal crosses the 0 (+-threshold).
    """
    positive = (frame[0] > threshold)
    ZC = 0
    for x in frame[1:]:
        if(positive):
            if(x < 0 - threshold):
                positive = False
                ZC += 1
        else:
            if(x > 0 + threshold):
                positive = True
                ZC += 1
    return ZC


def to_MYOP(frame, threshold):
    """ 
    The myopulse percentage rate (MYOP) is an average value of myopulse output.
    It is defined as one absolute value of the EMG signal exceed a pre-defined thershold value.
    """
    N = len(frame)
    MYOP = len([1 for x in frame if abs(x) >= threshold]) / N
    return MYOP


def to_WAMP(frame, threshold):
    """ 
    Wilson or Willison amplitude is a measure of frequency information.
    It is a number of time resulting from difference between the EMG signal of two adjoining segments, that exceed a threshold.::
    """
    N = len(frame)
    WAMP = 0
    for i in range(0, N-1):
        x = frame[i] - frame[i+1]
        if(x >= threshold):
            WAMP += 1
    return WAMP


def to_SSC(frame, threshold=0.01):
    """ 
    Number of times the slope of the EMG signal changes sign.
    """
    N = len(frame)
    SSC = 0
    for i in range(1, N-1):
        a, b, c = [frame[i-1], frame[i], frame[i+1]]
        if(a + b + c >= threshold * 3):  # computed only if the 3 values are above the threshold
            if(a < b > c or a > b < c):  # if there's change in the slope
                SSC += 1
    return SSC


def to_MAVSLPk(frame, nseg):
    """ 
    Mean Absolute value slope is a modified versions of MAV feature.
    """
    N = len(frame)
    lenK = int(N / nseg)  # length of each segment to compute
    MAVSLPk = []
    for s in range(0, N, lenK):
        MAVSLPk.append(to_MAV(frame[s:s+lenK]))
    return MAVSLPk


def to_HIST(frame, nseg=9, threshold=50):
    """ 
    Histograms is an extension version of ZC and WAMP features.
    """
    segmentLength = int(len(frame) / nseg)
    HIST = {}
    for seg in range(0, nseg):
        HIST[seg+1] = {}
        thisSegment = frame[seg * segmentLength: (seg+1) * segmentLength]
        HIST[seg+1]["ZC"] = to_ZC(thisSegment, threshold)
        HIST[seg+1]["WAMP"] = to_WAMP(thisSegment, threshold)
    return HIST


def to_skewness(frame):
    L = len(frame)
    x_hat = np.nanmean(frame)
    std = np.nanstd(frame)
    skewness = 0
    for i in range(L):
        skewness += (((frame[i] - x_hat) / std)**3)
    return skewness / L


def to_Activity(x):
    L = len(x)
    x_hat = np.nanmean(x)
    Activity = 0
    for i in range(L):
        Activity += ((x[i] - x_hat)**2)/L
    return Activity


def to_Mobility(x):
    x_der = np.gradient(x)
    a = to_Activity(x_der)
    b = to_Activity(x)
    Mobility = np.sqrt(a/b)

    return Mobility


def to_Complexity(x):
    x_der = np.gradient(x)
    a = to_Mobility(x_der)
    b = to_Mobility(x)

    Complexity = a/b

    return Complexity


def to_Hjort(frame):
    Activity = to_Activity(frame)
    Mobility = to_Mobility(frame)
    Complexity = to_Complexity(frame)

    return [Activity, Mobility, Complexity]


def to_slope_change_rate(frame):
    L = len(frame)
    second_discrete_derivative = np.diff(np.diff(frame))
    slp_chg_rate = np.count_nonzero(second_discrete_derivative) / L
    return slp_chg_rate


def to_stats(frame):
    n5 = np.nanpercentile(frame, 5)
    n25 = np.nanpercentile(frame, 25)
    n75 = np.nanpercentile(frame, 75)
    n95 = np.nanpercentile(frame, 95)
    median = np.nanpercentile(frame, 50)
    mean = np.nanmean(frame)
    std = np.nanstd(frame)
    var = np.nanvar(frame)
    return [n5, n25, n75, n95, median, mean, std, var]
