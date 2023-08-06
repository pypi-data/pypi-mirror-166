import io
import os
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import date
import logging

logger = logging.getLogger(__name__)

# This method create a linear regression
def lreg(x, y):
    lreg = LinearRegression().fit(x, y)
    lreg_score = lreg.score(x, y)
    lreg_coef = lreg.coef_
    lreg_interc = lreg.intercept_
    return lreg, lreg_score, lreg_coef, lreg_interc
     
