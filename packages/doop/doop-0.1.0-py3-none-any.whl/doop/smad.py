import numpy as np
from numpy import pi, sqrt, log10
from .constants import Earth

# Add some SMAD calculations here

def period(a):
    # a [km] -> period [sec]
    return 2*pi*sqrt(a**3/Earth.mu)

def dnode(period):
    """
    Orbit nodal precession on each rev. Orbits below GEO move (drift) Westerly
    while orbits above GEO move Easterly. Orbits at GEO are stationary, 0 deg drift.
    Use siderial day rotation for better accuracy.

    Arg:
    period [sec]
    Return:
    node precession (dn) [deg]
    """
    return 360 - 360/(23*3600+56*60+4)*period

def antennaGain(Dia,freq, efficiency=0.7):
    """Simple parabolic antenna

    - Dia: meters
    - freq: Hz
    - efficiency: 0.0 - 1.0
    """
    c = 3*10**8 # m/s
    lamda = c/freq # m
    return 10*log10((pi**2 * Dia**2 * efficiency)/lamda**2)

def receivePointingLoss(ptError, halfPwrBW):
    """Pointing error loss based off of error of pointing antenna and half power beamwidth

    - ptError: degrees
    - halfPwrBW: degrees
    """
    return -12*(ptError/halfPwrBW)**2

def spaceLoss(frequency, distance):
    """Free space loss

    - frequency: Hz
    - distance: m (not km)
    """
    c = 3*10**8 # m/s
    return 10*log10((c/(4*pi*distance*frequency))**2)

def EbNo(TX, RX, datarate, frequency, distance):
    """ Calculate the signal vs noise

    - TX: dict
    - RX: dict
    - datarate: bits per second
    - frequency: Hz
    - distance: m (not km)
    """
    Ls = spaceLoss(frequency, distance)
    eirp = TX["eirp"]

    if "G/T" in RX:
        GT = RX["G/T"]
    else:
        Gr = RX["gain"]
        Ts = RX["sysNoiseTemp"]
        GT = Gr - 10*log10(Ts)

    ptErr = RX["pointingError"]
    hpbw = RX["halfPowerBW"]
    Lpr = receivePointingLoss(ptErr, hpbw)
    pp = -0.3
    K = -228.6 # Boltzman const
    ebno = eirp + Lpr + Ls + pp - K + GT - 10*log10(datarate)
    return ebno
