library('ggplot2')
require(gridExtra)
library(latex2exp)
library(tikzDevice)

robustnessPK <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name %in% n),]
  #data <- data[which(data$k <= 50),]
  #data <- data[which(data$p <= 75),]
  
  mpl <- ggplot(data=data, aes(x=factor(p), y=factor(k)))
  mpl <- mpl + geom_tile(aes(fill=cor_mean))
  mpl <- mpl + theme_bw() + xlab('P') + ylab('N') + labs(fill='Similarity', title=name)
  mpl <- mpl + scale_fill_gradientn(colours=rainbow(3))
  mpl <- mpl + facet_grid(. ~ name)
  
  return(mpl)
}

robustnessLine <- function(fname, k, name) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$k == k),]
  
  pl <- ggplot(data = data)
  pl <- pl + geom_line(aes(x=p, y=cor_mean, group=factor(name), color=factor(name)))
  pl <- pl + geom_ribbon(aes(x=p, ymin=cor_mean-cor_std, ymax=cor_mean+cor_std, group=factor(name), fill=factor(name)), alpha=0.2)
  pl <- pl + guides(fill=FALSE)
  
  return(pl)
}

robustnessPKDiff <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name==n),]
  
  mpl <- ggplot(data=data, aes(x=factor(p), y=factor(k)))
  mpl <- mpl + geom_tile(aes(fill=diff))
  mpl <- mpl + theme_bw() + xlab('P') + ylab('K') + labs(fill='Diff', title=name)
  mpl <- mpl + scale_fill_gradientn(colours=rainbow(3)) + facet_grid(. ~ name)
  
  return(mpl)
}

plotRCDIS <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name %in% n),]
  #data <- data[which(data$iscore > 1),]
#data <- data[which(data$rcd > 1),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bin2d(aes(x=iscore, y=rcd), group=name, bins=30)
  #pl <- pl + labs(title=name) + theme_bw()
  pl <- pl +  theme_bw()
  pl <- pl + ylab('Core Strength') + xlab('Core Influence') 
  #pl <- pl + xlim(0,15) + ylim(0,60)
  #pl <- pl + scale_x_log10() + scale_y_log10()
  pl <- pl + scale_fill_gradientn(colours=rainbow(3)) + facet_grid(. ~ name)
  
  return(pl)
}

plotCoreDist <- function(fname, name) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name == 0),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bar(aes(x=cr))
  pl <- pl + scale_y_log10()
  return(pl)
}

plotCISCore <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name %in% n),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bin2d(aes(x=core, y=iscore), group=name, bins=30)
  pl <- pl + labs(title=name) + theme_bw()
  pl <- pl + ylab('CIS') + xlab('Core') 
  #pl <- pl + xlim(0,15) + ylim(0,60)
  #pl <- pl + scale_x_log10() + scale_y_log10()
  pl <- pl + scale_fill_gradientn(colours=rainbow(3)) + facet_grid(. ~ name)
  
  return(pl)
}

plotRCDCore <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name %in% n),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_point(aes(x=core, y=rcd), group=name, bins=30)
  pl <- pl + labs(title=name) + theme_bw()
  pl <- pl + ylab('Core Strength') + xlab('Core Number') 
  #pl <- pl + xlim(0,15) + ylim(0,60)
  #pl <- pl + scale_x_log10() + scale_y_log10()
  pl <- pl + scale_fill_gradientn(colours=rainbow(3)) + facet_grid(. ~ name)
  
  return(pl)
}

plotMeanCSRe <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$n %in% c(50,100)),]
  
  p <- ggplot(data=data)
  
  p <- p + geom_point(aes(x=cs_mean, y=cr, color=type))
  p <- p + xlab('Mean Core Strength') + ylab(TeX('$R_{p}(G)$')) + theme_bw()
  p <- p + facet_grid(. ~ n)
  #p <- p + scale_x_log10()
  
  #tikz(file = sname, width = 2, height = 2, standAlone = TRUE)
  #print(p)
  #dev.off()
  
  return(p)
}

plotMeanCIRe <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  #data <- data[which(data$n %in% c(50,100)),]
  
  p <- ggplot(data=data)
  
  p <- p + geom_point(aes(x=sqrt(cst_mean), y=cr, color=type))
  p <- p + xlab(TeX('$\\sqrt{C_{95}(G)}$')) + ylab(TeX('$R_{p}^{0,100}(G)$'))
  p <- p + theme_bw()
  p <- p + facet_grid(. ~ n)
  
  d <- data[which(data$n==25),]
  print(cor.test(d$cr, sqrt(d$cst_mean)))
  
  #tikz(file = sname, width = 2, height = 2, standAlone = TRUE)
  #print(p)
  #dev.off()
  
  return(p)
}

plotMeanCICSRe <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$n %in% c(50,100)),]
  
  p <- ggplot(data=data)
  
  p <- p + geom_point(aes(x=cs_mean/ci_mean, y=cr, color=type))
  #p <- p + geom_point(aes(x=cit_mean, y=cr))
  p <- p + xlab(TeX('\\frac{CS_{95}(G)}{CI_{95}(G)}')) + ylab(TeX('$R_{p}^{0,100}(G)$'))
  p <- p + theme_bw()
  p <- p + facet_grid(. ~ n)
  
   # d <- data[which(data$n==75),]
   # print(cor.test(d$cr, d$cs_perc/d$ci_perc))
   # print(cor.test(d$cr, d$cs_mean))
   # print(cor.test(d$cr, d$ci_mean))
   # 
   # d <- data[which(data$n==25),]
   # print(cor.test(d$cr, d$cs_perc/d$ci_perc))
   # print(cor.test(d$cr, d$cs_perc))
   # print(cor.test(d$cr, d$ci_perc))

  # d <- data[which(data$n==50),]
  # print(cor.test(d$cr, d$cs_perc/d$ci_perc))
  # print(cor.test(d$cr, d$cs_perc))
  # print(cor.test(d$cr, d$ci_perc))
  # 
  # d <- data[which(data$n==25),]
  # print(cor.test(d$cr, d$cs_perc/d$ci_perc))
  # print(cor.test(d$cr, d$cs_perc))
  # print(cor.test(d$cr, d$ci_perc))
  
  #tikz(file = sname, width = 2, height = 2, standAlone = TRUE)
  #print(p)
  #dev.off()
  
  return(p)
}

plotMeanCICS <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  p <- ggplot(data=data)
  p <- p + geom_point(aes(x=csm, y=cim, color=rem))
  p <- p + ylab('Mean Core Influence') + ylab('Mean Core Strength')
  p <- p + scale_x_log10() 
  p <- p + theme_bw()
  
  tikz(file = sname, width = 2, height = 2, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(p)
}

plotTopCICS <- function(fname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  p <- ggplot(data=data)
  #p <- p + geom_point(aes(x=citm/cstm, y=citm, color=rem))
  p <- p + geom_point(aes(x= citm/cim, y=rem, color=rem))
  p <- p + ylab('Mean Core Influence') + xlab('Mean Core Strength')
  #p <- p + scale_x_log10()
  #+ scale_y_log10()
  
  return(p)
}

plotTopCSRe <- function(fname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  p <- ggplot(data=data)
  p <- p + geom_point(aes(x=cstm, y=rem))
  p <- p + xlab('Mean Core Strength') + ylab(TeX('$R_{100}(G)$')) + theme_bw()
  p <- p + scale_x_log10()
  
  return(p)
}

plotTopCIRe <- function(fname, name) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  p <- ggplot(data=data)
  p <- p + geom_point(aes(x=cit_mean, y=cr))
  p <- p + ylab('Mean Core Influence') + ylab('Mean Core Strength')
  p <- p + scale_x_log10() 
  p <- p + theme_bw()
  p <- p + facet_grid(. ~ n)
  
  return(p)
}

resilianceChange <- function(fname, name, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$n %in% c(25)),]
  #data <- data[which(data$name <= 2),]
  
  pl <- ggplot(data=data)
  
  
  pl <- pl + geom_line(aes(y=cr, x=name, group=type, color=factor(type)))
  pl <- pl + geom_point(aes(y=cr, x=name, group=type, color=factor(type)))
  pl <- pl + geom_ribbon(aes(ymin=cr-cr_s, ymax=cr+cr_s, x=name, group=type, fill=factor(type)), alpha=0.2)
  pl <- pl + xlab('Nodes added') + ylab(TeX('$R_{25}^{0,100}(G)$'))
  pl <- pl + theme_bw()
  pl <- pl + guides(fill=FALSE)
  #pl <- pl + labs(title = name, color='Algorithm')
  pl <- pl + labs(color='Algorithm')
  
  tikz(file = sname, width = 4, height = 3, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
}