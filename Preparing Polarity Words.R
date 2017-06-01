


dataDir="C:\\Data Science App\\My Extra Project\\LoughranMcDonald_MasterDictionary_2014.csv"
df <- read.csv(dataDir, header=TRUE)
library(car)
library(ggplot2)
library(lattice)
library(lmtest)
library(sandwich)
library(AER)
library(ivpack) # use ivpack to get robust standard errors for IV regression
library(stargazer)
#ls()
#str(df)
summary(df)
#print(df)

positive_df = df[df$Positive == 2009,]
m <- positive_df[, c("ï..Word")]
#avector <- as.vector(m)
m = data.matrix(m)
write(m,file="positive.txt",ncolumns=ncol(m))
#write(m,"positive.dat")
#print(m[2])

print(length(m))

negative_df = df[df$Negative == 2009,]
n <- negative_df[, c("ï..Word")]
n = data.matrix(n)
write(n,file="negative.txt",ncolumns=ncol(n))
#print (length(n))






