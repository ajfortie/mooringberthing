""" This module will return the expected energy absorption and reaction for
    various floating fenders. Please note that the values reported can vary
    as much as ± 10% from the actual fender performance.
"""

import numpy as np
# Pneumatic Fender Curve
    # The performance curves described below are generalized curves
    # for pneumatic rubber fenders with an internal pressure of 50kPa.
    # The energy absorption is approximated by the 4th degree polynomial
    # listed below:
    #   E = 21.038(d)⁴ - 14.087(d)³ + 3.0646(d)² - 0.2055(d)
    #   R = 3.5054(d)³ - 0.236(d)² + 0.5336(d)

pneumatic_E = np.polynomial.Polynomial([0,-0.2055,3.9646,-14.087,21.038])
pneumatic_R = np.polynomial.Polynomial([0,0.5336,-0.236,3.5054])

# Hydropneumatic Fender Curve
    # The performance curves described below are generalized curves
    # for hydropneumatic rubber fenders with an internal pressure of 50kPa.
    # Values are interpolated from curves provided in NAVFAC TR-6064-OCN

hydropneumatic_E = np.polynomial.Polynomial([0,0.3992,-4.7441,58.567,-214.92,328.02])
hydropneumatic_R = np.polynomial.Polynomial([0,0.3992,-4.7441,58.567,-214.92,328.02])

# MV Leg Fender Curve
    # The performance curve described below is taken from the Trelleborg
    # Fender Design Manual for the MV Leg Fenders

MV_E = np.polynomial.Polynomial([0,0.0518,6.7381,-1.7559,-22.276,24.046])
MV_R = np.polynomial.Polynomial([0,6.5991,-5.4105,-32.671,47.616])

# Unit Leg Fender Curve
    # The performance curve described below is taken from the Trelleborg
    # Fender Design Manual for the Unit Leg Fender
Unit_Element_curve = [[0.000, 0.050, 0.100, 0.150, 0.200, 0.250, 0.300, 0.350, 0.400, 0.450, 0.500, 0.550, 0.575, 0.625],
                     [0.000, 0.010, 0.050, 0.120, 0.210, 0.320, 0.430, 0.540, 0.650, 0.750, 0.840, 0.950, 1.000, 1.130],
                     [0.000, 0.230, 0.470, 0.690, 0.870, 0.970, 1.000, 0.970, 0.900, 0.850, 0.840, 0.920, 1.000, 1.210]]

# Define Dictionary of all fender Curves:
Fenders = {"pneumatic"      :[pneumatic_E, pneumatic_R],
            "hydropneumatic"  :[hydropneumatic_E, hydropneumatic_R],
            "MV"              :[MV_E, MV_R],
            "unit fender"     :Unit_Element_curve}

def fender_reaction(x,E,R,fndr):

    #     
    # Definitions:
    #   x   = Berthing Energy to Fender
    #   E   = Energy Absorption at 60% Deflection
    #   R   = Fender Reaction at 60% Deflection
    #   fndr= Fender Type (str)
    #       "pneumatic" = pneumatic fender curve
    #       "MV"        = MV Fender Curve
    #       "unit"   = Unit Element Curve

    curve = Fenders[fndr]
    
    # Normalize Input Energy
    E_n = x/E

    E_curve = curve[0]-E_n
    R_curve = curve[1]
    # Root Counter
    ctr = 0
    
    for i in E_curve.roots():
        if (i.imag == 0) and (i.real >= 0):
            Deflection_N = i.real
            ctr += 1

    Reaction    = R_curve(Deflection_N) * R

    # Interpolate the fender reaction
    return [Deflection_N, Reaction]
