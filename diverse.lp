%
% base part
%

dom(1..4).
2 { a(X) : dom(X) }.
#show a/1.

{ b(1) }.
#show b/1.
#project b/1.

#minimize{
  1@1,X: a(X), minimize=1;
  1@2,X: b(X), minimize=1
}.

%
% multi part
%

% heuristics using prev
#heuristic a(X) :     prev(a(X)),         not first. [1,false]
#heuristic a(X) : not prev(a(X)), dom(X), not first. [1, true]

% holds/1 definition
holds(a(X)) :- a(X).

% externals
#external first.
#external prev(a(X)) : dom(X).
