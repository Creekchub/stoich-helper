from drafter import *
from dataclasses import dataclass
from chempy import balance_stoichiometry
from bakery import assert_equal

set_website_title("Stoichiometer")
set_site_information(
    author="Aaron",
    description="Help students who understand stoichiometry balance difficult or tedious reactions quickly.",
    sources="Shoutout drafter and chempy",
    planning=["selection.pdf", "design.pdf"],
    links=["https://github.com/creekchub/stoich-helper"]
)
hide_debug_information()
set_website_framed(False)

#subscripts = [₀,₁,₂,₃,₄,₅,₆,₇,₈,₉]
#numbers = ["1","2","3","4","5","6","7","8","9"]

def makesubs(molecule: str) -> str: #adds subscripts to number characters 
    subscript_map = {ord(str(i)): 0x2080 + i for i in range(10)}
    return molecule.translate(subscript_map)
#cannot be unit tested because copying subscripts crashes drafter

@dataclass
class State:
    react1: str
    react2: str
    prod1: str
    prod2: str
    solved_equations: list[dict]
    error: str #error message, not whether there is an error
    reac: str #current balanced reactant side
    produc: str #current balanced product side
    
@route
def index(state: State) -> Page:
    """main page displaying input fields and error message
    Args:
        state (State): contains relevant reaction data
    Returns:
        (Page): home page
    """
    print(state.solved_equations)
    return Page(state, [
        Image("einstein.png", width=70, height=60),
        "\n",
        change_text_size(Text("Let me help you."), 12),
        "\n",
        change_text_size(change_color(Header("THE \u2728 STOICHIOMETER \u2728", style_text_align = "center"), "rgb(44, 40, 222)"), 22),
        "\n",
        change_background_color(Row(
        Div("Reactant\n", TextBox("reactA"),),
        Div("Reactant\n", TextBox("reactB"),),
        Div("Product\n", TextBox("prodA"),),
        Div("Product\n", TextBox("prodB"),),
        state.error,
            ), "rgb(117, 118, 190)"),
        "\n",
        Button("Balance It", "balance"),
        "\n\n\n",
        "There are " + str(len(state.solved_equations)) + " saved equations",
        Button("Show", "show"),
        "\n\n",
        Button("Periodic Table", "table"),
        ])

@route
def balance(state, reactA, reactB, prodA, prodB) -> Page:
    """chempy balances coefficients. displays it
    Args:
        reactA (str): first reactant slot. input from textbox
        reactB (str): second reactant slot. input from textbox
        prodA (str): first product slot. input from textbox
        prodB (str): second product slot. input from textbox
    Returns:
        index (Page): main page, no changes
    """
    state.error = "No errors" #resets message incase user entered bad input previously
    try:
        balance_stoichiometry({prodA, prodB}, {reactA, reactB})
    except Exception: #catchall incase user input is bad or chempy misunderstands
        state.error = " Error: Enter valid chemical formula. Make sure only same elements exist on both sides."
        return index(state)
        
    state.react1, state.react2, state.prod1, state.prod2 = reactA, reactB, prodA, prodB #so save() can reference them
    #balance logic before returning page with balanced equation
    produc, reac = balance_stoichiometry({prodA, prodB}, {reactA, reactB})   
    state.reac = reac
    state.produc = produc
    print(reac),
    print(produc),
    
    reaction_message = " "
    for key in reac: #creates nice combined message for reactants and product
        if reac[key] > 1:
            reaction_message = reaction_message + str(reac[key]) + makesubs(key) + " "
        else:
            reaction_message = reaction_message + makesubs(key) + " "
    reaction_message = reaction_message + " ----> "
    for key in produc:
        if produc[key] > 1:
            reaction_message = reaction_message + str(produc[key]) + makesubs(key) + " "
        else:
            reaction_message = reaction_message + makesubs(key) + " "
        
    return Page(state, [
        "Equation Solved\n",
        reaction_message,
        Button("Save it for later!", "save"),
        Button("Return home", "index")
        ])
#hard to test because of subscripts

@route
def save(state: State) -> Page:
    """saves the current balanced reaction to state.solved_equation dictionary
    Returns:
        index (Page): index with +1 saved equations
    """
    new_dict = {
        "reactants": state.reac,
        "products": state.produc,
        }
    
    state.solved_equations.append(new_dict)
    return index(state)

@route
def show(state: State) -> Page:
    """shows saved equations from state
    Args:
        state (State): references state.solved_equations
    Returns:
        Page: new page showing all saved balanced reactions
    """
    page_content = []
    for equation in state.solved_equations:
        page_content.append("\n")
        for part in equation["reactants"]:
            if str(equation["reactants"][part]) != "1":
                page_content.append(str(str(equation["reactants"][part]) + makesubs(part)))
            else:
                page_content.append(makesubs(part))
        page_content.append(" ----> ")
        for parts in equation["products"]:
            if str(equation["products"][parts]) != "1":
                page_content.append(str(str(equation["products"][parts]) + makesubs(parts)))
            else:
                page_content.append(makesubs(parts))
    page_content.append("\n\n")
    page_content.append(Button("Return Home", "index"))
    return Page(state, page_content)

#assert_equal(show(state(" ", " ", " ", " ", [], "No errors to display", None, None)))

@route
def table(state: State) -> Page:
    """displays a periodic table image
    Returns:
        Page: periodic table image
    """
    return Page(state, [
        Image("periodic_table.png", width=1200, height=667),
        "\n",
        Link("Image Source", "https://s-ink.org/periodic-table-of-elements"),
        "\n",
        Button("Home", "index"),
        ])


start_server(State("Reactant", "Reactant", "Product", "Product", [], "No errors to display", None, None))
