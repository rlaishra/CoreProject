library('ggplot2')
require(gridExtra)
library(latex2exp)
#library(tikzDevice)

robustnessPK <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  # data <- data[which(data$name %in% n),]
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
  #data <- data[which(data$name == 0),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bar(aes(x=core))
  pl <- pl + scale_y_log10()
  pl <- pl + facet_grid(. ~ name)
  return(pl)
}

plotCIDist <- function(fname, name) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  #data <- data[which(data$ci > 1),]
  data <- data[which(data$name == 0),]
  
  print(data)
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bar(aes(x=ci))
  #pl <- pl + geom_bin2d(aes(x=core, y=ci))
  #pl <- pl + geom_point(aes(x=core, y=ci))
  #pl <- pl + scale_y_log10()
  pl <- pl + facet_grid(. ~ name)
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

plotCIRe <- function(fname, sname, name) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  #data <- data[which(data$n %in% c(100)),]
  
  p1 <- ggplot(data=data)
  p2 <- ggplot(data=data)
  p3 <- ggplot(data=data)
  
  p1 <- p1 + geom_point(aes(x=cst_mean + 1, y=cr, color=type))
  p1 <- p1 + geom_errorbar(aes(x=cst_mean + 1, ymin=cr-cr_s, ymax=cr + cr_s, color=type))
  #p1 <- p1 + geom_point(aes(x=cit_mean, y=cr, color=type))
  #p1 <- p1 + geom_errorbar(aes(x=cit_mean, ymin=cr-cr_s, ymax=cr + cr_s, color=type))
  #p1 <- p1 + xlab(TeX('$\\frac{\\bar{CI_{95}(G)}}{\\bar{CI(G)}$')) + ylab(TeX('$R_{p}^{n(0,50)}(G)$'))
  p1 <- p1 + xlab(TeX('Core Influence-Strength ($CIS_{95}(G))')) + ylab(TeX('Core Resilience ($R_{p}^{n(0,50)}(G)$)'))
  p1 <- p1 + theme_bw()
  p1 <- p1 + scale_x_log10()
  p1 <- p1 + labs(color='Network Type')
  p1 <- p1 + theme(legend.position="bottom")
  #p1 <- p1 + facet_grid(.~n)
  
  tikz(file = sname, width = 4, height = 2.5, standAlone = TRUE)
  print(p1)
  dev.off()
  
  return(p1)
  
  p2 <- p2 + geom_point(aes(x=k_shell, y=cr, color=type))
  p2 <- p2 + geom_errorbar(aes(x=k_shell, ymin=cr-cr_s, ymax=cr + cr_s, color=type))
  p2 <- p2 + xlab(TeX('Fraction of nodes with CI greater than \\bar{CI}')) + ylab(TeX('$R_{p}^{0,50}(G)$'))
  p2 <- p2 + theme_bw()
  p2 <- p2 + scale_x_log10()
  p2 <- p2 + facet_grid(.~n)
  #p2 <- p2 + scale_x_log10()
  
  p3 <- p3 + geom_point(aes(x=cs_mean, y=cr, color=type))
  #p2 <- p2 + geom_errorbar(aes(x=ci_mean, ymin=cr-cr_s, ymax=cr + cr_s, color=type))
  p3 <- p3 + xlab(TeX('$\\sigma^2(CI)$')) + ylab(TeX('$R_{p}^{0,25}(G)$'))
  p3 <- p3 + theme_bw()
  p3 <- p3 + scale_x_log10()
  
  #return(p2)
  
  #p <- p + scale_x_log10()
  #p <- p + facet_grid(. ~ n)
  
  #d <- data[which(data$n==25),]
  #print(cor.test(data$cr, data$ci_perc))
  
  #tikz(file = sname, width = 2, height = 2, standAlone = TRUE)
  #print(p)
  #dev.off()
  
  p <- grid.arrange(p1,p2,ncol=1)
  
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
  p <- p + geom_point(aes(x=ci_perc, y=cim, color=rem))
  p <- p + ylab('Mean Core Influence') + ylab('Mean Core Strength')
  p <- p + scale_x_log10() 
  p <- p + theme_bw()
  
  #tikz(file = sname, width = 2, height = 2, standAlone = TRUE)
  #print(pl)
  #dev.off()
  
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

resilianceChange <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$n %in% c(50)),]
  d <- data[which(data$type == "CICS"),]
  
  pl <- ggplot(data=data)
  
  
  pl <- pl + geom_line(aes(y=cr, x=name, group=type, color=factor(type)))
  pl <- pl + geom_point(aes(y=cr, x=name, group=type, color=factor(type)))
  pl <- pl + geom_ribbon(data = d, aes(ymin=cr-cr_s, ymax=cr+cr_s, x=name, group=type, fill=factor(type)), alpha=0.2)
  #pl <- pl + xlab('Edges added (\\%)') + ylab(TeX('Core Resilince $R_{50}^{e(0,25)}(G)$'))
  pl <- pl + xlab('Edges added (\\%)') + ylab('Core Resilince')
  pl <- pl + theme_bw() + theme(text = element_text(size=10))
  #pl <- pl + guides(fill=FALSE, color=FALSE)
  pl <- pl + guides(fill=FALSE)
  pl <- pl + labs(color='')
  pl <- pl + theme(legend.position="bottom")
  #pl <- pl + labs(color='Algorithm')
  #pl <- pl + facet_grid(. ~ n)
  
  tikz(file = sname, width = 4, height = 2.4, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
}

plotApplicationAnomaly <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$s %in% c(0.5)),]
  
  pl <- ggplot(data=data)
  
  
  pl <- pl + geom_errorbar(aes(ymin=mean - std, ymax=mean + std, x=resilience, color=factor(tname)))
  pl <- pl + geom_point(aes(y=mean, x=resilience, color=factor(tname)))
  #pl <- pl + geom_ribbon(aes(ymin=cr-cr_s, ymax=cr+cr_s, x=name, group=type, fill=factor(type)), alpha=0.2)
  pl <- pl + xlab('Core Resilience') + ylab('Jaccrd Similarity')
  pl <- pl + theme_bw()
  #pl <- pl + guides(fill=FALSE, color=FALSE)
  pl <- pl + labs(color='Network Type')
  pl <- pl + theme(legend.position="bottom")
  #pl <- pl + labs(color='Algorithm')
  #pl <- pl + facet_grid(. ~ n)
  
  tikz(file = sname, width = 4, height = 3, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
}

plotRunnigTime <- function(fname, sname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  
  pl <- ggplot(data=data)
  pl <- pl + geom_point(aes(x=added,y=time,group=factor(network), color=factor(network)))
  pl <- pl + geom_line(aes(x=added,y=time,group=factor(network), color=factor(network)))
  pl <- pl + labs(color='')
  pl <- pl + xlab('Edges Added (\\%)') + ylab('Time (seconds)')
  pl <- pl + theme_bw() + theme(text = element_text(size=8))
  pl <- pl + theme(legend.position="bottom")
  
  tikz(file = sname, width = 4, height = 3, standAlone = TRUE)
  print(pl)
  dev.off()
  
  return(pl)
}