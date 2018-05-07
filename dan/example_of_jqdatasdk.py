import jqdatasdk
from datetime import datetime
import pandas as pd
import numpy as np

jqdatasdk.auth("******", "******")




if __name__ == '__main__':

    '''get threshold on certain date and stock index'''
    benchmark_date = '2015-12-30'
    stock_set = '000018.XSHG'
    q = jqdatasdk.query(jqdatasdk.valuation.code, jqdatasdk.valuation.pe_ratio, jqdatasdk.valuation.market_cap).\
        filter(jqdatasdk.valuation.pe_ratio>0, jqdatasdk.valuation.code.in_(jqdatasdk.get_index_stocks(stock_set))).\
        order_by(jqdatasdk.valuation.pe_ratio.asc())
    df = jqdatasdk.get_fundamentals(q, benchmark_date)
    pe_mean =  float(df['pe_ratio'].mean())
    mc_mean = float(df['market_cap'].mean())
    print df.head()
    print
    print 'pe_mean', pe_mean , '; mc_mean', mc_mean
    print



    '''get stock index we want'''
    q = jqdatasdk.query(jqdatasdk.valuation.code, jqdatasdk.valuation.pe_ratio).\
        filter(jqdatasdk.valuation.pe_ratio<pe_mean, jqdatasdk.valuation.market_cap<mc_mean,\
               jqdatasdk.valuation.pe_ratio>0, jqdatasdk.valuation.code.in_(jqdatasdk.get_index_stocks(stock_set))).\
        order_by(jqdatasdk.valuation.pe_ratio.asc())
    df = jqdatasdk.get_fundamentals(q, benchmark_date)
    newlist = df['code'].tolist()
    print newlist
    print


    '''get benchmark_date data'''
    newq = jqdatasdk.query(jqdatasdk.valuation.code, jqdatasdk.valuation.pe_ratio).\
        filter(jqdatasdk.valuation.code.in_(newlist))
    newdf = jqdatasdk.get_fundamentals(newq, benchmark_date)
    names = ['code', 'initial_PE_%s'%benchmark_date]
    newdf.columns = names
    print newdf
    print


    '''
    con_df = jqdatasdk.get_fundamentals_continuously(newq, end_date='2017-12-29', count=5)   # not support
    use following method to get data during start_date and end_date
    '''
    start_date = datetime(2015,12,31)
    end_date = datetime(2016,1,31)
    all_trade_days = jqdatasdk.get_trade_days(start_date=start_date, end_date=end_date)
    for i in all_trade_days:
        # print i.strftime('%Y-%m-%d'), 'traded'
        newdf[i.strftime('%Y-%m-%d')] = jqdatasdk.get_fundamentals(newq, i.strftime('%Y-%m-%d'))['pe_ratio']
    newdf.set_index(["code"], inplace=True)
    print newdf


    '''save part'''
    # newdf.to_csv('save.csv')
