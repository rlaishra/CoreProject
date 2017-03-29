computeMonotonic <- function(data) {
  m <- 0
  for (i in 1:length(data)-1){
    u = data[i - 1]
    v = data[i]
    w = data[i + 1]
    
    if((u < v) & (v > w)) {
      
    }
  }
}