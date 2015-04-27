# R script to plot the india map

t <- read.csv("scaled_india.csv",sep=",")
t <- t(t)
x <- as.numeric(t[1,1:ncol(t)])
y <- as.numeric(t[2,1:ncol(t)])
pdf("india.pdf")
plot(x,y,pch='.') 
