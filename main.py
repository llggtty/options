#!/usr/bin/venv python3.7
import os
import math
import numpy as np
import pandas as pd
from options.utils.dgp import *
from options.common.config import *
pd.options.display.float_format = '{:,.3f}'.format
pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 2000)

import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')



if __name__ == '__main__':
    pricing_data = generate_pricing_data(initial_price, annual_return, annual_volatility, days_to_expiry)
    rvol = realised_volatility(pricing_data['base_price'])
    pnl = portfolio_pnl(pricing_data)

    print(pnl, rvol, annual_volatility)
