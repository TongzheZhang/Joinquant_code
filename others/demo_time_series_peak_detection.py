# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 16:44:14 2018
time series peak detection

ref: https://stackoverflow.com/questions/22583391/peak-signal-detection-in-realtime-timeseries-data

@author: Richard10ZTZ
"""

# Implementation of algorithm from https://stackoverflow.com/a/22640362/6029703
import numpy as np
import pylab
import matplotlib.pyplot as plt 
import pandas as pd

def thresholding_algo(y, lag, threshold, influence):
    signals = np.zeros(len(y))
    filteredY = np.array(y)
    avgFilter = [0]*len(y)
    stdFilter = [0]*len(y)
    avgFilter[lag - 1] = np.mean(y[0:lag])
    stdFilter[lag - 1] = np.std(y[0:lag])
    for i in range(lag, len(y)):
        if abs(y[i] - avgFilter[i-1]) > threshold * stdFilter [i-1]:
            if y[i] > avgFilter[i-1]:
                signals[i] = 1
            else:
                signals[i] = -1

            filteredY[i] = influence * y[i] + (1 - influence) * filteredY[i-1]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])
        else:
            signals[i] = 0
            filteredY[i] = y[i]
            avgFilter[i] = np.mean(filteredY[(i-lag):i])
            stdFilter[i] = np.std(filteredY[(i-lag):i])

    return dict(signals = np.asarray(signals),
                avgFilter = np.asarray(avgFilter),
                stdFilter = np.asarray(stdFilter))
    
    
if __name__ == '__main__':
    # Data
    y = [1,1,1.1,1,0.9,1,1,1.1,1,0.9,1,1.1,1,1,0.9,1,1,1.1,1,1,\
    1,1,1.1,0.9,1,1.1,1,1,0.9,1,1.1,1,1,1.1,1,0.8,0.9,1,1.2,0.9,1,\
    1,1.1,1.2,1,1.5,1,3,2,5,3,2,1,1,1,0.9,1,\
    1,3,2.6,4,3,3.2,2,1,1,0.8,4,4,2,2.5,1,1,1]

    # Settings
    lag = 10
    threshold = 3.5
    influence = 0.8

    # Get results
    result = thresholding_algo(y,lag,threshold,influence)
    plt.figure()  
    #plt.plot(y)
    #plt.plot(result['signals'])
    sent_processed= pd.read_csv('603019sent_processed.csv',index_col=[0]) 

    print sent_processed.head()
    sent_ES = sent_processed['sent_ES'].values
    plt.plot(sent_ES)
    result_sent = thresholding_algo(sent_ES,lag,threshold,influence)
    sent_processed['signal'] = result_sent['signals']
    plt.plot(result_sent['signals'])
    sent_processed['signal'].plot()