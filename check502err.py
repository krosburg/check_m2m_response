import requests
from datetime import datetime
from ooi_globals import U
from ooicreds import UKEY, TOKE
try:
    requests.packages.urllib3.disable_warnings()
except ModuleNotFoundError:
    None


# Define Variables
time_windows = ["day", "week", "month", "year"]
log_base = "/var/www/html/status/m2m_status_"

# Assemble URL
url = U + 'RS01SLBS/LJ01A/12-CTDPFB101/metadata/times/'

# Setup Run Date
t_now = datetime.utcnow()
t_str = t_now.strftime('%Y-%m-%dT%H:%M:00.000Z')

# Try to get data and "Time Request
t_bef = datetime.utcnow()
try:
    res = requests.get(url, auth=(UKEY, TOKE), timeout=10, verify=False)
    t_aft = datetime.utcnow()

    # Assign values based on status code from request
    if res.status_code == 502:
        value_502 = 0
    elif res.status_code == 200:
        value_502 = 2
    else:
        value_502 = 1
    print("Status Code: %i" % res.status_code)

#except requests.exceptions.timeout or socket.timeout:
except socket.timeout:
    t_aft = datetime.utcnow()
    print("Timeout likely.")
    print(err)
    value_502 = 3

# Calculate Run Time Difference
tdiff = t_aft - t_bef
tdiff = tdiff.seconds + (tdiff.microseconds*1E-6)


# Add Message to Log
file_entry = "%s,%i,%2.5f\n" % (t_str, value_502, tdiff)
for t_win in time_windows:
    log_file = log_base + t_win + ".log"
    f = open(log_file, "a+")
    f.write(file_entry)
    f.close()

