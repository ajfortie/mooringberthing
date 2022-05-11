"""This package will determine the berthing energy of the requested vessels, 
plot these energies on fender reaction curves, and generate the resulting
reactions.
"""
import csv

from .functions import berth_coeff as bc
from .functions import fndr_curves as fc
from .functions import fndr_plot as plt
from .functions import berthvel as bv

def berthing_energy(vessels, berths, loadcases, fender_dict, output):
    """Determine berthing energies using UFC 4-152-01 based on guidance from
    PIANC 2002.  Output units are (kip, ft)"""
    # Initialize Dictionaries
    Eberth_arr = {}
    Rberth_arr = {}
    Dberth_arr = {}
    results = {}

    for i in fender_dict.keys():
        results[i] = []
        Eberth_arr[i] = []
        Rberth_arr[i] = []
        Dberth_arr[i] = []

    # Field names used for CSV output
    fldnms = ['Vessel', 'Load Case','Berthing Condition','Acc. Factor', 'Berthing Configuration', 
            'Water Depth', 'Displacement','Length','Beam','Draft','CoG',
            'No. Fenders','Fender Name','Fender Type',
            'Rated Energy', 'Rated Reaction', 'Rated Deflection','Vel', 'Cbl', 
            'k_r', 'Cg', 'Cd', 'Cc', 'Ce', 'Cb', 'Cm','Eship', 'Deflection', 
            'Energy', 'Reaction']

    for i, key in enumerate(vessels):
        # Assign variables for the current vessel
        M = vessels[key][0]             # Vessel Displacement
        L = vessels[key][1]             # Vessel Length
        B = vessels[key][2]             # Vessel Beam
        D = vessels[key][3]             # Vessel Draft
        CG = vessels[key][4]            # Center of Gravity
        Cbl = bc.Cbl(M, L, B, D)        # Block Factor
        k_r = bc.k(Cbl, L)              # Radius of Gyration
        Cd = vessels[key][5]            # Deformation Factor
        loc_berths = vessels[key][8]

        for j, jtem in enumerate(loc_berths):
            loc_fndr_key = (berths[jtem][1])
            mudline= berths[jtem][0]      # Mudline
            bcond = berths[jtem][2]
            V = bv.velocity(M, bcond)   # Berthing Velocity
            Cc = berths[jtem][3]        # Configuration Factor

            fender_type = fender_dict[loc_fndr_key][0]
            E_rating = fender_dict[loc_fndr_key][1]
            R_rating = fender_dict[loc_fndr_key][2]
            D_rating = fender_dict[loc_fndr_key][3]

            # Calculate Ship Energy
            Eship = 0.5 * M * 2.240 * V**2 / 32.2
            for k in loadcases:
                config = loadcases[k][0]
                ABF = loadcases[k][1]
                if ABF == 1:
                    case = 'Operational'
                else:
                    case = 'Accidental'
                Cg = loadcases[k][2]
                wdepth = loadcases[k][3] - mudline

                # Define Number of Fenders and Eccentricity
                match config:
                    case 'Broadside':
                        nfndr = vessels[key][6]
                        a = 0
                    case 'Corner Protection':
                        nfndr = 1
                        a = 0
                    case 'Forward Quarter Point':
                        nfndr = 1
                        a = abs(CG-L/4)
                    case 'Rear Quarter Point':
                        nfndr = 1
                        a = abs(3*L/4-CG)
                
                Ce = bc.Ce(k_r,a)       # Eccentricity Coefficient Forward Fender

                # Berthing Coefficients:
                Cb = Ce * Cg * Cd * Cc

                # Virtual Mass Coefficient
                Cm = bc.Cm(L, B, D, Cb, wdepth, vessels[key][7])

                # Calculate Fender Energy (includes 10% increase for uncertainty)
                Efndr = ABF * Cm * Cb * Eship / nfndr * 1.1

                if ((config == 'Corner Protection' and fender_dict[loc_fndr_key][0] == 'MV')
                        or (config != 'Corner Protection' and fender_dict[loc_fndr_key][0] !='MV')):
                    Rfndr = fc.fender_reaction(Efndr,E_rating,R_rating,fender_type)
                    Eberth_arr[loc_fndr_key].append([Efndr])
                    Rberth_arr[loc_fndr_key].append([Rfndr[1]])
                    Dberth_arr[loc_fndr_key].append([Rfndr[0]])

                    results[loc_fndr_key].append([key, k, case, ABF, config, wdepth, 
                                                M, L, B, D, CG, nfndr, 
                                                loc_fndr_key, fender_type, 
                                                E_rating, R_rating, D_rating, 
                                                V, Cbl, k_r, Cg, Cd, Cc, Ce, Cb,
                                                Cm, Eship, Rfndr[0], Efndr, 
                                                Rfndr[1]])

    for i in fender_dict.keys():

        # Generate Fender Curves
        fender_type = fender_dict[i][0]
        E_rating = fender_dict[i][1]
        R_rating = fender_dict[i][2]
        D_curve = fender_dict[i][3]
        E_curve = fc.Fenders[fender_type][0]*E_rating
        R_curve = fc.Fenders[fender_type][1]*R_rating

        plt.ER_demand_curve(Dberth_arr[i],Eberth_arr[i],Rberth_arr[i],D_curve,
                            E_curve,R_curve,cht_title= i + ' Fender Demand Curves')
        plt.ER_curve(D_curve, E_curve,R_curve, cht_title= i + ' Fender Curves')

    data=[]
    for i, key in enumerate(vessels):
        data.append([key,vessels[key][0],bv.velocity(vessels[key][0],'sheltered')])
    plt.vel_plt(data,'Approach Velocity Perpendicular to Berth')

    f = open(output,'w',newline='')
    writer = csv.writer(f)

    writer.writerow(fldnms)
    for key in results:
        for row in results[key]:
            writer.writerow(row)

    f.close()
        
