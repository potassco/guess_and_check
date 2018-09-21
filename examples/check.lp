dom(1..3).
1 { a(X) : dom(X) }.

% subset preference
better :- holds(a(X)) :    a(X);
          holds(a(Y)), not a(Y).
:- not better.
