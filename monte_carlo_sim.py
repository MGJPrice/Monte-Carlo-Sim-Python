"""
Monte Carlo Simulator Python 2024. Author: Martin Price
Basic Python program to help visualise risk management. The program will read a structured CSV file (data.csv) and will output three statistics:
    1. Frequency of events modelled using Poisson distribution
    2. Impact of the losses modelled using a LogNormal distribution
    3. Monte Carlo simulation for each risk consisting of 10,000 trials.

Statistics will be displayed in the console and modelled in graphs. Note: These graphs can take time to generate, please do not close the program before the graphs appear.
This program was created for a project while studying for an MSc in Cyber Security @ Lancaster University. If studying for a similar degree, please don't plagiarise.
For more information, please view the GitHub repo @ https://github.com/MGJPrice/Monte-Carlo-Sim-Python
"""

#Imports
import numpy as np
import csv
import matplotlib.pyplot as plt
import matplotlib.ticker as tkr

# describe_stats(data)
# input: data - a list of numeric values to analyse
# output: tuple of (mean, median, variance) of the data in that order
def describe_stats(data):
    data.sort() #Sorted to calculate median
    sum = 0
    for i in data:
        # SUM of x[i]
        sum = sum + i
    mean = sum / len(data)
    if ((len(data) % 2) == 0): #If Even
        # Find midpoint between the TWO middle values: (n / 2) and ((n / 2) + 1)
        # -1's included in index because I starts from 0, not 1, formula assumes 1st data point is i == 1
        median = (data[int((len(data) / 2) - 1)] + data[
            int(((len(data) / 2) + 1) - 1)]) / 2
    else: #Else Odd
        median = data[int((len(data) + 1) / 2) - 1]

    sum = 0
    for i in data:
        #Calculate SUM of (x[i] - mean)^2
        sum = sum + ((i - mean) ** 2)
    variance = sum / len(data)

    return mean, median, variance

# poisson_param(data)
# input: data - a list of numeric values to analyse
# output: a value which is used a the lambda or mu value for a poisson dist
def poisson_param(data):
    sum = 0
    for i in data:
        # SUM of x[i]
        sum = sum + i
    return (sum / len(data)) #return mean/mu/lambda

# lognormal_param(data)
# input: data - a list of numerical values to analyse
# output: tuple of (ln_mu, ln_sigma) calculated from the data
def lognormal_param(data):
    sum = 0
    for i in data:
        # SUM of x[i]
        sum = sum + np.log(i)
    mean = sum / len(data)

    sum = 0
    for i in data:
        #Calculate SUM of (x[i] - mean)^2
        sum = sum + ((np.log(i) - mean) ** 2)
    variance = sum / len(data)

    return mean, (np.sqrt(variance))

# monte_carlo_run(p_mu, ln_mu, ln_sigma, trials)
# input: p_mu - the lambda/mu for the poison distribution
#        ln_mu - the lognormal mu for the dist
#        ln_sigma - the sigma (stddev) for the lognomal dist
#        trials - the number of trials to run
# returns: A list of total losses for that month (should be length should = trials)
def monte_carlo_run(p_mu, ln_mu, ln_sigma, trials):
    numberOfEvents = np.random.poisson(p_mu,trials)
    lossMagnitude = np.random.lognormal(ln_mu,ln_sigma,trials)
    totalLosses = numberOfEvents * lossMagnitude

    return totalLosses

def loadCSV(filename):
    logList = [] #Holds csv rows, 1 row is list entry
    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            rowList = [] #Holds information about current row, 1 segment is 1 list entry
            for seg in row:
                rowList.append(float(seg)) #Add segment as float
            logList.append(rowList)
    return logList

# Used to convert the currency ticks into a more readable format (10000 converts to £10,000)
def currencyFormatter(amt, pos):
    zeroCount = 0
    amt = amt.astype(str)[:-2]
    for i in range(len(amt) - 1,0,-1):
        if amt[i] == '0':
            zeroCount = zeroCount + 1
        if zeroCount == 3:
            amt = amt[:(i)] + "," + amt[(i):]
            zeroCount = 0
    amt = '£' + amt
    return amt

#Generate Loss Exceedance Curve based off total losses
def lossExceedenceCurve(totalLosses):
    percentiles = [] #Stores % of losses above amount in corrosponding array (index's corrospond to eachother)
    losses = [] #Holds amounts
    totalLosses = np.sort(totalLosses)

    # Loop through amounts incrementing in 2 to save some time
    for i in range(0,totalLosses.astype(int)[len(totalLosses) - 1],2):
        exceeded = 0
        #Calculate what % of losses are above this amount
        for loss in totalLosses:
            if loss > i:
                exceeded = exceeded + 1

        losses.insert(0,i) #Insert into array containing the loss amount
        percentiles.insert(0,exceeded / len(totalLosses)) #Insert into array containing % of losses that are above amount

    #Plot and display graph
    fig = plt.figure(figsize=(8,4))

    ax = plt.gca()
    curve, = ax.plot(losses,percentiles)
    ax.set_xscale("log")
    ax.set_ylim(0.0,percentiles[len(percentiles) - 1] + 0.05)
    print("**Ignore warnings related to x axis scale**")
    ax.set_xlim(0,losses[0] * 1.5)
    print("**End of expected warnings**")
    ax.yaxis.set_major_formatter(tkr.PercentFormatter(1,None,"%",False)) #Convert yaxis to percentages
    ax.xaxis.set_major_formatter(currencyFormatter) #convert x axis to currency
    ax.grid(True,'both','x')
    ax.grid(True,'major','y')
    plt.title("Loss Exceedance Curve for aggregated risk ")
    yData = curve.get_ydata()
    xData = curve.get_xdata()

    #print prob for 30,300,3000
    for i in range(0,len(xData)):
        if xData[i] == 30:
            print("Probability of exceeding £30: ", yData[i])
        if xData[i] == 300:
            print("Probability of exceeding £300: ", yData[i])
        if xData[i] == 3000:
            print("Probability of exceeding £3000: ", yData[i])


    return 0

def histrogram(losses, id):
    #Calculate num of bins
    #Calculate total loss % in each bin
    #Graph
    losses = np.sort(losses)


    fig = plt.figure(figsize=(5,6))
    plt.title("Probability Density Histogram for Risk " + id)
    ax = plt.gca()
    ax.hist(losses,bins=500,density=True)
    ax.set_xlabel('Loss Amount')
    ax.set_ylabel('Probability')

    pass

if __name__ == '__main__':
    #Load file
    logList = loadCSV("data.csv")

    #Simulate losses
    totalLosses = []
    totalInherentLoss = 0
    for i in range(0,len(logList),2): # Loop through each risk pair (0 & 1),(2 & 3),(4 & 5),(6 & 7)
        p_mu = poisson_param(logList[i])
        ln_mu,ln_sigma = lognormal_param(logList[i + 1])
        losses = monte_carlo_run(p_mu,ln_mu,ln_sigma,10000)
        id = str((i / 2) + 1)
        print("\n---Risk ", id, "---")
        print("event stats: ", describe_stats(logList[i]))
        print("loss stats: ", describe_stats(logList[i + 1]))
        print("p_mu: " , p_mu)
        print("ln_mu: " , ln_mu)
        print("ln_sigma: " , ln_sigma)
        # mean = exp(mu + ((sigma^2) / 2)) # prob = p_mu
        inherentLoss = p_mu * np.exp(ln_mu + ((ln_sigma**2) / 2) ) # prob * mean
        totalInherentLoss = totalInherentLoss + inherentLoss
        print("inherent loss: ", inherentLoss)
        histrogram(losses, id)
        if i == 0:
            totalLosses = losses
        else:
            totalLosses = totalLosses + losses
    print("\n---All Risks---\nTotal Inherent Loss: ", totalInherentLoss)
    totalLosses.sort()
    print("Minimum Simulated Loss:", totalLosses[0])
    print("Maximum Simulated Loss: ", totalLosses[-1])
    print("Mean Expected Sim Loss: ", ((totalLosses[0] + totalLosses[-1])/2))

    lossExceedenceCurve(totalLosses)
    plt.show()
    print("\nAnalysis Completed. Program will now close...")
