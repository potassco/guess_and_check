# Guess and Check Answer Set Programming
An implementation of Guess and Check Answer Set Programming in clingo.

The Guess and Check method was introduced by T. Eiter and A. Polleres in:
* Thomas Eiter, Axel Polleres: 
Towards automated integration of guess and check programs in answer set programming: a meta-interpreter and applications. TPLP 6(1-2): 23-60 (2006).

## Description
A Guess and Check program is a pair of logic programs `<G,C>`.
A set of atoms `X` is a stable model of `<G,C>` if `X` is a stable model of `G`, 
and `C` together with `H` is unsatisfiable, 
where `H` contains the facts `holds(x).` for all atoms of the form `holds(x)` in `X`.

The implementation translates a Guess and Check program into a disjunctive logic program, 
that is solved by clingo. 
It uses the meta-programming techniques introduced in:
*	Martin Gebser, Roland Kaminski, Torsten Schaub: Complex optimization in answer set programming. TPLP 11(4-5): 821-839 (2011).


## Usage

```
$ src/gc.py --help
usage: gc.py [--binary] [--check-to-sat] [number] [options] [guess_files] -C [check_files]
```

* Option `--binary` uses a clingo binary (which sould be installed in the system) for reifying the check program.
* Option `--check-to-sat` translates the check program to a SAT problem and then reifies it into ASP facts.
  It uses a clingo binary, and programs
  [lp2normal2](http://research.ics.aalto.fi/software/asp/lp2normal/),
  [lp2acyc](http://research.ics.aalto.fi/software/asp/lp2acyc/), and
  [lp2sat](http://research.ics.aalto.fi/software/asp/lp2sat/), 
  developed by Tomi Janhunen and his group.
  They all should be installed in the system.
* If none of those options is issued, the reification is performed using the Python API of clingo.
* The `number` and the `options` are passed to `clingo`, 
`guess_files` define `G`, and the `check_files` define `C`. 

Predicate `holds/1` should not appear in any head of `C`.

The script requires `clingo` Python library. 
It has been tested with `clingo` version `5.3.0`, `lp2normal2` version `2.18`, `lp2acyc` version `1.29`, and `lp2sat` version `1.9`.

## Examples:

### Basic case:
In this example the check program is always unsatisfiable.
Hence, all the stable models of the guess program are 
also stable models of the guess and check program.
```bash
$ cat examples/basic/a.lp
1 { a(1..3) }.  #show a/1.

$ cat examples/basic/holds.lp
holds(a(X)) :- a(X).

$ cat examples/basic/unsat.lp
:-.

$ gc.py examples/basic/{a.lp,holds.lp} -C examples/basic/unsat.lp 0
Answer 1:
a(3)
Answer 2:
a(2)
Answer 3:
a(2) a(3)
Answer 4:
a(1)
Answer 5:
a(1) a(2)
Answer 6:
a(1) a(3)
Answer 7:
a(1) a(2) a(3)
SAT
```

### Preferences:

In this example we compute subset (or superset) 
optimal answer sets of program `a.lp`.

The part in `a.lp` guesses candidate stable models,
whose atoms are mapped to `holds/1` by `holds.lp`.

The check, with file `subset.lp` (`superset.lp`) generates 
stable models of `a.lp`
that are smaller (bigger) than the one represented by `holds/1` atoms.
```bash
$ cat examples/preferences/a.lp
1 { a(1..3) }.  #show a/1.

$ cat examples/preferences/holds.lp
holds(a(X)) :- a(X).

$ cat examples/preferences/subset.lp
better :- holds(a(X)) :    a(X);
          holds(a(Y)), not a(Y).
:- not better.

$ cat examples/preferences/superset.lp
better :- a(X) :    holds(a(X));
          a(Y), not holds(a(Y)).
:- not better.

$ gc.py examples/preferences/{a.lp,holds.lp} -C examples/preferences/{a.lp,subset.lp} 0
Answer 1:
a(1)
Answer 2:
a(2)
Answer 3:
a(3)
SAT

$ gc.py examples/preferences/{a.lp,holds.lp} -C examples/preferences/{a.lp,superset.lp} 0
Answer 1:
a(1) a(2) a(3)
SAT
```

### Tic-Tac-Toe Game:
In this example there is a 3x3 Tic Tac Toe square. 
Player O has to place her 3 tokens in a winning position
such that afterwards player X cannot place her tokens in a winning position.

```bash
$ cat examples/tictactoe/playero.lp
#const n=3.
n { o(1..n,1..n) } n.
:- not win.
win :- I=1..n, o(I,J) : J=1..n.
win :- J=1..n, o(I,J) : I=1..n.
win :- o(I,I) : I=1..n.
win :- o(I,n+1-I) : I=1..n.
#show o/2.

$ cat examples/tictactoe/holds.lp
holds(o(I,J)) :- o(I,J).

$ cat examples/tictactoe/playerx.lp
#const n=3.
n { x(1..n,1..n) } n.
:- not win.
win :- I=1..n, x(I,J) : J=1..n.
win :- J=1..n, x(I,J) : I=1..n.
win :- x(I,I) : I=1..n.
win :- x(I,n+1-I) : I=1..n.

%%% o cells are blocked
:- holds(o(I,J)), x(I,J).

$ gc.py examples/tictactoe/{playero.lp,holds.lp} -C examples/tictactoe/playerx.lp 0
Answer 1:
o(1,3) o(2,2) o(3,1)
Answer 2:
o(1,1) o(2,2) o(3,3)
SAT
```

### Conformant planning:

Conformant planning can be represented in `QBF` style as:
  
* There exists an initial situation `I`, and a sequence of actions `S` that achieve the goal starting from `I`, such that
  for all initial situations `I'`, `S` achieves the goal starting from `I'`

which is equivalent to:
  
* There exists an initial situation `I`, and a sequence of actions `S` that achieve the goal starting from `I`, such that
  there is no `I'` such that `S` does not achieve the goal starting from `I'`.

In our approach the guess program represents the first exists part:

* Find an initial situation `I`, and a sequence of actions `S` that achieve the goal starting from `I`

and the check program represents the second part:

* Find an initial situation `I'`, such that `S` (given by the guess program) does not achieve the goal starting from `I'`.


In this example we adapt the conformant planning problem of clingo in
  [clingo/examples/reify/example2.lp](https://github.com/potassco/clingo/blob/master/examples/reify/example2.lp).
The file generates all initial situations `I` and all sequences of actions `S`, 
and fact `fail` holds iff `S` does not achieve the goal starting from `I`.

```bash
$ cat examples/conformant/example2_guess.lp
%%% generate holds atoms for the check part
holds(occurs(A,T)) :- occurs(A,T).

%%% The plan cannot fail
:- fail.

$ cat examples/conformant/holds.lp
holds(occurs(A,T)) :- occurs(A,T).


$ cat examples/conformant/example2_check.lp
%%% translate holds atoms from guess part
occurs(A,T) :- holds(occurs(A,T)).

%%% the plan has to fail
:- not fail.

$ gc.py examples/conformant/{example2.lp,example2_guess.lp,holds.lp} -C examples/conformant/{example2.lp,example2_check.lp} --binary
Answer 1:
occurs(cpa_go_down(cpa_e0,cpa_f1,cpa_f0),1) occurs(cpa_step_in(cpa_e0,cpa_f0,cpa_p0),2) occurs(cpa_go_up(cpa_e0,cpa_f0,cpa_f1),3) occurs(cpa_step_out(cpa_e0,cpa_f1,cpa_p0),4) occurs(cpa_collect(cpa_c0,cpa_f1,cpa_p0),5) occurs(cpa_collect(cpa_c1,cpa_f1,cpa_p0),6) occurs(cpa_move_right(cpa_f1,cpa_p0,cpa_p1),7) occurs(cpa_collect(cpa_c0,cpa_f1,cpa_p1),8) occurs(cpa_collect(cpa_c1,cpa_f1,cpa_p1),9)
SAT
```
