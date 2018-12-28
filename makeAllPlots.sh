#!/bin/bash

## Plot Status Figures for year, month, week, day
$HOME/miniconda3/bin/python plotStatus.py day >> $HOME/logs/plotStatus_daily.log 2>&1 &
$HOME/miniconda3/bin/python plotStatus.py week >> $HOME/logs/plotStatus_weekly.log 2>&1 &
$HOME/miniconda3/bin/python plotStatus.py month >> $HOME/logs/plotStatus_monthly.log 2>&1 &
$HOME/miniconda3/bin/python plotStatus.py year >> $HOME/logs/plotStatus_yearly.log 2>&1 &
wait
