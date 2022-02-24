'''
#################################
plot_curve.py
################################# 

This model was written by Abygail R. Waggoner(1*) and L. Ilsedore Cleeves(1,2).

This script will plot the stochastic light curve produced by xray_generator.py

(1) University of Virginia, Department of Chemistry
(2) University of virginia, Department of Astronomy
* contact information: arw6qz@virginia.edu

################################
To run the script: 

1.) Generate a light curve with xray_generator.py
2.) Define the input parameters
3.) Run the script! 

#################################
'''
import numpy as N
import matplotlib.pyplot as plt
import pdb as pdb
import csv as csv

#######################
# Function goals: 
#    if plot_peaks = True, this function will read in and plot
#    the individual flare peaks generated by xray_generator.py
# Inputs: 
#    filename: Name of .inp file containing the flare peaks
#    plot_label: string that is the plot legend
# Outputs: 
#    None 
#######################
def find_peaks(filename,plot_label):

    days = 86400.0 # number of seconds in a day
    years = 3.154e7 # seconds in 1 year   
 
    flare_peak = []
    time_peak = []

    f = open(filename,'r')
    line = f.readline()
    while line:
        if line[0] == '#':
            pass
        else:
            line_split = line.split()
            flr = line_split[1]
            flr = float(flr)
            tm = line_split[0]
            tm = float(tm)
            flare_peak.append(flr)
            time_peak.append(tm)
        line = f.readline()
    
    f.close()
    
    plt.scatter(N.array(time_peak)/days,flare_peak,label=plot_label,marker="1",color='black')

    return

#######################
# Function Goal: 
#    Read in and plot the light curve generated by xray_generator.py 
# Inputs: 
#    filename: The name of the lightcurve csv file
#    plot_label: plot legend label
#    Lchar: Desired/target characteristic luminosity 
#######################
def main(filename,plot_label,Lchar):
    days = 86400.0 # seconds in 1 day
    years = 3.154e7 # seconds in 1 year

    Lxr = []
    time = []
    
    with open(filename) as csv_file: 
        csv_reader = csv.reader(csv_file,delimiter=",")
        line_cnt = 0
        for row in csv_reader:
            
            if row[0] == "#":
                pass
            else: 
                time.append(float(row[0]))
                Lxr.append(float(row[1]))
    plt.plot(N.array(time)/days,Lxr,color='black',label='Simulated Light Curve')

    return

#############################
#############################
# INPUT PARAMETERS
############################
############################
Lchar = 10**30.25 #observed characteristic luminosity, erg/sec
curve_name = './lightcurve_1.00_60.0_0.0_37.57_32.50_0.01_30.25_30.25_3.0_8.0_1.64_1.csv' 
peaks_name = './peaks_1.00_60.0_0.0_37.57_32.50_0.01_30.25_30.25_3.0_8.0_1.64_1.inp' 

normalized        = True   # set to true if the generated curve is normalized to DeltaLXR 
plot_peaks        = True   # if True, each modeled flare peak is plotted
plot_target_Lchar = True   # if True, plot +/- 10% of the target characteristic luminosity
                           # NOTE: this can be used to ensure micro/nano flaring are not
                           # raising the characteristic luminosity
############################
############################

labl = 'Light Curve'
main(curve_name,labl,Lchar)  #,normalize)

if plot_peaks == True:
    labl = 'Modeled Flare Peaks' 
    find_peaks(peaks_name,labl)

if plot_target_Lchar == True:
    char_upper_lim = [] 
    char_lower_lim = []
    time_plotter = N.arange(0.0,365.0,1.0)
    for t in time_plotter:
        char_upper_lim.append(Lchar + 0.10*Lchar)
        char_lower_lim.append(Lchar - 0.10*Lchar)
    if normalized == True: 
        char_upper_lim = (N.array(char_upper_lim)) / Lchar
        char_lower_lim = (N.array(char_lower_lim)) / Lchar
    else: 
        pass
    plt.plot(time_plotter, char_upper_lim, color='grey',label=r'+/- 10% of $L_{\rm char, obs}$')
    plt.plot(time_plotter, char_lower_lim, color='grey')


#plt.legend()
plt.xlabel("time (days)")

if normalized == True: 
    plt.ylabel('$\Delta$L$_{XR}$')#"Energy (ergs)")
else:
    plt.ylabel('Total Energy, including $L_{\rm char}$ (erg)')

plt.legend()
plt.show()
  
'''
End of plot_curve.py 
'''
