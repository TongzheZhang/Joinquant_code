# -*- coding: utf-8 -*-
"""
Created on Wed Sep 20 17:49:18 2017

@author: Richard10ZTZ
"""

from sklearn import svm
import pandas as pd
import numpy as np
if __name__ == "__main__":
    df=pd.read_csv('jqdatasdk_image_high_pe_low_mc.csv')
    df.set_index('code', inplace = True)
    dfnew = df.T
    dfnew.drop('600155.XSHG',axis=1, inplace=True)
    dfnew.plot(figsize = (12, 8), legend = True)