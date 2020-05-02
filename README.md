# WorkoutBuddy

![](https://github.com/cedricduriau/workoutbuddy/workflows/Build/badge.svg?branch=master)
[![Platform: linux-64](https://img.shields.io/badge/Platform-linux--64-lightgrey.svg)](https://img.shields.io/badge/Platform-linux-lightgrey.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
[![Python](https://img.shields.io/badge/Python-2.7%20|%203.8-blue.svg)](https://img.shields.io/badge/Python-2.7%20|%203.8-blue.svg)

## Overview

WorkoutBuddy is a workout database and plotting tool.

## Install

If you wish to install the current master, use the following command:

`pip install git+git://github.com/cedricduriau/workoutbuddy.git`

Or a specific release version:

`pip install git+git://github.com/cedricduriau/workoutbuddy.git@v0.3.1`


## Usage

```
# set up database
workoutbuddy-cli set-up

# clear database
workoutbuddy-cli tear-down

# create exercise
workoutbuddy-cli create-exercise --name "pull up"

# list exercises
workoutbuddy-cli list-exercises

# log exercises
workoutbuddy-cli log-exercise --date "today" --exerciseid 1 --reps 20
workoutbuddy-cli log-exercise --date "01/01/2020" --exerciseid 1 --reps 20

# list logs
workoutbuddy-cli list-logs

# launch gui
workoutbuddy-gui
```
