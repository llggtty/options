#!/usr/bin/venv python3.7
import math

"""
Constants 
"""

TRADING_DAYS = 256

SQRT_TWO = math.sqrt(2)

SQRT_TWO_PI = math.sqrt(2*math.pi)

"""
pricing parameters
"""
initial_price = 100
strike = 100
annual_return = 0.1
annual_volatility = 0.3
rate = 0.05
days_to_expiry = 256
tte = days_to_expiry/TRADING_DAYS
contract_multiplier = 100
k1 = 100
k2 = 120

