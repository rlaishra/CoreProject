library('ggplot2')
require(gridExtra)
library(latex2exp)
library(reshape)

plotDecomposition <- function(fname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  
  datm <- melt(data, id.vars = c('name'), measure.vars=c('mat_dec', 'nx_dec', 'nor_dec'))
  #print(datm)
  
  p1 <- ggplot(data=data)
  p2 <- ggplot(data=data)
  p3 <- ggplot(data=data)
  p4 <- ggplot(data=data)
  p5 <- ggplot(data=datm)
  
  p1 <- p1 + geom_point(aes(x=nodes, y=mat_dec, color='Matrix'))
  p1 <- p1 + geom_point(aes(x=nodes, y=nor_dec, color='Normal'))
  p1 <- p1 + geom_point(aes(x=nodes, y=nx_dec, color='NX'))
  p1 <- p1 + theme_bw() + xlab('Nodes') + ylab('Time') + labs(color='Algorithm', title='Time v Nodes')
  
  p2 <- p2 + geom_point(aes(x=edges, y=mat_dec, color='Matrix'))
  p2 <- p2 + geom_point(aes(x=edges, y=nor_dec, color='Normal'))
  p2 <- p2 + geom_point(aes(x=edges, y=nx_dec, color='Nx'))
  p2 <- p2 + theme_bw() + xlab('Edges') + ylab('Time') + labs(color='Algorithm', title='Time v Edges')
  
  p3 <- p3 + geom_point(aes(x=degree, y=mat_dec, color='Matrix'))
  p3 <- p3 + geom_point(aes(x=degree, y=nor_dec, color='Normal'))
  p3 <- p3 + geom_point(aes(x=degree, y=nx_dec, color='Nx'))
  p3 <- p3 + theme_bw() + xlab('Average Degree') + ylab('Time') + labs(color='Algorithm', title='Time vs Average Degree')
  
  p4 <- p4 + geom_point(aes(x=sparsity, y=mat_dec, color='Matrix'))
  p4 <- p4 + geom_point(aes(x=sparsity, y=nor_dec, color='Normal'))
  p4 <- p4 + geom_point(aes(x=sparsity, y=nx_dec, color='Nx'))
  p4 <- p4 + theme_bw() + xlab('Sparsity') + ylab('Time') + labs(color='Algorithm', title='Time vs Sparsity')
  
  p5 <- p5 + geom_col(aes(x=name, y=value, fill=variable), position='dodge')
  #p5 <- p5 + geom_crossbar(aes(x=name, y=nor_dec, ymin=nor_dec, ymax=nor_dec, color='Normal'))
  #p5 <- p5 + geom_crossbar(aes(x=name, y=nx_dec, ymin=nx_dec, ymax=nx_dec, color='Nx'))
  p5 <- p5 + theme_bw() + xlab('Networks') + ylab('Time (seconds)') + theme(text = element_text(size=10))
  p5 <- p5 + theme(axis.text.x = element_text(angle = 90, hjust = 0))
  p5 <- p5 + theme(legend.title=element_blank(), legend.position = 'bottom')
  p5 <- p5 + scale_fill_manual("", values=c('red', 'green', 'blue'),  breaks=c('mat_dec','nor_dec','nx_dec'), labels=c('Matrix','Naive','NetworkX'))
  return(p5)
  
  pl <- grid.arrange(p1,p2,p3)
  return(pl)
}

plotChange <- function(fname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  
  datm <- melt(data, id.vars = c('name'), measure.vars=c('mat_cha', 'nx_cha', 'nor_cha'))
  
  p1 <- ggplot(data=data)
  p2 <- ggplot(data=data)
  p3 <- ggplot(data=data)
  p4 <- ggplot(data=data)
  p5 <- ggplot(data=datm)
  
  p1 <- p1 + geom_point(aes(x=nodes, y=mat_cha, color='Matrix'))
  p1 <- p1 + geom_point(aes(x=nodes, y=nor_cha, color='Normal'))
  p1 <- p1 + geom_point(aes(x=nodes, y=nx_cha, color='NX'))
  p1 <- p1 + theme_bw() + xlab('Nodes') + ylab('Time') + labs(color='Algorithm', title='Time v Nodes')
  
  p2 <- p2 + geom_point(aes(x=edges, y=mat_cha, color='Matrix'))
  p2 <- p2 + geom_point(aes(x=edges, y=nor_cha, color='Normal'))
  p2 <- p2 + geom_point(aes(x=edges, y=nx_cha, color='Nx'))
  p2 <- p2 + theme_bw() + xlab('Edges') + ylab('Time') + labs(color='Algorithm', title='Time v Edges')
  
  p3 <- p3 + geom_point(aes(x=degree, y=mat_cha, color='Matrix'))
  p3 <- p3 + geom_point(aes(x=degree, y=nor_cha, color='Normal'))
  p3 <- p3 + geom_point(aes(x=degree, y=nx_cha, color='Nx'))
  p3 <- p3 + theme_bw() + xlab('Average Degree') + ylab('Time') + labs(color='Algorithm', title='Time vs Average Degree')
  
  p4 <- p4 + geom_point(aes(x=sparsity, y=mat_cha, color='Matrix'))
  p4 <- p4 + geom_point(aes(x=sparsity, y=nor_cha, color='Naive'))
  p4 <- p4 + geom_point(aes(x=sparsity, y=nx_cha, color='NetworkX'))
  p4 <- p4 + theme_bw() + xlab('Sparsity') + ylab('Time') + labs(color='Algorithm', title='Time vs Sparsity')
  
  p5 <- p5 + geom_col(aes(x=name, y=value, fill=variable), position='dodge')
  p5 <- p5 + theme_bw() + xlab('Networks') + ylab('Time (seconds)') + theme(text = element_text(size=10))
  p5 <- p5 + theme(axis.text.x = element_text(angle = 90, hjust = 0))
  p5 <- p5 + theme(legend.title=element_blank(), legend.position = 'bottom')
  p5 <- p5 + scale_fill_manual("", values=c('red', 'green', 'blue'),  breaks=c('mat_cha','nor_cha','nx_cha'), labels=c('Matrix','Naive','NetworkX'))
  return(p5)
  
  pl <- grid.arrange(p1,p2,p3,p4)
  return(pl)
}