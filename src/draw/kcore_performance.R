library('ggplot2')
require(gridExtra)
library(latex2exp)

plotChangeDetect <- function(fname) {
  data <- read.csv(fname, header = TRUE, sep = ',')
  
  p1 <- ggplot(data=data)
  p2 <- ggplot(data=data)
  p3 <- ggplot(data=data)
  p4 <- ggplot(data=data)
  p5 <- ggplot(data=data)
  
  p1 <- p1 + geom_crossbar(aes(x=nodes, y=mat_time, ymin=mat_time-mat_std, ymax=mat_time+mat_std, color='Matrix'))
  p1 <- p1 + geom_crossbar(aes(x=nodes, y=nor_time, ymin=nor_time-mat_std, ymax=nor_time+mat_std, color='Normal'))
  p1 <- p1 + geom_point(aes(x=nodes, y=mat_time, color='Matrix'))
  p1 <- p1 + geom_point(aes(x=nodes, y=nor_time, color='Normal'))
  p1 <- p1 + theme_bw() + xlab('Nodes') + ylab('Time') + labs(color='Algorithm', title='Time v Nodes')
  
  p2 <- p2 + geom_crossbar(aes(x=edges, y=mat_time, ymin=mat_time-mat_std, ymax=mat_time+mat_std, color='Matrix'))
  p2 <- p2 + geom_crossbar(aes(x=edges, y=nor_time, ymin=nor_time-mat_std, ymax=nor_time+mat_std, color='Normal'))
  p2 <- p2 + geom_point(aes(x=edges, y=mat_time, color='Matrix'))
  p2 <- p2 + geom_point(aes(x=edges, y=nor_time, color='Normal'))
  p2 <- p2 + theme_bw() + xlab('Edges') + ylab('Time') + labs(color='Algorithm', title='Time v Edges')
  
  p3 <- p3 + geom_crossbar(aes(x=nodes*edges, y=mat_time, ymin=mat_time-mat_std, ymax=mat_time+mat_std, color='Matrix'))
  p3 <- p3 + geom_crossbar(aes(x=nodes*edges, y=nor_time, ymin=nor_time-mat_std, ymax=nor_time+mat_std, color='Normal'))
  p3 <- p3 + geom_point(aes(x=nodes*edges, y=mat_time, color='Matrix'))
  p3 <- p3 + geom_point(aes(x=nodes*edges, y=nor_time, color='Normal'))
  p3 <- p3 + theme_bw() + xlab(TeX('Nodes $\\times$ Edges')) + ylab('Time') + labs(color='Algorithm', title=TeX('Time v Nodes $\\times$ Edges'))
  
  p4 <- p4 + geom_crossbar(aes(x=degree, y=mat_time, ymin=mat_time-mat_std, ymax=mat_time+mat_std, color='Matrix'))
  p4 <- p4 + geom_crossbar(aes(x=degree, y=nor_time, ymin=nor_time-mat_std, ymax=nor_time+mat_std, color='Normal'))
  p4 <- p4 + geom_point(aes(x=degree, y=mat_time, color='Matrix'))
  p4 <- p4 + geom_point(aes(x=degree, y=nor_time, color='Normal'))
  p4 <- p4 + theme_bw() + xlab('Avgerage Degree') + ylab('Time') + labs(color='Algorithm', title='Time v Average Degree')
  
  p5 <- p5 + geom_crossbar(aes(x=name, y=mat_time, ymin=mat_time-mat_std, ymax=mat_time+mat_std, color='Matrix'))
  p5 <- p5 + geom_crossbar(aes(x=name, y=nor_time, ymin=nor_time-mat_std, ymax=nor_time+mat_std, color='Normal'))
  p5 <- p5 + theme_bw() + xlab('Avgerage Degree') + ylab('Time') + labs(color='Algorithm', title='Time v Average Degree')
  
  pl <- grid.arrange(p1,p2,p4)
  return(pl)
}