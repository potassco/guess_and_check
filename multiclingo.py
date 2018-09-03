#script (python)


# imports
import clingo


# defines
UNKNOWN = 0
UNSATISFIABLE = 1
SATISFIABLE = 2
HOLDS = "holds"
PREV = "prev"
FIRST = "first"


class ProgramGroundObserver:

    def __init__(self, control, projection):
        control.register_observer(self)
        self.projection = True if projection==1 else False
        if self.projection:
            self.atoms = []
        else:
            self.atoms = set()
        self.minimization = {}

    def get_atoms(self):
        if self.projection:
            return self.atoms
        else:
            return sorted(list(self.atoms))

    def get_minimization(self):
        keys = sorted(self.minimization.keys(), reverse=True)
        return [sorted(list(self.minimization[key])) for key in keys]

    #
    # observe
    #

    def project(self, atom):
        if self.projection:
            self.atoms.append(atom[0])

    def rule(self, choice, head, body):
        if not self.projection:
            self.atoms.update(head)

    def weight_rule(self, choice, head, lower_bound, body):
        if not self.projection:
            self.atoms.update(head)

    def minimize(self, priority, literals):
        level = self.minimization.get(priority)
        if level is None:
            level = set()
            self.minimization[priority] = level
        level.update(literals)


class Controller:

    def __init__(self, control, projection):
        self.control = control
        self.calls = 0
        self.result = UNKNOWN
        self.prev = []
        self.last_prev = []
        self.atoms = []
        self.model = []
        self.cost = []
        self.minimization = []
        # observer and backend
        self.observer = ProgramGroundObserver(control, projection)
        self.backend = self.control.backend()

    def ground(self, *args, **kwargs):
        self.control.ground(*args, **kwargs)
        self.atoms = self.observer.get_atoms()
        self.minimization = self.observer.get_minimization()
        del self.observer

    def on_model(self, model):
        # set result and print call number
        self.result = SATISFIABLE
        print("Call: {}".format(self.calls))
        # if optimization:
        # set last_prev, prev, model and cost
        self.last_prev = self.prev
        self.prev = [
            atom.symbol.arguments
            for atom in self.control.symbolic_atoms.by_signature(HOLDS, 1)
            if atom.symbol in model.symbols(atoms=True)
        ]
        self.model = [i for i in self.atoms if model.is_true(i)]
        self.cost = model.cost

    def solve(self, *args, **kwargs):
        # set external prev/1
        for atom in self.last_prev:
            self.control.assign_external(clingo.Function(PREV, atom), False)
        for atom in self.prev:
            self.control.assign_external(clingo.Function(PREV, atom),  True)
        # set external first/0
        if self.calls == 0:
            self.control.assign_external(clingo.Function(FIRST, []),  True)
        elif self.calls == 1:
            self.control.release_external(clingo.Function(FIRST, []))
        # add constraint for last model
        if self.calls == 0:
            self.backend.__enter__()
        if self.calls > 0:
            body = self.model + [-a for a in self.atoms if a not in self.model]
            self.backend.add_rule([], body, False)
        # if calls == 1 and optimization: add constraint
        if self.calls == 1 and self.cost != []:
            # just in case:
            if len(self.cost) != len(self.minimization):
                raise Exception("ERROR (multiclingo): implementation error")
            # iterate over levels
            for idx, cost in enumerate(self.cost):
                level = self.minimization[idx]
                self.backend.add_weight_rule([], cost+1, level, False)
                total = sum([abs(w) for _, w in level])
                body = [(-l,w) for l, w in level]
                self.backend.add_weight_rule([], total-cost+1, body, False)
        # solve and return result
        self.result = UNSATISFIABLE
        self.calls += 1
        self.control.solve(on_model = self.on_model, *args, **kwargs)
        return self.result


#
# main
#

def get(val, default):
    return val if val != None else default

def main(control):

    # options
    max_models = get(control.get_const("models"),  clingo.Number(1)).number
    projection = get(control.get_const("project"), clingo.Number(0)).number

    # loop
    controller = Controller(control, projection)
    controller.ground([("base", [])])
    models = 0
    while models < max_models or max_models == 0:
        result = controller.solve()
        if result == SATISFIABLE:
            models += 1
        else:
            break
#end.
