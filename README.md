# Monte-Carlo-Sim-Python
Basic Python program to help visualise risk management. The program will read a structured CSV file and will output three statistics:
1. Frequency of events modelled using Poisson distribution
2. Impact of the losses modelled using a LogNormal distribution
3. Monte Carlo simulation for each risk consisting of 10,000 trials.

This program was created for a project while studying for an MSc in Cyber Security @ Lancaster University. If studying for a similar degree, please don't plagiarise.

**Requirements**
- data.csv --- CSV file that contains event data for risks. Each risk requires two rows: Row A = Risk event occurrence, Row B = Risk Loss Occurance. The provided data.csv contains 4 years of data for 4 different risks (8 rows).

**Instructions**
1. Ensure data.csv matches the requirements above.
2. Run the Python file monte_carlo_sim.py
3. The program will export data for each risk in the console. The program will also generate graphs, this may take some time. DO NOT close the program until the graphs appear. There will be 1 graph per risk and an overall graph: Probability Density Histograms per risk & Loss Expectancy Curve

**Imports**
- NumPy
- csv
- matplotlib.pyplot
- matplotlib.ticker
