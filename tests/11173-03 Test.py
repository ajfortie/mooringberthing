'''
Project #     11173/03
Project Name: Repair Ammunition Wharves W3 & W1
Designer:     Aaron Fortier - afortier@moffattnichol.com

This script houses all the berthing parameters neccessary for evaluation of 
berthing energy demands using the mooringberthing package and associated 
modules. For the latest distribution of this package and a list of 
dependancies, please contact Aaron Fortier (afortier@moffattnichol.com).
'''
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..\\src')))

import vesselberthing.berthing_energy as mb

# from ..src.vesselberthing import berthing_energy as mb

# Vessel Parameters:
#           Name                Broadside   Submarine?  Berths
#           (str)               # Fndr      (Bool)      
vessels =  {'T-AKE':            [5,          False,      ['Surface Berth 1', 'Corner Protection']],
            'DDG-1000':         [3,          False,      ['Surface Berth 1', 'Corner Protection']],
            'DDG-51':           [3,          False,      ['Surface Berth 2', 'Corner Protection']],
            'CG-52':            [3,          False,      ['Surface Berth 2', 'Corner Protection']],
            'LCS-2':            [3,          False,      ['Surface Berth 1', 'Corner Protection']],
            'SSGN-726':         [2,          True,       ['Submarine Berth 1', 'Corner Protection']],
            'SSN-774 BLK V':    [2,          True,       ['Submarine Berth 2', 'Corner Protection']],
            'SSN-774 BLK IV':   [2,          True,       ['Submarine Berth 2', 'Corner Protection']],
            'SSN-688':          [2,          True,       ['Submarine Berth 2', 'Corner Protection']]
            }

#         Berth Description             Mudline         Fender                      Berthing        Config  
#                                       Elevation       Type                        Condition       Factor
berths = {'Surface Berth 1':            [66.0,          'Typical Pneumatic',        'sheltered',    1.0],
          'Surface Berth 2':            [61.0,          'Typical Pneumatic',        'sheltered',    1.0],
          'Submarine Berth 1':          [61.0,          'Hydropneumatic 6.4m Sub',  'sheltered',    1.0],
          'Submarine Berth 2':          [66.0,          'Hydropneumatic 5.0m Sub',  'sheltered',    1.0],
          'Corner Protection':          [61.0,          'Corner Protection Fender', 'sheltered',    1.0]
          }

#            Load Case      Berthing                    Abnormal    Geometry    Water
#                           Config                      Berthing    Factor      Level
loadcases = {'Op_LAT_FQp': ['Forward Quarter Point',    1.0,        0.95,       99.490],
             'Op_HAT_FQp': ['Forward Quarter Point',    1.0,        0.95,       102.78],
             'Ac_LAT_FQp': ['Forward Quarter Point',    1.5,        0.95,       99.490],
             'Ac_HAT_FQp': ['Forward Quarter Point',    1.5,        0.95,       102.78],
             'Op_LAT_RQp': ['Rear Quarter Point',       1.0,        0.95,       99.490],
             'Op_HAT_RQp': ['Rear Quarter Point',       1.0,        0.95,       102.78],
             'Ac_LAT_RQp': ['Rear Quarter Point',       1.5,        0.95,       99.490],
             'Ac_HAT_RQp': ['Rear Quarter Point',       1.5,        0.95,       102.78],
             'Op_LAT_Bs' : ['Broadside',                1.0,        1.0,        99.490],
             'Op_HAT_Bs' : ['Broadside',                1.0,        1.0,        102.78],
             'Ac_LAT_Bs' : ['Broadside',                1.5,        1.0,        99.490],
             'Ac_HAT_Bs' : ['Broadside',                1.5,        1.0,        102.78],
             'Ac_LAT_Cp' : ['Corner Protection',        1.5,        1.0,        99.490],
             'Ac_HAT_Cp' : ['Corner Protection',        1.5,        1.0,        102.78]
             }

fender_dict = {'Typical Pneumatic':       ['pneumatic',       1339.0,     678.0,    0.6],
               'Hydropneumatic 6.4m Sub': ['hydropneumatic',  1253.9,     1011.6,   0.4],
               'Hydropneumatic 5.0m Sub': ['hydropneumatic',  1064.4,     844.0,    0.4],
               'Corner Protection Fender':['MV',              441.1,      365.5,    0.575]
               }
# Define Eccentricity over-rides for corner protection system
cp_e_dict = {'T-AKE': 164.5,
             'DDG-1000': 105.4,
             'DDG-51': 72.5,
             'CG-52': 103.5,
             'LCS-2': 0,
             'SSGN-726': 58,
             'SSN-774 BLK V': 35,
             'SSN-774 BLK IV': 0,
             'SSN-688': 0}

# Output File
output = 'BerthingEnergy.csv'

fndr_results = mb.berthing_energy(vessels, berths, loadcases, fender_dict, cp_e_dict, output)

mb.plot_fndr_results(vessels,fender_dict,fndr_results)

mb.print_fndr_csv(fndr_results,output='this is a test.csv')
