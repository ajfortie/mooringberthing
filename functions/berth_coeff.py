def Cbl(M, L, B, D, rho=64):
    # Determine block coefficient for vessel
    # per UFC 4-152-01 §5-2.1.1
    # Definitions:
    #   M   = Vessel displacement (LT)
    #   L   = Vessel Length (ft)
    #   B   = Vessel Beam (ft, width)
    #   D   = Vessel Draft (ft)
    #   rho = Density of Water (lb/ft³)
    #           Default = 64 lb/ft³

    return (M *2240)/(L * B * D * rho)

def k(Cbl, L):
    # Determine the vessel's radius of gyration
    # per Guidelines for the design of fender systems
    # PIANC, 2002
    # Definitions:
    #   Cbl = Block Coefficient
    #   L   = Vessel Length

    return (0.19 * Cbl + 0.11) * L

def Ce(k, a):
    # Determine eccentricity coefficient 
    # Definitions:
    #   k   = Radius of gyration in longitudinal dir (ft)
    #   a   = Distance from ship's center of gravit to point of contact

    return (k**2 / (a**2 + k**2))

def Cm(L, B, D, Cb, Wdepth, subflg = False):
    # Determine Virtual Mass Coefficient
    # Definitions:
    #   L       = Vessel Length (ft)
    #   B       = Vessel Beam (ft)
    #   D       = Vessel Draft (ft)
    #   Cb      = Berthing Factor (Ce x Cg x Cd x Cc)
    #   Wdepth  = Water Depth (ft)
    #   result  = Virtual Mass Coefficient
    if subflg:
        result = 2.36 + 1.74 * (D/Wdepth)**3.5
    else:
        if Cb < 0.6:
            F = 1.5 * Cb
        else:
            F = 0.9

        Cm0 = 1.3 + 1.5 * (D/B)
        Cm1 = F * (12.4 * (D/B)**0.3 - 50*(D/L))
        result = Cm0 + (Cm1 - Cm0) * (D/Wdepth)**3.5
    
    return result
