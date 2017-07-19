library('ggplot2')

drawNodesFoundTruss <- function(fname, t) {
  data <- read.csv(file = fname, sep = ',')

  pl <- ggplot(data = data, aes(x=missing))

  alp = 0

  pl <- pl + geom_smooth(aes(y = truss2, color = '2_truss'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = truss4, color = '4_truss'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = truss6, color = '6_truss'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = truss8, color = '8_truss'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = truss10, color = '10_truss'), alpha = alp)
  
  if(t == 'n'){
    pl <- pl + labs(x='Missing Nodes (%)', y='Core Nodes (%)')
  } else if (t == 'e') {
    pl <- pl + labs(x='Missing Edges (%)', y='Core Nodes (%)')
  }

  return(pl)
}

drawNodesFoundCore <- function(fname, t) {
  data <- read.csv(file = fname, sep = ',')

  pl <- ggplot(data = data, aes(x=missing))

  alp = 0

  pl <- pl + geom_smooth(aes(y = core2, color = '2_core'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = core4, color = '4_core'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = core6, color = '6_core'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = core8, color = '8_core'), alpha = alp)
  pl <- pl + geom_smooth(aes(y = core10, color = '10_core'), alpha = alp)

  if(t == 'n'){
    pl <- pl + labs(x='Missing Nodes (%)', y='Core Nodes (%)')
  } else if (t == 'e') {
    pl <- pl + labs(x='Missing Edges (%)', y='Core Nodes (%)')
  }

  return(pl)
}

drawKendallCorrelation <- function(fname, t, d) {
  data <- read.csv(file = fname, sep = ',')
  pl <- ggplot(data = data, aes(x=change))
  
  if (d == 'd') {
    pl <- pl + geom_jitter(aes(y = correlation_100, color='All'))
    pl <- pl + geom_jitter(aes(y = correlation_20, color='Top 20%'))
    pl <- pl + geom_jitter(aes(y = correlation_10, color='Top 10%'))
    pl <- pl + geom_jitter(aes(y = correlation_5, color='Top 5%'))
  } else if (d == 's') {
    pl <- pl + geom_smooth(aes(y = correlation_100, color='All'), alpha=0)
    #pl <- pl + geom_smooth(aes(y = correlation_20, color='Top 20%'), alpha=0)
    pl <- pl + geom_smooth(aes(y = correlation_10, color='Top 10%'), alpha=0)
    pl <- pl + geom_smooth(aes(y = correlation_5, color='Top 5%'), alpha=0)
  } else if (d == 'p') {
    pl <- pl + geom_point(aes(y = correlation_100, color='All'))
    pl <- pl + geom_point(aes(y = correlation_20, color='Top 20%'))
    pl <- pl + geom_point(aes(y = correlation_10, color='Top 10%'))
    pl <- pl + geom_point(aes(y = correlation_5, color='Top 5%'))
  } else if (d == 'l') {
    pl <- pl + geom_line(aes(y = correlation_100, color='All'))
    pl <- pl + geom_line(aes(y = correlation_20, color='Top 20%'))
    pl <- pl + geom_line(aes(y = correlation_10, color='Top 10%'))
    pl <- pl + geom_line(aes(y = correlation_5, color='Top 5%'))
  }
  
  if(t == 'n'){
    pl <- pl + labs(x='Missing Nodes (%)', y='Kendal Tau Correlation')
  } else if (t == 'e') {
    pl <- pl + labs(x='Missing Edges (%)', y='Kendal Tau Correlation')
  } else if (t == 'r') {
    pl <- pl + labs(x='Edges Rewired (%)', y='Kendal Tau Correlation')
  } else if (t == 'd') {
    pl <- pl + labs(x='Days', y='Kendal Tau Correlation')
  }
  
  return(pl)
}

drawMeanKendallCorrelation <- function(fname, t) {
  data <- read.csv(file = fname, sep = ',')
  pl <- ggplot(data = data, aes(x=change))
  
  pl <- pl + geom_line(aes(y = correlation_kt_100, color='All'))
  #pl <- pl + geom_line(aes(y = correlation_kt_80, color='Top 80%'))
  pl <- pl + geom_line(aes(y = correlation_kt_50, color='Top 50%'))
  pl <- pl + geom_line(aes(y = correlation_kt_20, color='Top 20%'))
 # pl <- pl + geom_line(aes(y = correlation_kt_20, color='Top 20%'))
  #pl <- pl + geom_line(aes(y = correlation_5, color='Top 5%'))
  
  pl <- pl + geom_ribbon(aes(ymin=correlation_kt_100 - std_kt_100, ymax=correlation_kt_100 + std_kt_100, fill='All'), alpha=0.2)
  pl <- pl + geom_ribbon(aes(ymin=correlation_kt_50 - std_kt_50, ymax=correlation_kt_50 + std_kt_50, fill='Top 50%'), alpha=0.2)
  pl <- pl + geom_ribbon(aes(ymin=correlation_kt_20 - std_kt_20, ymax=correlation_kt_20 + std_kt_20, fill='Top 20%'), alpha=0.2)
 # pl <- pl + geom_ribbon(aes(ymin=correlation_kt_10 - std_kt_10, ymax=correlation_kt_10 + std_kt_10, fill='Top 10%'), alpha=0.2)
  #pl <- pl + geom_ribbon(aes(ymin=correlation_5-std_5, ymax=correlation_5+std_5, fill='Top 5%'), alpha=0.2)
  
  if(t == 'n'){
    pl <- pl + labs(x='Missing Nodes (%)', y='Kendal Tau Correlation')
  } else if (t == 'e') {
    pl <- pl + labs(x='Missing Edges (%)', y='Kendal Tau Correlation')
  } else if (t == 'r') {
    pl <- pl + labs(x='Edges Rewired (%)', y='Kendal Tau Correlation')
  }
  
  return(pl)
}

drawDegreeDist <- function(fname) {
  data <- read.csv(file = fname, sep = ',')
  
  pl <- ggplot(data = data, aes(x=degree))
  pl <- pl + geom_point(aes(y = removed_0, color='Removed 0'))
  #pl <- pl + geom_point(aes(y = removed_16))
  pl <- pl + geom_point(aes(y = removed_18, color='Removed 18'))
  pl <- pl + geom_point(aes(y = removed_20, color='Removed 20'))
  pl <- pl + geom_point(aes(y = removed_22, color='Removed 22'))
  #pl <- pl + geom_point(aes(y = removed_24))
  
  pl <- pl + scale_y_log10() + scale_x_log10()
  
  return(pl)
}

drawCoreNumberHistogram <- function(fname) {
  data <- read.csv(file = fname, sep = ',')
  pl <- ggplot(data = data, aes(x=core_number))
  pl <- pl + geom_line(aes(y = change_0, color='Removed 0'))
  pl <- pl + geom_line(aes(y = change_2, color='Removed 2'))
  pl <- pl + geom_line(aes(y = change_4, color='Removed 4'))
  pl <- pl + geom_line(aes(y = change_6, color='Removed 6'))
  pl <- pl + geom_line(aes(y = change_8, color='Removed 8'))
  pl <- pl + geom_line(aes(y = change_10, color='Removed 10'))
  pl <- pl + geom_line(aes(y = change_12, color='Removed 12'))
  pl <- pl + geom_line(aes(y = change_14, color='Removed 14'))
  pl <- pl + geom_line(aes(y = change_16, color='Removed 16'))
  pl <- pl + geom_line(aes(y = change_18, color='Removed 18'))
  pl <- pl + geom_line(aes(y = change_20, color='Removed 20'))
  pl <- pl + geom_line(aes(y = change_22, color='Removed 22'))
  pl <- pl + geom_line(aes(y = change_24, color='Removed 24'))
  pl <- pl + geom_line(aes(y = change_26, color='Removed 26'))
  pl <- pl + geom_line(aes(y = change_28, color='Removed 28'))
  pl <- pl + geom_line(aes(y = change_30, color='Removed 30'))
  pl <- pl + geom_line(aes(y = change_32, color='Removed 32'))
  pl <- pl + geom_line(aes(y = change_34, color='Removed 34'))
  pl <- pl + geom_line(aes(y = change_36, color='Removed 36'))
  pl <- pl + geom_line(aes(y = change_38, color='Removed 38'))
  pl <- pl + geom_line(aes(y = change_40, color='Removed 40'))
  pl <- pl + geom_line(aes(y = change_42, color='Removed 42'))
  pl <- pl + geom_line(aes(y = change_44, color='Removed 44'))
  pl <- pl + geom_line(aes(y = change_46, color='Removed 46'))
  pl <- pl + geom_line(aes(y = change_48, color='Removed 48'))
  
  pl <- pl + labs(x='Core Number', y='Number of nodes')
  
  return(pl)
}

drawCoreTriangle <- function(fname) {
  data <- read.csv(file = fname, sep = ' ')
  
  pl <- ggplot(data = data, aes(x=core))
  pl <- pl + geom_point(aes(y=triangles))
  pl <- pl + geom_density2d(aes(y=triangles))
  
  pl <- pl + labs(x='Core Number', y='4-Cliques Count')
  
  return(pl)
}

drawHistogram <- function(fname){
  data <- read.csv(file = fname, sep = '\t')
  
  pl <- ggplot(data=data, aes(x=core))
  pl <- pl + geom_line(aes(y=count))
  pl <- pl + labs(x='Core Number', y='Count')
  
  return(pl)
}

drawError <- function(fname,k) {
  data <- read.csv(fname, header=TRUE, sep=',')
  p <- ggplot()
  p <- p + geom_point(data=data[which(data$core==k),], aes(x=components, y=error_0.2))
  #p <- p + geom_line(data=data[which(data$core==k),], aes(x=components, y=error_1))
  return(p)
}

compareRobustness <- function(fname) {
  fname0 <- paste(fname, '_0_core_mean_edges_delete_random.csv', sep = '')
  fname1 <- paste(fname, '_1_core_mean_edges_delete_random.csv', sep = '')
  fname2 <- paste(fname, '_2_core_mean_edges_delete_random.csv', sep = '')
  fname3 <- paste(fname, '_3_core_mean_edges_delete_random.csv', sep = '')
  fname4 <- paste(fname, '_4_core_mean_edges_delete_random.csv', sep = '')
  fname5 <- paste(fname, '_5_core_mean_edges_delete_random.csv', sep = '')
  fname6 <- paste(fname, '_6_core_mean_edges_delete_random.csv', sep = '')
  fname7 <- paste(fname, '_7_core_mean_edges_delete_random.csv', sep = '')
  fname8 <- paste(fname, '_8_core_mean_edges_delete_random.csv', sep = '')
  fname9 <- paste(fname, '_9_core_mean_edges_delete_random.csv', sep = '')
  fname10 <- paste(fname, '_10_core_mean_edges_delete_random.csv', sep = '')
  
  d0 <- read.csv(fname0, header = TRUE, sep = ',')
  d1 <- read.csv(fname1, header = TRUE, sep = ',')
  d2 <- read.csv(fname2, header = TRUE, sep = ',')
  d3 <- read.csv(fname3, header = TRUE, sep = ',')
  d4 <- read.csv(fname4, header = TRUE, sep = ',')
  d5 <- read.csv(fname5, header = TRUE, sep = ',')
  d6 <- read.csv(fname6, header = TRUE, sep = ',')
  d7 <- read.csv(fname7, header = TRUE, sep = ',')
  d8 <- read.csv(fname8, header = TRUE, sep = ',')
  d9 <- read.csv(fname9, header = TRUE, sep = ',')
  d10 <- read.csv(fname10, header = TRUE, sep = ',')
  
  pl <- ggplot()
  
  pl <- pl + geom_line(data = d0, aes(x=change, y=correlation_mean_10, color='00'))
  pl <- pl + geom_line(data = d1, aes(x=change, y=correlation_mean_10, color='01'))
  pl <- pl + geom_line(data = d2, aes(x=change, y=correlation_mean_10, color='02'))
  pl <- pl + geom_line(data = d3, aes(x=change, y=correlation_mean_10, color='03'))
  pl <- pl + geom_line(data = d4, aes(x=change, y=correlation_mean_10, color='04'))
  pl <- pl + geom_line(data = d5, aes(x=change, y=correlation_mean_10, color='05'))
  pl <- pl + geom_line(data = d6, aes(x=change, y=correlation_mean_10, color='06'))
  pl <- pl + geom_line(data = d7, aes(x=change, y=correlation_mean_10, color='07'))
  pl <- pl + geom_line(data = d8, aes(x=change, y=correlation_mean_10, color='08'))
  pl <- pl + geom_line(data = d9, aes(x=change, y=correlation_mean_10, color='09'))
  pl <- pl + geom_line(data = d10, aes(x=change, y=correlation_mean_10, color='10'))
  
  pl <- pl + geom_ribbon(data = d0, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='00'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d1, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='01'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d2, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='02'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d3, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='03'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d4, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='04'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d5, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='05'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d6, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='06'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d7, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='07'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d8, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='08'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d9, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='09'), alpha=0.1)
  pl <- pl + geom_ribbon(data = d10, aes(x=change, ymin=correlation_mean_10 - correlation_std_10, ymax=correlation_mean_10 + correlation_std_10, fill='10'), alpha=0.1)
  
  
  return(pl)
}