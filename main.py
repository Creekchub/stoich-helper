from drafter import *
from dataclasses import dataclass

set_website_title("Stoichiometry")
set_site_information(
    author="Aaron",
    description="Balance chemistry reactions.",
    sources="Thanks to the Drafter docs and my study group.",
    planning=["plan.pdf", "design.pdf"],
    links=["https://github.com/creeekchub/your-repository"]
)

@dataclass
class State:
    solved_equations: list[dict]
    
@route
def index(state: State) -> Page:
    return Page(state, [
        "Enter chemical reactants and products below\n",
        TextBox("reactA", "Reactant A"),
        TextBox("reactB", "Reactant B"),
        TextBox("prodA", "Product A"),
        TextBox("prodB", "Product B (optional)"),
        "\n",
        Button("Balance It", "balance"),
        "\n",
        "There are " + str(len(state.solved_equations)) + " saved equations"
        #Make a button that displays solved equations.
        ])

@route
def balance(state, reactA, reactB, prodA, prodB) -> Page:
    return Page(state, [
        "Data collected:" + reactA + reactB + prodA + prodB + "\n",
        Button("Save it for later!", "save"),
        Button("Return home", "index")
        ])
@route
def save(state, reactA, reactB, prodA, prodB) -> Page:
    new_equation = {
        "Reactant1": reactA,
        "Reactant2": reactB,
        "Product1": prodA,
        "Product2": prodB,
        }
    state.solved_equations.append(new_equation)
    return index(state)

start_server(State([]))
