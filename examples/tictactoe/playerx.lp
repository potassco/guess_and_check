#const n=3.
n { x(1..n,1..n) } n.
:- not win.
win :- I=1..n, x(I,J) : J=1..n.  
win :- J=1..n, x(I,J) : I=1..n.  
win :- x(I,I) : I=1..n.
win :- x(I,n+1-I) : I=1..n.

%%% o cells are blocked
:- holds(o(I,J)), x(I,J).
