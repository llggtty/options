#!/usr/bin/venv python3.7
import os
import pandas as pd

from strategy.common.config import *

import logging
logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s')





if __name__ == '__main__':
    run_all_data()
    # spread_trading(20200721)