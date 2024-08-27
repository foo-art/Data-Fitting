import numpy as np
import pandas as pd
from datetime import datetime
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import time
import math

class Data:
    def __init__(self,dataframe,gas_species,site_code,units,scale):
        self.dataframe = dataframe
        self.average = 0  # default attribute to store average value of data 
        self.name = gas_species
        self.site = site_code
        self.units = units
        self.scale = scale
        
    def calc_average(self,period="M"): # default setting to "M" which calculates monthly average in ppb
        self.dataframe["time"] = pd.to_datetime(self.dataframe["time"])
        self.dataframe.index = self.dataframe["time"]
        self.average = self.dataframe.groupby(pd.Grouper(freq=period)).mean() # update the attribute self.average with the average value
        if (self.units=="ppm"):
            self.average = self.average*1000 # if self.units are set to "ppm" the method will return converted value in terms of ppb
    
    
    def plot(self,other,start='2019-01-01',finish="2019-12-31",period="M",size=100,quantile=0.10):
        self.calc_average(period) # update the average value of instances
        other.calc_average(period)
        x1 = self.average[start:finish] # slice the average value for selected duration of datetime
        x2 = other.average[start:finish]
        chunks_x1 = [x1.iloc[i:i+size-1,:] for i in range(0,len(x1),size)] # selectively collect data for specific size of increments
        chunks_x2 = [x2.iloc[i:i+size-1,:] for i in range(0,len(x2),size)] # this data is use for the creation of baseline

        base=[]
        for i in range(len(chunks_x1)):
            base1 = chunks_x1[i].quantile(quantile) # generate quantile from selected data collected
            base2 = chunks_x2[i].quantile(quantile)
            base.append(np.min([base1,base2])) # take the minimum value of quantile from both selected data as the y-coordinate of baseline

        date = []
        for i in range(len(chunks_x1)):
            date.append(pd.to_datetime([chunks_x1[i].index[0]])) # take the datetime of selected data to be use as x-coordinate of baseline
        
        fig, ax = plt.subplots()
        
        ax.set_ylabel(f"{self.name} (ppb)")
        
        ax.plot(x1.index, x1.values) # plotting the average value for the first instance
        ax.plot(x2.index, x2.values) # plotting the average value for the second instance
        ax.plot(date, base) # plotting the baseline
        
        plt.legend([self.site,other.site,"baseline"]) # label the plots
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.show()

    def polynomial(self,other,start='2019-01-01',finish="2019-12-31",period="M",degree=3):
        self.calc_average(period) # update the average value of instances
        other.calc_average(period)
        x1 = self.average[start:finish] # slice the average value for selected duration of datetime
        x2 = other.average[start:finish]
        
        fig, ax = plt.subplots()
        
        ax.set_ylabel(f"{self.name} (ppb)")
        
        idx = np.where(~np.isfinite(self.average[start:finish]))[0] # finding the index for missing values or NaN in both instances
        idx2 = np.where(~np.isfinite(other.average[start:finish]))[0]
        for i in idx:
            x1 = x1.replace(x1.values[i],x1.values[i-1]) # update the missing values with the nearest previous value 
        for j in idx2:
            x2 = x2.replace(x2.values[j],x2.values[j-1]) # this is to generate smoothest continuous plot of graph
            
        x = mdates.date2num(x1.index.to_pydatetime()) 
        average = (x1["mf"]+x2["mf"])/2 # take the average value of the average data from both instances
        coef = np.polyfit(x,list(average),degree) # the average value is to represent the coefficient for the approximate polynomial
        base = np.poly1d(coef) # obtain the polynomial data corresponding to y-coordinate of the opproximate polynomial
        d = mdates.num2date(x) # set datetime to be the x-coordinate of the approximate polynomial
        
        ax.plot(self.average[start:finish].index, self.average[start:finish].values) # plotting the average value for the first instance
        ax.plot(other.average[start:finish].index, other.average[start:finish].values) # plotting the average value for the second instance
        ax.plot(d, base(x)) # plotting the approximate polynomial 
        
        plt.legend([self.site,other.site,"polynomial"]) # label the plots
        plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%B %d'))
        plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
        plt.show()