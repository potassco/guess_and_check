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
usage: gc.py [--binary] [number] [options] [guess_files] -C [check_files]
```

* The `number` and the `options` are passed to `clingo`, 
`guess_files` define `G`, and the `check_files` define `C`. 
* Option `--binary` uses a clingo binary (which sould be installed in the system) for reifying the check program. 
  By default, the reification is performed using the Python API of clingo.

Predicate `holds/1` should not appear in any head of `C`.

The script requires `clingo` Python library. It has been tested with `clingo` version `5.3.0`.

## Examples:

* Program `guess.lp`:
```bash

```

* Execution:
```bash
$ src/gc.py examples/guess
```
