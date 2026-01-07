from itertools import chain, combinations

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))


class Dependency:
    def __init__(self, determinant: set, determined: set):
        self.determinant = determinant
        self.determined = determined

    def __repr__(self):
        return (f"{self.determinant} -> {self.determined}")

    def __eq__(self, other: Dependency):
        if self.determinant == other.determinant and \
        self.determined == other.determined:
            return True
        return False

    def __hash__(self):
        return hash((frozenset(self.determinant), frozenset(self.determined)))

    def is_trivial(self):
        return self.determined.issubset(self.determinant)

    def augment(self, attribute: set) -> Dependency:
        if not isinstance(attribute, set):
            attribute = {attribute}
        return Dependency(
            self.determinant | attribute,
            self.determined | attribute
        )

    def reflexivity(self) -> set["Dependency"]:
        return {
            Dependency(self.determinant, set(subset))
            for subset in powerset(self.determinant) if subset
        }

    def transitivity(self, other: Dependency) -> Dependency:
        if self.determined == other.determinant:
            return Dependency(self.determinant, other.determined)
        else:
            return self

class RelationScheme:
    def __init__(self, attributes: set, dependencies: set[dependencies]):
        self.attributes = attributes
        self.dependencies = dependencies

    def __repr__(self):
        return '\n'.join({str(d) for d in self.dependencies})

    def apply_augment(self):
        new_dependencies = {
            d.augment(a)
            for d in self.dependencies
            for a in self.attributes
        }
        self.dependencies |= new_dependencies

    def apply_reflexivity(self):
        new_dependencies = {
            reflexive_dep 
            for d in self.dependencies 
            for reflexive_dep in d.reflexivity()
        }
        self.dependencies |= new_dependencies

    def apply_transitivity(self):
        new_dependencies = {
            d1.transitivity(d2)
            for d1 in self.dependencies
            for d2 in self.dependencies
        }
        self.dependencies |= new_dependencies

    def armstrong_closure(self):
        prev_n = 0
        while prev_n < len(self.dependencies):
            prev_n = len(self.dependencies)
            self.apply_reflexivity()
            self.apply_augment()
            self.apply_transitivity()

    def filter_non_trivials(self):
        self.dependencies = {d for d in self.dependencies if not d.is_trivial()}


if __name__=="__main__":

    r = RelationScheme(
        {"CodiceFiscale", "Nome", "Cognome", "Regione"},
        {
            Dependency({"CodiceFiscale"}, {"Nome", "Cognome", "Provincia"}),
            Dependency({"Provincia"}, {"Regione"}),
        }
    )

    r.armstrong_closure()
    total = len(r.dependencies)
    r.filter_non_trivials()
    non_trivials = len(r.dependencies)
    print(*r.dependencies, sep='\n')
    print(f'dipendenze non banali: {non_trivials}')
    print(f'dipendenze banali: {total-non_trivials}')

