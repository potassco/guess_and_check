%%% translate holds atoms from guess part
occurs(A,T) :- holds(occurs(A,T)).

%%% the plan has to fail
:- not fail.
