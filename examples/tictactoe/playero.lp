#const n=3.
n { o(1..n,1..n) } n.
:- not win.
win :- I=1..n, o(I,J) : J=1..n.  
win :- J=1..n, o(I,J) : I=1..n.  
win :- o(I,I) : I=1..n.
win :- o(I,n+1-I) : I=1..n.
#show o/2.
