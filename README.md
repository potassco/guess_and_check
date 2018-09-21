# guess_and_check
An implementation of Guess and Check Answer Set Programming in clingo.


## Description

## Options


## Syntax

## Example: enumerating diverse stable models

* Program `diverse.lp`:
```bash
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
```

* Execution (all models, projecting on b/1, no optimization):
```bash
$ clingo multiclingo.py diverse.lp -c models=0 -c project=1 -c minimize=0 --heuristic=Domain
clingo version 5.3.0
Reading from multiclingo.py ...
Solving...
Call: 1
Answer: 1
a(1) a(2)
Solving...
Call: 2
Answer: 1
a(3) a(4) b(1)
Solving...
UNSATISFIAB:!LE

Models       : 2
Calls        : 3
Time         : 0.015s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.016s

```

* Execution (2 models, no projection, optimization):
```bash
$ clingo multiclingo.py diverse.lp -c models=2 -c project=0 -c minimize=1 --heuristic=Domain
clingo version 5.3.0
Reading from multiclingo.py ...
Solving...
Call: 1
Answer: 1
a(1) a(2)
Optimization: 0 2
Solving...
Call: 2
Answer: 1
a(3) a(4)
Optimization: 0 2
OPTIMUM FOUND

Models       : 2
  Optimum    : yes
Optimization : 0 2
Calls        : 2
Time         : 0.016s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.016s

```
