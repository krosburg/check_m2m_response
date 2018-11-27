import sys
import requests
import matplotlib
matplotlib.use('Agg')
import numpy as np
from PIL import Image
from os import remove
import numpy as np
import pandas as pd
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from datetime import datetime
from ooi_globals import BASE_URL
from ooicreds import UKEY, TOKE
try:
    requests.packages.urllib3.disable_warnings()
except ModuleNotFoundError:
    None

# Define Functions:
def saveFig(fname, lgd):
    """Saves the figure"""
    plt.savefig(fname + '.png',
                bbox_extra_artists=(lgd,), 
                bbox_inches='tight')
    Image.open(fname + '.png').convert('RGB').save(fname + '.jpg', 'JPEG')
    remove(fname + '.png')


def makePlotNice():
    """Add xlims, ylabel, title, and grid to plot"""
    plt.ylim(0, 60)
    plt.ylabel("Reponse Time (s)", fontsize=label_size, fontweight=label_wt)
    plt.title("M2M Response Time & Status", fontsize=title_size, fontweight=title_wt)
    plt.grid(True, linestyle='dashed', linewidth=2)

def tidyXAxis(date_fmt, tsize):
    """Formats xaxis dates"""
    ax = plt.gca()
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt))
    plt.tick_params(labelsize=tsize)

def addLegend():
    """Adds legend to plot."""
    box_y = -.50*(1 + (2*.225))
    return plt.legend(loc='lower right', bbox_to_anchor=(1.005, box_y),
                      fontsize=20, frameon=False)


# Define Variables
img_dir = '/var/www/html/engm2m/images/'

# Define Plotting Variables
label_size = 23
title_size = 30
value_size = 22
legtx_size = 24
label_wt = "bold"
title_wt = "bold"

# Assemble URL
url = BASE_URL + '/12576/sensor/inv/RS01SLBS/LJ01A/12-CTDPFB101/metadata/times/'

# Date Variable
t_now = datetime.utcnow()
t_str = t_now.strftime('%Y-%m-%dT%H:%M:00.000Z')

# Try to get data
t_bef = datetime.utcnow()
res = requests.get(url, auth=(UKEY, TOKE), timeout=10, verify=False)
t_aft = datetime.utcnow()
tdiff = t_aft - t_bef
tdiff = tdiff.seconds + (tdiff.microseconds*1E-6)
if res.status_code == 502:
    value_502 = 0
elif res.status_code == 200:
    value_502 = 2
else:
    value_502 = 1
print("Status Code: %i" % res.status_code)

# Add Message to Log
if value_502  and t_str:
    f = open("/var/www/html/status/m2m_status.log", "a+")
    f.write("%s,%i,%2.5f\n" % (t_str, value_502, tdiff))
    f.close()


# Load Data
df = pd.read_csv("/var/www/html/status/m2m_status.log", delim_whitespace=False, header=None)
t = []
for d in df[0]:
    t.append(datetime.strptime(str(d), '%Y-%m-%dT%H:%M:00.000Z'))
t = np.array(t)
    
# Classify Data
ired = df.index[df[1] == 0].tolist()
iyel = df.index[df[1] == 1].tolist()
igrn = df.index[df[1] == 2].tolist()

# Plot Datas
fig = plt.figure(1, figsize=(18, 4.475))
plt.plot(t, df[2], 'k-', label='_nolegend_')
plt.plot(t[ired], df[2][ired], 'or', label="502 Error")
plt.plot(t[iyel], df[2][iyel], 'o', color='gold', label="Other Error")
plt.plot(t[igrn], df[2][igrn], 'og', label="Successful Query")
makePlotNice()
lgd = addLegend()

# Tidy up the X-Axis
#tidyXAxis('%H:%M\n%m-%d-%y', value_size)


# Save FIgure
fname = "/var/www/html/status/images/m2m_status_day"
saveFig(fname, lgd)
'''


# Get IP Data
            inst, t_start, t_end = getIPData(inst, t_window)

            if not inst:
                print(' Data return empty: Skipping...')
                continue
            else:
                err_flag = False

            # Loop on IP Parameters to Plot
            figNum = 1
            for data in inst.ipData:
                # Assemble Plot Label
                plt_lab = 'J%s avg: %2.2f, max: %2.2f' % (inst.id,
                                                          np.nanmean(data),
                                                          np.nanmax(data))
                # Instantiate Figure and Plot Data; Incrament Counter
                fig = plt.figure(figNum, figsize=(18, 4.475))
                plt.plot(inst.time, data, label=plt_lab)
                figNum += 1

        # Loop Back Through Figures to Add Important Info
        for ii in range(1, 5):
            # Switch To Figure
            fig = plt.figure(ii, figsize=(18, 4.475))

            if err_flag:
                t_start, t_end = errorPlot()

            # Add Y-Label, Title, and Grid
            tstr = node.id + ' ' + tstrs[ii-1]
            makePlotNice()

            # Tidy up the X-Axis
            if not err_flag:
                tidyXAxis('%H:%M\n%m-%d-%y', value_size)

            # Setup File Names
            fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
            print(fig_file + '_NL.png updated')
            saveFigNL(fig_file + '_NL')

            # Add Legend
            if err_flag:
                lgd = []
            else:
                lgd = addLegend()

            # Save Figures
            fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
            print(fig_file + '_L.png updated')
            saveFig(fig_file + '_L', lgd)
        plt.close('all')
        print(' ')


# == NOW PLOT ONLY FOR PD STREAMS ===========
with open(in_file, 'rb') as input:
    rsn = pickle.load(input)
tstrs = ['Dock Temperature', 'Dock 12 Volt Current', 'Dock Humidity']
# Loop on Sites, Nodes, Instruments, Streams
for site in rsn.sites:
    # Skip if No Nodes
    if not site.nodes:
        continue

    # Filter only for PD nodes
    nodes = [n for n in site.nodes if 'PD' in n.id]

    # Skip if filtering results in empty list
    if not nodes:
        continue

    # Loop on Nodes for Site
    for node in nodes:
        print('%s %s-%s' % (datetime.now(), site.id,node.id))
        # Skip if No Instruments
        if not node.instruments:
            continue

        # Loop on Instrument for Node
        err_flag = True
        for inst in node.instruments:

            # Skip if No Streams
            if not inst.streams:
                continue

            # Get IP Data
            inst, t_start, t_end = getPDData(inst, t_window)

            if not inst:
                print(' Data return empty: Skipping...')
                continue
            else:
                err_flag = False


            # Plot Temperature
            fig = plt.figure(1, figsize=(18, 4.475))
            lb1 = "Dock Temp (avg: %2.2f, max: %2.2f, min: %2.2f)" % (inst.avgs[0], inst.maxs[0], inst.mins[0])
            lb2 = "Heat Sink Temp (avg: %2.2f, max: %2.2f, min: %2.2f)" % (inst.avgs[1], inst.maxs[1], inst.mins[1])
            lb3 = "12 Volt Current (avg: %2.2f, max: %2.2f, min: %2.2f)" % (inst.avgs[2], inst.maxs[2], inst.mins[2])
            lb4 = "Relative Humidity (avg: %2.2f, max: %2.2f, min: %2.2f)" % (inst.avgs[3], inst.maxs[3], inst.mins[3])
            plt.plot(inst.time, inst.data[0], label=lb1)
            #plt.plot(inst.time, inst.data[1], label='Heat Sink Temp')
            plt.plot(inst.time, inst.data[1], label=lb2)
            if err_flag:
                t_start, t_end = errorPlot()
                

            # Plot Current
            fig = plt.figure(2, figsize=(18, 4.475))
            plt.plot(inst.time, inst.data[2], label=lb3)
            if err_flag:
                t_start, t_end = errorPlot()

            # Plot Current
            fig = plt.figure(3, figsize=(18, 4.475))
            plt.plot(inst.time, inst.data[3], label=lb4)
            if err_flag:
                t_start, t_end = errorPlot()

            # Return toe ach plot and clean up
            for ii in range(1, 3):
                fig = plt.figure(ii, figsize=(18, 4.475))
                tstr = node.id + ' ' + tstrs[ii-1]
                makePlotNice()
                if not err_flag:
                    tidyXAxis('%H:%M\n%m-%d-%y', value_size)
                # Generate no-legend figure
                fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
                print(fig_file + '_NL.png updated')
                saveFigNL(fig_file + '_NL')
                # Add legend (or not)
                if err_flag:
                    lgd = []
                else:
                    lgd = addLegend()
                # Generate w/ legend figure
                fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
                print(fig_file + '_L.png updated')
                saveFig(fig_file + '_L', lgd)
#                fig_file = img_dir + site.id + '-' + tstr.replace(' ', '_')
#                print(fig_file + '.png updated')
#                saveFig(fig_file, lgd)
            plt.close('all')
        print(' ')
'''
