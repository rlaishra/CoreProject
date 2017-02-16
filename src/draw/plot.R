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
