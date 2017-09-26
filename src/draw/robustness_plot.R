library('ggplot2')
require(gridExtra)

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
  
  pl <- ggplot(data=data)
  pl <- pl + geom_point(aes(x=iscore, y=rcd), group=name, bins=10)
  pl <- pl + labs(title=name) + theme_bw()
  pl <- pl + ylab('RCD') + xlab('CIS') 
  #pl <- pl + xlim(0,15) + ylim(0,60)
  #pl <- pl + scale_x_log10() + scale_y_log10()
  pl <- pl + scale_fill_gradientn(colours=rainbow(3)) + facet_grid(. ~ name)
  
  return(pl)
}

plotCoreDist <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name %in% n),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bar(aes(x=core), group=name)
  pl <- pl + facet_grid(. ~ name)
  pl <- pl + scale_y_log10()
  return(pl)
}

plotCISCore <- function(fname, name, n) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  data <- data[which(data$name %in% n),]
  
  pl <- ggplot(data=data)
  pl <- pl + geom_bin2d(aes(x=core, y=iscore), group=name, bins=10)
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
  pl <- pl + geom_point(aes(x=core, y=rcd), group=name, bins=10)
  pl <- pl + labs(title=name) + theme_bw()
  pl <- pl + ylab('RCD') + xlab('Core') 
  #pl <- pl + xlim(0,15) + ylim(0,60)
  #pl <- pl + scale_x_log10() + scale_y_log10()
  pl <- pl + scale_fill_gradientn(colours=rainbow(3)) + facet_grid(. ~ name)
  
  return(pl)
}