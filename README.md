This code corresponds to the Probabilistic Algorithm in "Predicting peak-demand days in the Ontario peak reduction program for large consumers" papers[1,2].

Data Needed:

1. Actual hourly Ontario demand: http://www.ieso.ca/Pages/Power-Data/demand.aspx -> Historical Hourly Ontario and Market Demand

2. Forecasted short term hourly Ontario demand: http://reports.ieso.ca/public/SSR1/, http://reports.ieso.ca/public/SAADaily/

3. Weather data: http://climate.weather.gc.ca/advanceSearch/searchHistoricData_e.html

4. Long term peak demand forecast in 18-Month Outlook: http://www.ieso.ca/Pages/Participate/Reliability-Requirements/Forecasts-%26-18-Month-Outlooks.aspx

Algorithm: 

The details are in [1,2]. The code for the Probabilistic algorithm is in ProbabilisticAlgorithm.py.

Input Sample:

thres_d=22355 					                    #Demand threshold (specified in Table 6 of [2])

thres_t=30 					                        #Temperature threshold

thres_p=0.1 					                      #Probabilistic threshold

weatherfile='Weather2012.csv' 			        #Schema:|Date(YYYYDDMM)|Date+Hour(YYYYDDMMHR)|Temperature|

actualdemandfile='ActualPeak_2012.csv' 		  #Schema:|Date(YYYYDDMM)|Peak Demand|Peak Hour(HR)|Date+Hour(YYYYDDMMHR)|

forecastdemandfile='ForecastPeak_2012.csv' 	#Schema:|Forecasted Date(YYYYDDMM)|Date(YYYYDDMM)|DayAhead|Peak Demand Forecast|

[1] Jiang, Y., Levman, R., Golab, L., and Nathwani, J., 2014. Predicting peak-demand days in the Ontario peak reduction program for large consumers. In proc. of the 5th international conference on Future energy systems (ACM e-Energy), pages 221-222.

[2] Jiang, Y., Levman, R., Golab, L., and Nathwani, J., 2014b. Predicting peak-demand days in the Ontario peak reduction program for large consumers. In proc. of the International Workshop on Demand Response, co-located with ACM e-Energy 2014.  Accessed on April 28 2015, at http://wattalyst.org/static/DocumentUsed/dr2014_submission_8.pdf.
