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

drawKendallCorrelation <- function(fname, t) {
  data <- read.csv(file = fname, sep = ',')
  pl <- ggplot(data = data, aes(x=missing))
  pl <- pl + geom_point(aes(y = correlation, color='All'))
  pl <- pl + geom_point(aes(y = correlation_20, color='Top 20%'))
  #pl <- pl + geom_point(aes(y = correlation_10, color='Top 10%'))
 #pl <- pl + geom_point(aes(y = correlation_5, color='Top 5%'))
  
  if(t == 'n'){
    pl <- pl + labs(x='Missing Nodes (%)', y='Kendal Tau Correlation')
  } else if (t == 'e') {
    pl <- pl + labs(x='Missing Edges (%)', y='Kendal Tau Correlation')
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
  pl <- pl + geom_line(aes(y = missing_0, color='Removed 0'))
  pl <- pl + geom_line(aes(y = missing_2, color='Removed 2'))
  pl <- pl + geom_line(aes(y = missing_4, color='Removed 4'))
  pl <- pl + geom_line(aes(y = missing_6, color='Removed 6'))
  pl <- pl + geom_line(aes(y = missing_8, color='Removed 8'))
  pl <- pl + geom_line(aes(y = missing_10, color='Removed 10'))
  pl <- pl + geom_line(aes(y = missing_12, color='Removed 12'))
  pl <- pl + geom_line(aes(y = missing_14, color='Removed 14'))
  pl <- pl + geom_line(aes(y = missing_16, color='Removed 16'))
  pl <- pl + geom_line(aes(y = missing_18, color='Removed 18'))
  pl <- pl + geom_line(aes(y = missing_20, color='Removed 20'))
  pl <- pl + geom_line(aes(y = missing_22, color='Removed 22'))
  pl <- pl + geom_line(aes(y = missing_24, color='Removed 24'))
  pl <- pl + geom_line(aes(y = missing_26, color='Removed 26'))
  pl <- pl + geom_line(aes(y = missing_28, color='Removed 28'))
  pl <- pl + geom_line(aes(y = missing_30, color='Removed 30'))
  pl <- pl + geom_line(aes(y = missing_32, color='Removed 32'))
  pl <- pl + geom_line(aes(y = missing_34, color='Removed 34'))
  pl <- pl + geom_line(aes(y = missing_36, color='Removed 36'))
  pl <- pl + geom_line(aes(y = missing_38, color='Removed 38'))
  pl <- pl + geom_line(aes(y = missing_40, color='Removed 40'))
  pl <- pl + geom_line(aes(y = missing_42, color='Removed 42'))
  pl <- pl + geom_line(aes(y = missing_44, color='Removed 44'))
  pl <- pl + geom_line(aes(y = missing_46, color='Removed 46'))
  pl <- pl + geom_line(aes(y = missing_48, color='Removed 48'))
  
  pl <- pl + labs(x='Core Number', y='Number of nodes')
  
  return(pl)
}
