from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, \
     Number, Literal, Operator, Generic, Whitespace

# Many examples are here https://bitbucket.org/birkenfeld/pygments-main/src/default/pygments/styles/default.py

class PineStyle(Style):
    background_color = "#f8f8f8"
    default_style = ""

    styles = {
        Whitespace:                "#bbbbbb",
        Comment:                   "italic #408080",

        Keyword:                   "bold #008000",

        Operator:                  "#666666",

        Literal:                   "#ff00ff", # Color literal
        Name:                      "#101010",
        Name.Constant:             "bold #800000", # Built-in series 'open', 'high', ...
        Name.Entity:               "bold #008000", # Annotation function

        String:                    "#BA2121",
        Number:                    "#6666FF",

        Error:                     "border:#FF0000"
    }
