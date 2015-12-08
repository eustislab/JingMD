#
# Title = AverageScaling_GaussianDecomp.R
# Description
#	Takes a CSV file of input (ie. wavelength vs. absorptivity).
#	Generates a 1-dimensional pseudo-data set that models the data given.
#	Fits Gaussian curves to the pseudo data set.
#		The method is likely to produce false peaks if given a small sampling set. (modify the variable samplingSize to change this)
#		Using an extremely large sampling set the accuracy of this method is improved but not guaranteed 
# Authors
#	Professor Jack O'Brien (Bowdoin College)
#	Peter Cohen (Bowdoin College, Class of 2017)
#
# To run this code in the R command line
#	source("AverageScaling_GaussianDecomp.R")
#		Notice that the file to read is hard-coded within the program itself
#
# Dependencies
#	Mclust library

#
# Output
#	Information on each Gaussian component (mean and sigma value)
#	Plot of the summation of the set of Gaussian components
#

#prepares R to use the Mclust package
library(mclust);

#hard-coded value of the CSV data file to read into the program
csvFileToRead = file.choose();

#reads the given CSV file
data.set = read.table(csvFileToRead, header = TRUE, sep = ",")

#remove rows of data for which the absorptivityVal < a cut-off val
cutOffValue = .003
data.set = subset(data.set, data.set[,2] >= cutOffValue)

#plots the given data set
Wave_Number = data.set[,1];
Molar_Absorptivity = data.set[,2];

#the set of all values in the second column of the given data (ie. molar absorptivity)
total.abs = data.set[,2];

#the minimum value of total.abs
minAbs.val   = min(total.abs);

#the minimum value of the wave characteristic (wavelength or wave number)
minWave.val = min(data.set[,1])

#the maximum value of the absorptivity
maxAbs.val   = max(total.abs);

#the maximum value of the wave characteristic (wavelength or wave number)
maxWave.val = max(data.set[,1])

# makes sure that all absorptivity values are greater than zero
if (minAbs.val <= 0)
{
	# small epsilon value to ensure positivity
	epsilon = 0.003;
	
	total.abs = total.abs - minAbs.val + epsilon;
}

#the sampling size used in creating the pseudo data
samplingSize = 1e5;

#constructs a 1-dimensional data set based upon the input dataset
pseudo_Data = sample(x=data.set[,1],size=samplingSize,replace=TRUE,total.abs)

#finds the Gaussian components of the generated pseudo-data
#modelNames = "V" for variable variance Gaussians
GaussianDecompositionApproximation = Mclust(pseudo_Data, modelNames = "V");

#		Given a Gaussian function from a Gaussian Decomposition program.
#		Computes the oscillator strength based on the equation f = (4.93E-9) * integral(M * dv)
#			Where: f is oscillator strength, M is molar absorptivity, and v is wave number
#		Recall that M = Gaussian * v
#			Where: M is molar absorptivity, v is wave number
	
#		Let G(v) be a Gaussian of the independent variable v
#		Thus, f = (4.93E-9) * integral(G(v) * v * dv)
Absorptivity2Oscillator <- function(lowerLim, upperLim, mean, sd, scalar)
{
	#change of variables
	lowerLim = -mean #the upper limit is unchanged because it is infinite
	
	
	#the initial constant scaling factor of the oscillator strength equation
	constantMultiple = (-sd * scalar) / sqrt(2 * pi)
	
	#the wave number dependent part of the integration
	functionalPart <- function(x)
	{
		value = exp(-((x)^2) / (2 * (sd^2)))
		return(value)
	}
	
	#the non-erf part of the oscillator strength integration
	oscillatorStrength = constantMultiple * (functionalPart(upperLim) - functionalPart(lowerLim))
	
	#the error function approximation (can be considered accurate because the mean is many times the sd)
	erfApproximation = scalar * mean
	
	#incorporates the approximation for the error function and the analytically evaluated integral
	oscillatorStrength = oscillatorStrength + erfApproximation
	
	#scales the oscillator strength by the literature value of (4.93E-9)
	oscillatorStrength = oscillatorStrength * (4.93E-9)
	
	return(oscillatorStrength)
}

#an equation for a non-normalized Gaussian style curve.
#scalar is a constant scaling factor of the curve.  mean and sd have the usual significance
#colour is an integer parameter giving the colour specification for the curve by index in R
GaussianCurve <- function(scalar, mean, sigmasq, colour)
{
	#convert from sigma squared variance to standard deviation
	sd = sqrt(sigmasq)
	
	par(new = TRUE)
	
	#scaling of the given normalized Gaussian curve (the integral from -infinity to +infinity is 1), the number 657 is the largest colour specification for R
	curve(scalar * dnorm(x, mean = mean, sd = sd, log = FALSE), add = TRUE, col = (colour %% 657))
	
	#oscillator strength is computed by the equation presented on pg 35 of "Photochemistry of Organic Compounds: From Concepts to Practice" by Klan and Wirz
	#the lower bound and upper bound are specified such that all possible wave numbers are considered in the calculation of oscillator strength
	oscillatorStrength = Absorptivity2Oscillator(0, Inf, mean, sd, scalar)
	
	#draws a line for the oscillator strength
	lines(x = mean, y = oscillatorStrength, type = "h", col = (colour %% 657))
	
	#Gaussian component information printout
	#cat("mean = ", mean, "\t standard deviation = ", sd, "\t \t scaling factor = ", scalar, "\t oscillator strength = ", oscillatorStrength, "\n")
	
	#wavelength (nm) and oscillator strength value
	cat("wavelength (nm) = ", ((1E7) / mean) , "\t oscillator strength = ", oscillatorStrength, "\n")
}

#the average maximum value of all the individual Gaussian components is initialized to 0
averageCorrectionFactor = 0

#creates a vector of each scaling factor
correctionFactorVector = vector(mode = "numeric", length = length(GaussianDecompositionApproximation$parameters$mean))

#enters data into the scale vector
for (i in 1:length(GaussianDecompositionApproximation$parameters$mean))
{
	mean = GaussianDecompositionApproximation$parameter$mean[i]
	scalar = GaussianDecompositionApproximation$parameter$pro[i]
	sigmasq = GaussianDecompositionApproximation$parameters$variance$sigmasq[i]
	sd = sqrt(sigmasq)
	
	#finds the wave number value closest to the mean of the Gaussian component
	index = which(abs(Wave_Number - mean) == min (abs(Wave_Number - mean)))
	
	#the molar abs. of the wave number closest to the mean of the component
	absorptivityVal = Molar_Absorptivity[index]
	
	#the max of the Gaussian component
	
	gaussianMax = scalar / (sqrt(2 * pi) * sd)
	
	correctionFactorVector[i] = absorptivityVal / gaussianMax
}

#the average maximum value of all the individual Gaussian component
averageCorrectionFactor = mean(correctionFactorVector)

plot(data.set, xlim=c(maxWave.val,minWave.val), xlab = "Wave Number (cm-1)", ylab = "Molar Abs./Wave Number (M-1 cm-2)", main = "Original Data with Gaussian Decomposition Overlay")

for (i in 1:length(GaussianDecompositionApproximation$parameters$mean))
{		
	#specifies the scaling factor for use in the GaussianCurve function based upon the mixing proportions
	scalar = GaussianDecompositionApproximation$parameter$pro[i]
	
	#scales the scalar in order to make the scales of the data and the Gaussian components match
	scalar = scalar * averageCorrectionFactor
	
	#calls the function to draw a Gaussian curve with the given specifications
	GaussianCurve(scalar, GaussianDecompositionApproximation$parameters$mean[i],
	GaussianDecompositionApproximation$parameters$variance$sigmasq[i], i)
}

