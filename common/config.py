#!/usr/bin/venv python3.7
import datetime as dt

PTH_ContractList = '/Users/annhuang/code/strategy/data/ContractList.csv'
DIR_OUTPUT = '/Users/annhuang/code/strategy/data/results/'
DIR_RAW_DATA = '/Users/annhuang/Downloads/Future/'
DIR_PICKLE = '/Users/annhuang/code/strategy/data/md/'

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

ID_Market = 1

ID_AT = 2

Main_Futures = [332009, 702012, 762011] #[112010, 702012, 762011]

# in minutes
UnwindPositionTime = 10

"""
Theo set to lower base price by 1 bps at first, on every failed order, increase theo adj by change rate (CR)
"""
HACKING_THEO_ADJ = 1E-4

HACKING_CR = 0.05

Position_Limit = {'intraday_notional_per_contract': 1E6, 'overnight_notional_per_contract': 0}

"""
at check point adjust credit, one day session is 13500 seconds.if we want to adjust 14 times, 
then set interval to 900 seconds. On each session expect trade target set to 1.5 trades. 
If not hitting the target then lower credit. If one strategy losing above threshold, raising credit.
"""
Bool_Trading_Control = True
Trading_Control = {'pnl_warning': -1000, 'trade_target': 1.5, 'credit_raising_cr': 0.03,
                   'credit_lowering_cr': 0.03, 'check_point': 600, 'look_back': 10}

"""
If bid credit is 10 bps, current position is 20 and position retreat is 0.5 bps, then the offset is 0 bps. AT will send 
order on theo + minimum credit to flatten position. 
"""
DefaultCredit = {332009: {
        'bid_credit': 8 * 1E-4, 'ask_credit': 8 * 1E-4,
        'position_retreat': 0.5 * 1E-4,
        'hedge_retreat': 0,
        'min_credit': 2 * 1E-4
    },
    702012: {
        'bid_credit': 10 * 1E-4, 'ask_credit': 10 * 1E-4,
        'position_retreat': 0.3 * 1E-4,
        'hedge_retreat': 0.2 * 1E-4,
        'min_credit': 2 * 1E-4
        },
    762011: {
        'bid_credit': 10 * 1E-4, 'ask_credit': 10 * 1E-4,
        'position_retreat': 0.3 * 1E-4,
        'hedge_retreat': 0.2 * 1E-4,
        'min_credit': 2 * 1E-4
    }
}
"""
Configure per contract volume to be always below 1 million notional, for 5 CNY edge, want to trade 2 lots, 
for 10 CNY edge want to trade 3 lots. 762011 is bigger size, so trade less volume.
"""
DefaultVolume = {
    332009: {'min_volume': 1, 'max_volume': 3, 'accelerator': 0.2},
    702012: {'min_volume': 1, 'max_volume': 3, 'accelerator': 0.2},
    762011: {'min_volume': 1, 'max_volume': 2, 'accelerator': 0.1}
}

"""
Lead Lag
"""
Bool_Theo_Feed_From_Leader = True
Theo_Beta = {
    332009: {'leader': 762011, 'beta': 0.3},
    702012: {'leader': 762011, 'beta': 0.3},
}