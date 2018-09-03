%
% base part
%

dom(1..5).
{ a(X) : dom(X) }.
#show a/1.

{ b(1) }.
#show b/1.
#project b/1.


%
% multi part
%

% holds/1 definition
holds(a(X)) :- a(X).

% heuristics using prev
#heuristic a(X) :     prev(a(X)),         not first. [-1,sign]
#heuristic a(X) : not prev(a(X)), dom(X), not first. [ 1,sign]

% externals
#external prev(a(X)) : dom(X).
#external first.
