%%% generate holds atoms for the check part
holds(occurs(A,T)) :- occurs(A,T).

%%% The plan cannot fail
:- fail.
