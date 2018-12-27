#!/bin/bash

# Check Status
date >> $HOME/logs/response_check.log
$HOME/miniconda3/bin/python check502err.py >> $HOME/logs/response_check.log
echo " " >> $HOME/logs/response_check.log

## Initialize log files with date
date > $HOME/logs/plotStatus_daily.log
date > $HOME/logs/plotStatus_weekly.log
date > $HOME/logs/plotStatus_monthly.log
date > $HOME/logs/plotStatus_yearly.log

## Plot Status Figures for year, month, week, day
$HOME/miniconda3/bin/python plotStatus.py day >> $HOME/logs/plotStatus_daily.log 2>&1 &
$HOME/miniconda3/bin/python plotStatus.py week >> $HOME/logs/plotStatus_weekly.log 2>&1 &
$HOME/miniconda3/bin/python plotStatus.py month >> $HOME/logs/plotStatus_monthly.log 2>&1 &
$HOME/miniconda3/bin/python plotStatus.py year >> $HOME/logs/plotStatus_yearly.log 2>&1 &
wait

# Cleanup Daily Files
cd /var/www/html/status;
echo "$(tail -96 m2m_status_day.log)" > m2m_status_day.log

# Cleaup weekly files
echo "$(tail -672 m2m_status_week.log)" > m2m_status_week.log

# Cleanup Monthly Files
echo "$(tail -2880 m2m_status_month.log)" > m2m_status_month.log

# Cleanup Yearly Files
echo "$(tail -35040 m2m_status_year.log)" > m2m_status_year.log




