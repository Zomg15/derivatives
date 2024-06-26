from tokenizer import Tokenizer
from parser.parser import Parser
from find_derivative import FindDerivative
from parser.Tree import Tree

from tkinter import *
from tkinter import ttk

output = None
rules_shown = False
rules_string = """Tehtesümbolid on +, -, *, /, ^ ja sulud. Mingit muud sümbolit kasutada ei tohi. 
Korrutamisel tuleb alati kasutada märki *, välja arvatud siis, kui tegemist on muutuja korrutisega.
Üksliikme kirjutamisel tuleb kordaja ning aste kirjutada vahetult enne ja pärast muutujat. Näiteks 3*x^2 peab kirjutama nagu 3x2.
Programm järgib rangelt tehete järjekorda.
Eksponentsiaalfunktsioon tuleb kirjutada kui e^x. exp(x) ei ole õige.
Numbrite komakoht tuleb kirjutada punkti, mitte komaga.
Ruutjuure jaoks võib kasutada funktsiooni sqrt(). Muude murdarvuliste astmete puhul tuleb sisestada aste ning arv ise.
Logaritmide puhul on saadaval funktsioonid ln() ja log(). Muude aluste jaoks peab kasutama aluse vahetuse reeglit, et avaldada logaritm kas ln() või log() suhtes.
"""

font_style = ("Segoe UI", 20)

def calc():
    print(f"INPUT: {func.get()}")
    tokeniser = Tokenizer()

    tokeniser.run(func.get())

    result = tokeniser.result

    parser = Parser()

    tree_form = parser.begin_parse(result)
    print(tree_form)

    derivative_finder = FindDerivative()
    derivative = derivative_finder.derive(tree_form)

    if type(derivative) == Tree:
        derivative = derivative.clean(derivative)

    output.set(derivative.__repr__())
    func.set("")

def toggle_rules():
    global rules_shown # don't question it
    if not rules_shown:
        rules.config(text=rules_string)
        rules_button.config(text="Peida reeglid")
        rules_shown = True
    else:
        rules.config(text="")
        rules_button.config(text="Kuva reeglid")
        rules_shown = False

main_frame = Tk()
main_frame.title("Tuletiste leidja")

ttk.Label(main_frame, text="Funktsioon:", font=font_style).grid(column=1, row=1, sticky=W)

func = StringVar()
func_textbox = ttk.Entry(main_frame, width=30, textvariable=func, font=font_style)
func_textbox.grid(column=2, row=1, sticky=E)

rules_button = Button(main_frame, text="Kuva reeglid", command=toggle_rules, font=font_style)
rules_button.grid(column=1, row=2, sticky=W)
Button(main_frame, text="Arvuta", command=calc, font=font_style).grid(column=2, row=2, sticky=E)

rules = ttk.Label(main_frame, text="", font=("Segoe UI", 10))
rules.grid(column=1, row=3, sticky=W)

output = StringVar()
ttk.Label(main_frame, text="Tulemus:", font=font_style).grid(column=1, row=4, sticky=W)
output_label = ttk.Label(main_frame, textvariable=output, font=font_style)
output_label.grid(column=2, row=4, sticky=E)

for child in main_frame.winfo_children():
    child.grid_configure(padx=10, pady=10)

main_frame.mainloop()