#!/usr/bin/venv python3.7
import datetime as dt
import math

SQRT_TWO = math.sqrt(2)

SQRT_TWO_PI = math.sqrt(2*math.pi)

"""
Define winddown start from 15:00:00 at day T-1 to 15:00:00 at day T. Based on concentration of market events and news,
future move more when market is active.
Information accumulates during market close hours, so time should still tick during non-trading hours.
Assume during no-trading session time tick the slowest, evening session time tick slower than day sessions.
"""
TRADING_DAYS = 256

CUTOFF = dt.time(15)

SCHEDULE = {0: {'start': 15, 'end': 21, 'span': 6, 'event_hours_left': 24.0, 'speed': 0.6, 'status': 'close'},
            1: {'start': 21, 'end': 24, 'span': 2, 'speed': 1.2, 'status': 'open', 'event_hours_left': 20.4},
            2: {'start': 0, 'end': 1, 'span': 2, 'speed': 1.2, 'status': 'open', 'event_hours_left': 16.8},
            3: {'start': 1, 'end': 9, 'span': 8, 'speed': 0.6, 'status': 'close', 'event_hours_left': 15.6},
            4: {'start': 9, 'end': 10.25, 'span': 1.25, 'speed': 2.4, 'status': 'open', 'event_hours_left': 10.8},
            5: {'start': 10.25, 'end': 10.5, 'span': 0.25, 'speed': 1.2, 'status': 'close', 'event_hours_left': 7.8},
            6: {'start': 10.5, 'end': 11.5, 'span': 1, 'speed': 2.4, 'status': 'open', 'event_hours_left': 7.5},
            7: {'start': 11.5, 'end': 13.5, 'span': 2, 'speed': 1.2, 'status': 'close', 'event_hours_left': 5.1},
            8: {'start': 13.5, 'end': 15, 'span': 1.5, 'status': 'open', 'event_hours_left': 2.7, 'speed': 1.8}}

