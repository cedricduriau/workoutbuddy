# WorkoutBuddy

![](https://github.com/cedricduriau/workoutbuddy/workflows/Build/badge.svg?branch=master)
[![Platform: linux](https://img.shields.io/badge/Platform-linux-lightgrey.svg)](https://img.shields.io/badge/Platform-linux-lightgrey.svg)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)

## Overview

WorkoutBuddy is a workout database and plotting tool.

## Install

If you wish to install the current master, use the following command:

`pip install git+git://github.com/cedricduriau/workoutbuddy.git`

## Usage

#### Set up database
```
workoutbuddy-cli set-up
```

#### Clear database
```
workoutbuddy-cli tear-down
```

#### Create Exercise
```
workoutbuddy-cli create-exercise --name "pull up"
```

#### List Exercises
```
workoutbuddy-cli list-exercises
```

#### Log Exercise
```
workoutbuddy-cli log-exercise --date "today" --exerciseid 1 --reps 20
```

#### List Logs
```
workoutbuddy-cli list-logs
```
