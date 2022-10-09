"""This package will determine the berthing energy of the requested vessels, 
plot these energies on fender reaction curves, and generate the resulting
reactions.
"""
import csv
import json
import os

from .functions import berth_coeff as bc
from .functions import fndr_curves as fc
from .functions import fndr_plot as plt
from .functions import berthvel as bv

const_path = os.path.abspath(os.path.join(os.path.dirname(__file__),'.\\constants'))

# Load Vessel Parameters 
f = open(const_path + '\\vessels.json','r')
vessel_library = json.load(f)
f.close()

# Load Fender Parameters
f = open(const_path + '\\fenders.json','r')
fender_library = json.load(f)
f.close()

def berthing_energy(vessels, berths, loadcases, fender_dict, cp_e_dict, output):
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

    for i, key in enumerate(vessels):
        # Assign variables for the current vessel
        M = vessel_library[key]['Displacement']     # Vessel Displacement
        L = vessel_library[key]['Length Overall']   # Vessel Length
        B = vessel_library[key]['Breadth']          # Vessel Beam
        D = vessel_library[key]['Draft']            # Vessel Draft
        CG = vessel_library[key]['CoG']             # Center of Gravity
        Cbl = bc.Cbl(M, L, B, D)                    # Block Factor
        k_r = bc.k(Cbl, L)                          # Radius of Gyration
        Cd = vessel_library[key]['C_d']             # Deformation Factor
        loc_berths = vessels[key][2]                # Array of Berths for this vessel

        for j, jtem in enumerate(loc_berths):
            loc_fndr_key = (berths[jtem][1])
            mudline= berths[jtem][0]      # Mudline
            bcond = berths[jtem][2]
            V = bv.velocity(M, bcond)   # Berthing Velocity
            Cc = berths[jtem][3]        # Configuration Factor

            fender_type = fender_dict[loc_fndr_key][0]
            # fender_grade = fender_dict[loc_fndr_key][1]
            # E_rating = fender_library[fender_type][fender_grade]["E_rated"]
            # R_rating = fender_library[fender_type][fender_grade]["R_rated"]
            # D_rating = fender_library[fender_type][fender_grade]["D_rated"]
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
                        nfndr = vessels[key][0]
                        a = 0
                    case 'Corner Protection':
                        nfndr = 1
                        a = cp_e_dict[key]
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
                Cm = bc.Cm(L, B, D, Cb, wdepth, vessels[key][1])

                # Calculate Fender Energy (includes 10% increase for uncertainty)
                Efndr = ABF * Cm * Cb * Eship / nfndr * 1.1

                if ((config == 'Corner Protection' and fender_dict[loc_fndr_key][0] == 'MV')
                        or (config != 'Corner Protection' and fender_dict[loc_fndr_key][0] !='MV')):
                    Rfndr = fc.fender_reaction(Efndr,E_rating,R_rating,fender_type)
                    Eberth_arr[loc_fndr_key].append([Efndr])
                    Rberth_arr[loc_fndr_key].append([Rfndr[1]])
                    Dberth_arr[loc_fndr_key].append([Rfndr[0]])

                    results[loc_fndr_key].append([key, k, case, ABF, config, a, wdepth, 
                                                M, L, B, D, CG, nfndr, 
                                                loc_fndr_key, fender_type, 
                                                E_rating, R_rating, D_rating, 
                                                V, Cbl, k_r, Cg, Cd, Cc, Ce, Cb,
                                                Cm, Eship, Rfndr[0], Efndr, 
                                                Rfndr[1]])
    return results

def plot_fndr_results(vessels,fender_dict,fndr_results):

    for i in fender_dict.keys():
        Eberth_arr = []
        Rberth_arr = []
        Dberth_arr = []

        for j in fndr_results[i]:
            Eberth_arr.append(j[29])
            Rberth_arr.append(j[30])
            Dberth_arr.append(j[28])

        # Generate Fender Curves
        fender_type = fender_dict[i][0]
        E_rating = fender_dict[i][1]
        R_rating = fender_dict[i][2]
        D_curve = fender_dict[i][3]
        E_curve = fc.Fenders[fender_type][0]*E_rating
        R_curve = fc.Fenders[fender_type][1]*R_rating

        plt.ER_demand_curve(Dberth_arr,Eberth_arr,Rberth_arr,D_curve,
                            E_curve,R_curve,cht_title= i + ' Fender Demand Curves')
        plt.ER_curve(D_curve, E_curve,R_curve, cht_title= i + ' Fender Curves')

    data=[]
    for i, key in enumerate(vessels):
        data.append([key,vessel_library[key]['Displacement'],bv.velocity(vessel_library[key]['Displacement'],'sheltered')])
    plt.vel_plt(data,'Approach Velocity Perpendicular to Berth')

    return

def print_fndr_csv(results,output='Berthing Energy.csv'):

    # Field names used for CSV output
    fldnms = ['Vessel', 'Load Case','Berthing Condition','Acc. Factor', 'Berthing Configuration', 'Eccentricity',
            'Water Depth', 'Displacement','Length','Beam','Draft','CoG',
            'No. Fenders','Fender Name','Fender Type',
            'Rated Energy', 'Rated Reaction', 'Rated Deflection','Vel', 'Cbl', 
            'k_r', 'Cg', 'Cd', 'Cc', 'Ce', 'Cb', 'Cm','Eship', 'Deflection', 
            'Energy', 'Reaction']

    f = open(output,'w',newline='')
    writer = csv.writer(f)

    writer.writerow(fldnms)
    for key in results:
        for row in results[key]:
            writer.writerow(row)

    f.close()
        
