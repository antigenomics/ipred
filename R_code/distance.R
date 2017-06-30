# https://johanndejong.wordpress.com/2015/10/02/faster-hamming-distance-in-r-2/

hamming <- function(X, Y) {
  if ( missing(Y) ) {
    uniqs <- unique(as.vector(X))
    print(uniqs)
    U <- X == uniqs[1]
    H <- t(U) %*% U
    for ( uniq in uniqs[-1] ) {
      U <- X == uniq
      H <- H + t(U) %*% U
    }
  } else {
    uniqs <- union(X, Y)
    H <- t(X == uniqs[1]) %*% (Y == uniqs[1])
    for ( uniq in uniqs[-1] ) {
      H <- H + t(X == uniq) %*% (Y == uniq)
    }
  }
  nrow(X) - H
}

a <- c("a","b","c")
b <- c("c","a","b")
d <- c("c","a","a")
e <- data.frame(a,a,b,d)
f <- data.frame(b)
hamming(as.matrix(e),as.matrix(f))