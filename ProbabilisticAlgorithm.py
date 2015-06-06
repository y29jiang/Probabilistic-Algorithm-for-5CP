import numpy as np
from scipy.stats import norm

#Probabilistic Algorithm for 5CP 
def Probabilistic(thres_d,thres_t,thres_p,weatherfile,actualdemandfile,forecastdemandfile):
	#Sample input
	#thres_d=22355 #Demand threshold
	#thres_t=30 #Temperature threshold
	#thres_p=0.1 #Probabilistic threshold
	#weatherfile='Weather2012.csv' |Date|Date+Hour|Temperature|
	#actualdemandfile='ActualPeak_2012.csv' |Date|Peak Demand|Peak Hour|Date+Hour|
	#forecastdemandfile='ForecastPeak_2012.csv' |Forecasted Date|Date|DayAhead|Peak Demand Forecast|
	np.set_printoptions(suppress=True)
	
	#Define parameters
	N=31+30+31+31+30 #Number of days in the year from May 1st to September 30th
	calledCP=[] #to store called 5CP days
	weatherdata=np.genfromtxt(weatherfile, delimiter=',')
	demand_actual=np.genfromtxt(actualdemandfile, delimiter=',')
	demand_forecast=np.genfromtxt(forecastdemandfile, delimiter=',')
	delta=[271,210,653,380,545,584] #normal distribution delta

	for i in range(1,N):
		d_tomorrow=demand_forecast[((i-1)*6),3]#tomorrow's peak forecast on day i
		d_forecast=demand_forecast[((i-1)*6+1):((i-1)*6+6),3]#short term peak forecast on day i
		d_past=demand_actual[:i-1,1]#historic peak demand before day i
		t_tomorrow=weatherdata[i-1,2] #tomorrow's temperature forecast for the peak hour
		
		if d_tomorrow >=thres_d and t_tomorrow>=thres_t:
			#Compute Probabilities where P_future[i] represent the the probability of tomorrow's peak ranking (i+1)_th in forecast data, i=0 to 4
			P_future=np.zeros(5)
			norm_p=np.zeros(5) #store P(tomorrow's demand>=forecast demand for day(tomorrow+j+1) for 6 days short term forecast, excluding tomorrow
			for j in range(0,5):
				norm_p[j]=norm.cdf(d_tomorrow-d_forecast[j],0,delta[j+1]+delta[0])
			P_future[0]=1
			for j in range(0,5):
				P_future[0]=P_future[0]*norm_p[j]
			P_future[1]=norm_p[0]*norm_p[1]*norm_p[2]*norm_p[3]*(1-norm_p[4])+norm_p[0]*norm_p[1]*norm_p[2]*norm_p[4]*(1-norm_p[3])+norm_p[0]*norm_p[1]*norm_p[4]*norm_p[3]*(1-norm_p[2])+norm_p[0]*norm_p[4]*norm_p[2]*norm_p[3]*(1-norm_p[1])+norm_p[4]*norm_p[1]*norm_p[2]*norm_p[3]*(1-norm_p[0])
			P_future[2]=norm_p[0]*norm_p[1]*norm_p[2]*(1-norm_p[3])*(1-norm_p[4])+norm_p[0]*norm_p[1]*norm_p[3]*(1-norm_p[2])*(1-norm_p[4])+norm_p[0]*norm_p[1]*norm_p[4]*(1-norm_p[3])*(1-norm_p[2])+norm_p[0]*norm_p[2]*norm_p[3]*(1-norm_p[1])*(1-norm_p[4])+norm_p[0]*norm_p[2]*norm_p[4]*(1-norm_p[3])*(1-norm_p[1])+norm_p[0]*norm_p[3]*norm_p[4]*(1-norm_p[1])*(1-norm_p[2])+norm_p[1]*norm_p[2]*norm_p[3]*(1-norm_p[0])*(1-norm_p[4])+norm_p[1]*norm_p[2]*norm_p[4]*(1-norm_p[0])*(1-norm_p[3])+norm_p[1]*norm_p[3]*norm_p[4]*(1-norm_p[0])*(1-norm_p[2])+norm_p[2]*norm_p[3]*norm_p[4]*(1-norm_p[0])*(1-norm_p[1])
			P_future[3]=norm_p[0]*norm_p[1]*(1-norm_p[2])*(1-norm_p[3])*(1-norm_p[4])+norm_p[0]*norm_p[2]*(1-norm_p[1])*(1-norm_p[3])*(1-norm_p[4])+norm_p[0]*norm_p[3]*(1-norm_p[2])*(1-norm_p[1])*(1-norm_p[4])+norm_p[0]*norm_p[4]*(1-norm_p[2])*(1-norm_p[3])*(1-norm_p[1])+norm_p[1]*norm_p[2]*(1-norm_p[0])*(1-norm_p[3])*(1-norm_p[4])+norm_p[1]*norm_p[3]*(1-norm_p[2])*(1-norm_p[0])*(1-norm_p[4])+norm_p[1]*norm_p[4]*(1-norm_p[2])*(1-norm_p[3])*(1-norm_p[0])+norm_p[2]*norm_p[3]*(1-norm_p[0])*(1-norm_p[4])*(1-norm_p[1])+norm_p[2]*norm_p[4]*(1-norm_p[0])*(1-norm_p[3])*(1-norm_p[1])+norm_p[3]*norm_p[4]*(1-norm_p[2])*(1-norm_p[0])*(1-norm_p[1])
			P_future[4]=norm_p[0]*(1-norm_p[1])*(1-norm_p[2])*(1-norm_p[3])*(1-norm_p[4])+norm_p[1]*(1-norm_p[0])*(1-norm_p[2])*(1-norm_p[3])*(1-norm_p[4])+norm_p[2]*(1-norm_p[1])*(1-norm_p[0])*(1-norm_p[3])*(1-norm_p[4])+norm_p[3]*(1-norm_p[1])*(1-norm_p[2])*(1-norm_p[0])*(1-norm_p[4])+norm_p[4]*(1-norm_p[1])*(1-norm_p[2])*(1-norm_p[3])*(1-norm_p[0])
			
			#Compute Probabilities where P_past[i] represent the the probability of tomorrow's peak ranking (i+1)_th in historic data, i=0 to 4
			P_past=np.zeros(5)
			d_past.sort()
			d_past_top=d_past[-6:-1]
			P_past[0]=1-norm.cdf(d_past_top[4]-d_tomorrow,0,delta[0]) #1-P(tomorrow's peak<=top 1 in historic peaks)
			for j in range(1,5):
				P_past[j]=norm.cdf(d_past_top[5-j]-d_tomorrow,0,delta[0])-norm.cdf(d_past_top[4-j]-d_tomorrow,0,delta[0])
			
			#Compute Probabilities where P_overall[i] represent the the probability of tomorrow's peak ranking (i+1)_th in all data, i=0 to 4
			P_overall=np.zeros(5)
			P_overall[0]=P_future[0]*P_past[0]
			P_overall[1]=P_future[0]*P_past[1]+P_future[2]*P_past[1]
			P_overall[2]=P_future[0]*P_past[2]+P_future[1]*P_past[1]+P_future[2]*P_past[0]
			P_overall[3]=P_future[0]*P_past[3]+P_future[1]*P_past[2]+P_future[2]*P_past[1]+P_future[3]*P_past[0]
			P_overall[4]=P_future[0]*P_past[4]+P_future[1]*P_past[3]+P_future[2]*P_past[2]+P_future[3]*P_past[1]+P_future[4]*P_past[0]
			#if the P_overall(rank<=5) is greater than the probability threshold, tomorrow is alerted as a 5CP day.

			if sum(P_overall)>=thres_p:
				#call as a peak day
				calledCP.append(i)
				
		#Update demand threshold
		elif d_tomorrow >=thres_d and t_tomorrow<thres_t:
			thres_d=d_tomorrow
		elif d_tomorrow <thres_d and t_tomorrow>=thres_t:
			thres_d=d_tomorrow
	#Output the called peak days	
	print calledCP
