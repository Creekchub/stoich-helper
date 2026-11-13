from drafter import *
from dataclasses import dataclass
from chempy import balance_stoichiometry

@dataclass
class State:
    react1: str
    react2: str
    prod1: str
    prod2: str
    solved_equations: list[dict]
    error: str
    reac: str
    produc: str
    
@route
def index(state: State) -> Page:
    print(state.solved_equations)
    return Page(state, [
        "Enter chemical reactants and products below\n\n",
        Row(
        Div("Reactant\n", TextBox("reactA"),),
        Div("Reactant\n", TextBox("reactB"),),
        Div("Product\n", TextBox("prodA"),),
        Div("Product\n", TextBox("prodB"),),
        state.error,
            ),
        "\n",
        Button("Balance It", "balance"),
        "\n\n\n",
        "There are " + str(len(state.solved_equations)) + " saved equations",
        Button("Show", "show")
        ])

@route
def balance(state, reactA, reactB, prodA, prodB) -> Page:
    state.react1, state.react2, state.prod1, state.prod2 = reactA, reactB, prodA, prodB #so save() can reference them
    #balance logic before returning page with balanced equation
    reac, produc = balance_stoichiometry({prodA, prodB}, {reactA, reactB})   
    state.reac = reac
    state.produc = produc
    print(reac),
    print(produc),
    
    return Page(state, [
        "Equation Solved",
        Button("Save it for later!", "save"),
        Button("Return home", "index")
        ])
@route
def save(state: State) -> Page:
    new_dict = {
        "reactants": state.reac,
        "products": state.produc,
        }
    
    state.solved_equations.append(new_dict)
    return index(state)

@route
def show(state: State) -> Page:
    print(state.solved_equations)
    return index(state)

start_server(State("Reactant", "Reactant", "Product", "Product", [], "No errors to display", None, None))
