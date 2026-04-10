#
# IMPORTS
#

import clingo
import guess_and_check.metasp_programs as metasp_programs
import guess_and_check.reify as reify
import sys
import re

#
# DEFINES
#

STATE_G = 0
STATE_C = 1
HELP = """\
usage: guess-and-check [--binary] [--check-to-sat] [number] [options] [guess_files] -C [check_files]
"""
ANSWER = """\
Answer {}:
{}"""
HOLDS = "holds"
BINDING_PYTHON = """
##true(atom(A)) :-     holds(X), ##output(holds(X),A).
##fail(atom(A)) :- not holds(X), ##output(holds(X),A).
:- not ##bot.
"""
BINDING_BINARY = """
##true(atom(A)) :-     holds(X), ##output(holds(X),B), ##literal_tuple(B,A).
##fail(atom(A)) :- not holds(X), ##output(holds(X),B), ##literal_tuple(B,A).
:- not ##bot.
"""


#
# METHODS
#


class Observer:

    def __init__(self):
        self.rules = []
        self.weight_rules = []
        self.output_atoms = []
        self.output_terms = []

    def rule(self, choice, head, body):
        self.rules.append((choice, head, body))

    def weight_rule(self, choice, head, lower_bound, body):
        self.weight_rules.append((choice, head, lower_bound, body))

    def output_atom(self, symbol, atom):
        self.output_atoms.append((symbol, atom))

    def output_term(self, symbol, condition):
        self.output_terms.append((symbol, condition))


def parse_args():
    options, guess, check = [], [], []
    state = STATE_G
    binary = False
    toSat = False
    for i in sys.argv[1:]:
        if i == "--help":
            print(HELP)
            sys.exit(0)
        if i == "--binary":
            binary = True
        elif i == "--check-to-sat":
            toSat = True
        elif i == "-C":
            state = STATE_C
        elif i.startswith("-") or i.isdigit():
            options.append(i)
        elif state == STATE_G:
            guess.append(i)
        else:
            check.append(i)
    return options, binary, toSat, guess, check


def observe(program):
    observer = Observer()
    control = clingo.Control()
    control.register_observer(observer, replace=True)
    control.add("base", [], program)
    control.ground([("base", [])])
    return observer


def get_prefix(control):
    prefix = "_"
    for name, _, _ in control.symbolic_atoms.signatures:
        if name.startswith(prefix):
            prefix = re.sub(r"(_+).*", r"\1", name) + "_"
    return prefix


def solve_guess_and_check(
    options, binary, toSat, guess_files, check_files, on_model=None
) -> bool:
    """
    Solve a guess and check program and return whether it is satisfiable.
    """
    control = clingo.Control(options)

    # load guess and ground
    for _file in guess_files:
        control.load(_file)
    control.ground([("base", [])])

    # get choices
    choices = (
        "{ "
        + "; ".join(
            str(atom.symbol) for atom in control.symbolic_atoms.by_signature(HOLDS, 1)
        )
        + " }."
    )
    choices = "" if choices == "{  }." else choices

    # create check
    check = choices + "\n#show holds/1.\n"
    for _file in check_files:
        with open(_file, "r") as f:
            check += f.read() + "\n"

    # fix prefix
    prefix = get_prefix(control)

    # reify check
    if binary:
        check_reified = reify.reify_from_string(check, prefix)
        check_reified += BINDING_BINARY.replace("##", prefix)
    elif toSat:
        check_reified = reify.reify_from_string_through_sat(check, prefix)
        check_reified += BINDING_BINARY.replace("##", prefix)
    else:
        observer = observe(check)
        check_reified = reify.reify_from_observer(observer, prefix)
        check_reified += BINDING_PYTHON.replace("##", prefix)
    # add meta encoding
    check_reified += metasp_programs.metaD_program.replace("##", prefix)

    # add to control and ground
    control.add("check", [], check_reified)
    control.ground([("check", [])])

    # solve
    models = 0
    with control.solve(yield_=True, on_model=on_model) as handle:
        for m in handle:
            models += 1
            if not on_model:
                model = " ".join([str(x) for x in m.symbols(shown=True)])
                print(ANSWER.format(models, model))
        if not on_model:
            print(handle.get())

    return models > 0
