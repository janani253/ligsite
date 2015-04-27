# R script to plot the india map with pockets

t <- read.csv("pockets.csv",sep=",")
t <- t(t)
x <- as.numeric(t[1,1:ncol(t)])
y <- as.numeric(t[2,1:ncol(t)])
z <- as.numeric(t[3,1:ncol(t)])
pdf("pockets.pdf")
plot(x,y,col=c("black","red")[z],pch='.') 
