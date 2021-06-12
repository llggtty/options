import math
from options.common.config import *


def norm_cdf(x: float) -> float:
    """
    normal distribution cdf
    :param x: x~N(0,1)
    :return: P(z<=x)
    """
    return 0.5*(1+math.erf(x/SQRT_TWO))


def norm_pdf(x: float) -> float:
    """
    normal distribution pdf
    :param x: x~N(0,1)
    :return: f(x)
    """
    return math.exp(-0.5*x**2) / SQRT_TWO_PI
