# Data Fitting
Python module to generate best fit graph for gas pressure reading using polynomial regression and K-nearest neighbour for quantile estimation.

## ```Data``` module
 - Module that defines a weather data (e.g. ```mhd_co2```) into a class with four main attributes which is the type of gas, code of site, unit of measurement and gas standard.
 - Also consists of three main methods :
   1) ```calc_average``` - To calculate the average reading of gas pressure at desirable intervals for quantile estimation using K-nearest neighbour approach.
   2) ```plot``` - To plot the reading of gas pressure of ```Data``` instances as well as the best fit and quantile estimation trendlines.
   3) ```polynomial``` - To plot the best fit line to represent overall pattern of the gas pressure reading using polynomial regression.

## Module testing
- Along with the module contains six ```csv``` formatted toy datasets to test the functionalities of the module ```Data```.
- The step-by-step instructions for the usage of ```Data``` module is in ```Data_module_guide```.
