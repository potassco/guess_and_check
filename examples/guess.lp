dom(1..3).
1 { a(X) : dom(X) }.
#show a/1.

b(X) :- __c(X).
__c(1..3).
#show __c/1.
___d.
% define holds/1
holds(a(X)) :- a(X).
