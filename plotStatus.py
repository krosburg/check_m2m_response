import sys
import matplotlib
matplotlib.use('Agg')
import numpy as np
from PIL import Image
from os import remove
import pandas as pd
from matplotlib import dates as mdates
from matplotlib import pyplot as plt
from datetime import datetime

# Define Functions:
def getTimeWinArg():
    """Retrieves commandline argument for time-window for ploting"""
    if len(sys.argv) < 2:
        print('No time windows supplied, using day.')
        return 'day'
    else:
        t_win = str(sys.argv[1]).lower()
        if t_win not in ['day', 'week', 'month', 'year']:
            raise Exception('Invalid time window, using day')
            return 'day'
    return t_win

def saveFig(fname, lgd):
    """Saves the figure"""
    plt.savefig(fname + '.png',
                bbox_extra_artists=(lgd,), 
                bbox_inches='tight')
    Image.open(fname + '.png').convert('RGB').save(fname + '.jpg', 'JPEG')
    remove(fname + '.png')


def makePlotNice():
    """Add xlims, ylabel, title, and grid to plot"""
    plt.ylim(ylim)
    plt.xlim(xlims)
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
    box_y = -.50*0.65
    return plt.legend(loc='upper center', bbox_to_anchor=(0.5, box_y),
                      fontsize=legtx_size, frameon=True, ncol=4)


# Get Command Line Args
t_win = getTimeWinArg()

# Define Variables
log_dir = "/var/www/html/status/"
img_dir = log_dir + "images/"
file_base = "m2m_status_" + t_win
log_file = log_dir + file_base + ".log"

# Define Plotting Variables
ylim = [0, 15]
label_size = 21
title_size = 28
value_size = 20
legtx_size = 18
label_wt = "bold"
title_wt = "bold"

# Load Data
print("Reading log: " + log_file)
df = pd.read_csv(log_file, delim_whitespace=False, header=None)
t = []
for d in df[0]:
    t.append(datetime.strptime(str(d), '%Y-%m-%dT%H:%M:00.000Z'))
t = np.array(t)
    
# Classify Data
ired = df.index[df[1] == 0].tolist()
iyel = df.index[df[1] == 1].tolist()
igrn = df.index[df[1] == 2].tolist()
iblk = df.index[df[1] == 3].tolist()

# Limits
xlims = [np.nanmin(t), np.nanmax(t)]

# Plot Datas
fig = plt.figure(1, figsize=(18, 4.475))
if "month" not in t_win and "year" not in t_win:
    plt.plot(t, df[2], 'k-', label='_nolegend_')
else:
    plt.plot(t, df[2], '-', color='lightgray', label='_nolegend_')
plt.plot(t[igrn], df[2][igrn], 'og', label="Successful Query")
plt.plot(t[iyel], df[2][iyel], 'o', color='gold', label="Other Error")
plt.plot(t[ired], df[2][ired], 'or', label="502 Error")
plt.plot(t[iblk], df[2][iblk], 'o', color='maroon', label="Request Timeout")
makePlotNice()
lgd = addLegend()

# Tidy up the X-Axis
tidyXAxis('%H:%M\n%d-%b\n%Y', value_size)

# Save FIgure
saveFig(img_dir + file_base, lgd)
print(img_dir + file_base + ".jpg updated.")
plt.close('all')

