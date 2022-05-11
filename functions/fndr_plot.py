# This module will generate various berthing plots
import sys
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
import math 
from scipy import interpolate
from ..functions import berthvel as bv


def ER_demand_curve(D_d,E_d,R_d,Dplt_max,Eplt_data,Rplt_data, cht_title='Fender Demand Curves'):
    #Initialize plot
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    xmax_lin = Dplt_max

    D_arr = np.array(D_d)
    E_arr = np.array(E_d)
    R_arr = np.array(R_d)

    # Format Axis tick lables
    # X-axis
    xtickinc = 0.1
    xmin = 0
    xmax = max(max(D_arr),0)
    #xmax_lin = max(max(Dplt_arr),0)
    xmaxarr = np.arange(0,xmax*1.1,xtickinc)
    xtickarr = xmaxarr
    x_linspace = np.linspace(0,xmax_lin,50)

    y1max = max(max(E_arr),0)*1.3
    y1order = math.floor(math.log(y1max, 10))-1
    y1max = math.ceil(y1max/10**y1order)*10**y1order
    y1numtick = 10
    y1tickinc = y1max/y1numtick
    y1 = Eplt_data(x_linspace)
    
    y2max = max(max(R_arr),0)*1.7
    y2order = math.floor(math.log(y2max, 10))-1
    y2max = math.ceil(y2max/10**y2order)*10**y2order
    y2numtick = 10
    y2tickinc = y2max/y2numtick
    y2 = Rplt_data(x_linspace)

    # Y1-axis
    y1maxarr = np.arange(0,y1max,y1tickinc)
    y1tickarr = y1maxarr

    # Y2-axis
    y2maxarr = np.arange(0,y2max,y2tickinc)
    y2tickarr = y2maxarr

    lines0, labels0 = ax1.get_legend_handles_labels()
    lines1, labels1 = ax2.get_legend_handles_labels()

    #Draw Energy Curve
    ax1.plot(x_linspace,y1,'b', label = 'Energy Absorption Curve', zorder=1)
    ax2.plot(x_linspace,y2,'r', label = 'Reaction Curve', zorder=1)

    ax1.scatter(D_arr,E_arr, c = 'orange', s = 50, label = 'Energy Demands', marker='+', zorder=3)
    ax2.scatter(D_arr,R_arr, c = 'darkgreen', s = 50, label = 'Reaction Demands', marker='x', zorder=3)

    E_max = 0
    D_max = 0
    R_max = 0
    for i,item in enumerate(E_arr):
        if item > E_max:
            E_max = item
            D_max = D_arr[i]
            R_max = R_arr[i]
    ax1.text(D_max,E_max,"{0:.3f} kip-ft".format(E_max[0]),backgroundcolor='white', zorder = 2)
    ax2.text(D_max,R_max,"{0:.3f} kip".format(R_max[0]),backgroundcolor = 'white', zorder = 2)

    fig.figure.set_tight_layout(True)
    fig.figure.set_dpi(300)
    fig.figure.set_figheight(6.5)
    fig.figure.set_figwidth(6.5)

    # ax1.legend(lines0 + lines1, labels0 + labels1)
    ax1.legend(loc=2)
    ax2.legend(loc=1)

    ax1.set(xlabel = 'Normalized Deflection', xlim=(xmin,xmax*1.1), xticks=xtickarr,
            ylabel = 'Energy Absorption (Kip-ft)', ylim = (0,y1max), yticks=y1tickarr,
            title = cht_title)
    ax1.set_xticklabels(['{:,.2%}'.format(x) for x in xtickarr])

    ax1.grid(visible=True)
    ax2.set(ylabel = 'Fender Reaction (Kip)', ylim = (0,y2max), yticks=y2tickarr)
    
    fig.savefig(cht_title+'.png')
    plt.close()

def ER_curve(Dplt_max,Eplt_data,Rplt_data, cht_title='Fender Reaction Curves'):
    #Initialize plot
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    
    xmax_lin = Dplt_max

# Format Axis tick lables
    # X-axis
    xtickinc = 0.1
    xmin = 0
    xmax = max(xmax_lin,0)
    xmaxarr = np.arange(0,xmax*1.1,xtickinc)
    xtickarr = xmaxarr
    x_linspace = np.linspace(0,xmax,50)

    y1max = max(Eplt_data(xmax_lin),0)*1.1
    y1order = math.floor(math.log(y1max, 10))-1
    y1max = math.ceil(y1max/10**y1order)*10**y1order
    y1numtick = 10
    y1tickinc = y1max/y1numtick
    y1 = Eplt_data(x_linspace)
    E_int = np.polynomial.Polynomial.integ(Rplt_data,1,[0])*10.827
    y3 = E_int(x_linspace)
    
    y2max = max(Rplt_data(xmax_lin),0)*1.7
    y2order = math.floor(math.log(y2max, 10))-1
    y2max = math.ceil(y2max/10**y2order)*10**y2order
    y2numtick = 10
    y2tickinc = y2max/y2numtick
    y2 = Rplt_data(x_linspace)

    # Y1-axis
    y1maxarr = np.arange(0,y1max,y1tickinc)
    y1tickarr = y1maxarr

    # Y2-axis
    y2maxarr = np.arange(0,y2max,y2tickinc)
    y2tickarr = y2maxarr

    #Draw Energy Curve
    ax1.plot(x_linspace,y1,'b', label = 'Energy Absorption Curve', zorder=1)
    # ax1.plot(x_linspace,y3,'g', label = 'Energy Absorption Curve', zorder=1)
    ax2.plot(x_linspace,y2,'r', label = 'Reaction Curve', zorder=1)


    fig.figure.set_tight_layout(True)
    fig.figure.set_dpi(300)
    fig.figure.set_figheight(6.5)
    fig.figure.set_figwidth(6.5)

    lines0, labels0 = ax1.get_legend_handles_labels()
    lines1, labels1 = ax2.get_legend_handles_labels()

    ax1.legend(lines0 + lines1, labels0 + labels1)

    ax1.set(xlabel = 'Normalized Deflection', xlim=(xmin,xmax*1.1), xticks=xtickarr,
            ylabel = 'Energy Absorption (Kip-ft)', ylim = (0,y1max), yticks=y1tickarr,
            title = cht_title)
    ax1.set_xticklabels(['{:,.2%}'.format(x) for x in xtickarr])

    ax1.grid(visible=True)
    ax2.set(ylabel = 'Fender Reaction (Kip)', ylim = (0,y2max), yticks=y2tickarr)
    
    fig.savefig(cht_title+'.png')
    plt.close()

def vel_plt(data,cht_title='Vessel Berthing Velocity'):
    #Initialize plot
    fig, ax = plt.subplots()

    # Marker arrays
    mkrs = ['+','x','*','1','3','s','o','.','p']
    base_colors=['b','g','r','c','m','y','k']
    color = []
    for i in data:
        ind=(math.floor(np.random.random(1)*len(base_colors)))
        color.append(base_colors[ind])

    data_t = list(map(list,zip(*data)))
    disp_d = np.array(data_t[1])
    vel_d = np.array(data_t[2])
    y1 = []
    y2 = []
    y3 = []

    x  = np.linspace(1000,100000,100)
    for i in x:
        y1.append(bv.velocity(i,'sheltered'))
        y2.append(bv.velocity(i,'moderate'))
        y3.append(bv.velocity(i,'exposed'))
    y1arr = np.array(y1)
    y2arr = np.array(y2)
    y3arr = np.array(y3)
    y1spline = interpolate.make_interp_spline(x,y1arr)
    y2spline = interpolate.make_interp_spline(x,y2arr)
    y3spline = interpolate.make_interp_spline(x,y3arr)

    y1sp = y1spline(x)
    y2sp = y2spline(x)
    y3sp = y3spline(x)

    xtickinc = 5000
    xmax = math.ceil(max(disp_d)*1.1/10**4)*10**4
    xmin = 0
    xtickinc = xmax/10
    xmaxarr = np.arange(0,xmax,xtickinc)
    xtickarr = xmaxarr

    y1max = 2.0
    y1numtick = 10
    y1tickinc = y1max/y1numtick

    y1maxarr = np.arange(0,2,y1tickinc)
    y1tickarr = y1maxarr

    ax.plot(x,y1sp,'g', label = 'Sheltered Condition', zorder=1)
    ax.plot(x,y2sp,'y', label = 'Moderate Condition', zorder=1)
    ax.plot(x,y3sp,'r', label = 'Exposed Condition', zorder=1)

    for i, key in enumerate(data_t[0]):
        ax.scatter(disp_d[i],vel_d[i], c = color[i], label = key, s = 50, marker=mkrs[i], zorder=2)
        if (vel_d[i] == max(vel_d)) or (vel_d[i] == min(vel_d)):
            ax.text(disp_d[i],vel_d[i],'v = {0:.2f} ft/s'.format(vel_d[i]))

    fig.figure.set_tight_layout(True)
    fig.figure.set_dpi(300)
    fig.figure.set_figheight(6.5)
    fig.figure.set_figwidth(6.5)

    ax.set(xlabel = 'Vessel Displacement (LT)', xlim=(0,xmax), xticks=xtickarr,
           ylabel = 'Berthing Velocity (ft/s)', ylim = (0,2), yticks=y1tickarr,
           title = cht_title)    

    ax.grid(visible=True)
    ax.legend()
    plt.tight_layout()
    fig.savefig(cht_title+'.png')
    plt.close()