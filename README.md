# multiclingo
A simple approach to multi-shot solving with clingo


## Description
`multiclingo` solves multiple times a logic program.
Given an input program `P`, it computes stable models as follows:
* In step `0`, it computes a stable model `M(1)` of `P` together with fact `first.`.
* In step `n`, for `n>0`, let `P(n)` be the program `P` together with facts `prev(x).` 
  for every `x` such that `holds(x)` was in `M(n-1)`. Then, it computes a stable model `M(n)`
  of `P(n)` that is different to all `M(m)` for `m<n` if it exists, else it returns `UNSATISFIABLE`.

## Options

* Option `-c models=n` sets to `n` the number of stable models to be computed 
  (use `0` to computing all stable models until `UNSATISFIABLE` is returned).
* Option `-c project=1` activates projection (clingo option `--project` has no effect).

## Syntax
The program must define some externals:
* external `first` to represent the first step
* externals `prev(x)` for each atom `holds(x)` that appears in `P`

## Example: enumerating diverse stable models

* Program `diverse.lp`:
```bash
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

% heuristics using prev
#heuristic a(X) :     prev(a(X)),         not first. [-1,sign]
#heuristic a(X) : not prev(a(X)), dom(X), not first. [ 1,sign]

% holds/1 definition
holds(a(X)) :- a(X).

% externals
#external prev(a(X)) : dom(X).
#external first.
```

* Execution:
```bash
$ clingo multiclingo.py diverse.lp -c models=2 -c project=1 --heuristic=Domain
clingo version 5.3.0
Reading from multiclingo.py ...
Solving...
Call: 1
Answer: 1

Solving...
Call: 2
Answer: 1
a(1) a(2) a(3) a(4) a(5) b(1)
SATISFIABLE

Models       : 2+
Calls        : 2
Time         : 0.020s (Solving: 0.00s 1st Model: 0.00s Unsat: 0.00s)
CPU Time     : 0.020s

```
