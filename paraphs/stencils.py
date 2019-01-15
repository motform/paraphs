"""
4ME501 - Programming for Digital Humanities - 2019
Assignment 6: Final Project
Author: Love Lagerkvist (ll223jp)
Python version: 3.7

Stencils - pre-defined shapes used to draw cairo graphics.

There are two main types of stencils:
    Floating - Stencils that float in the surface
    Central  - Stencils that grow from the center coordinate.

Stencils are either drawn filled our outlined. This is
controlled by decorators on a per-stencil basis.

The Cairo surface is normalized, which means that any
instructions have to be in the [0:1] decimal range.
"""

# import parser
from paraphs import helpers

import math
from random import Random
from functools import wraps


def handler(context, word, tag):
    """Handles all the stencil definitions, keeps our code DRY.

    Once the appropriate turn of action is found in the dict,
    a stencil function is called as an inner function."""

    float_word = helpers.str_to_float(word)
    random = Random(float_word)  # Deterministic randomnes

    # Decorators

    def fill(func):
        """Decorator - renders stencil filled."""
        @wraps(func)
        def wrapped():
            func()
            context.fill()
        return wrapped

    def stroke(func):
        """Decorator - renders stencil as an outline (stroke only)."""
        @wraps(func)
        def wrapped():
            func()
            context.stroke()
        return wrapped

    # Stencils

    @fill
    def floating_row_rectangles():
        """Floting rect tba"""
        iterations = int(str(float_word)[2])
        x1, x2 = float_word, float_word

        for i in range(1, iterations + 1):
            context.rectangle(x1, x2, 0.01, 0.03)  # x1 y1 x2 y2
            x1 += 0.03

    def floating_triangle():
        """Floating Triangle tba"""
        pass

    @fill
    def floating_circle():
        """Floating Circle tba."""
        context.new_sub_path()
        context.arc(random.uniform(0, 1), random.uniform(0, 1),
                    float_word / 50,                                # radius
                    0, 2 * math.pi)                                 # angle (start, end)

    @stroke
    def central_line():
        """Draw central_line from center and out."""
        context.move_to(0.5, 0.5)
        context.line_to(float_word, random.uniform(0, 1))           # x2, y2

    @stroke
    def central_arc():
        """Draws and central_arc based on the hashing of word."""
        context.arc(0.5, 0.5,                                       # position
                    float_word / 2,                                 # radius
                    random.uniform(0, 1), random.uniform(0, 1))   # angle (start, end)

    def adj():
        """Handles adjectives and adverbs. When these tags are found
        we use the sentiment subjectivity to set the central_line weight,
        importance, of the next drawable word."""
        pass
        # adj_sentiment = parser.generate_sentiment(word, type_of_sentiment=subjectivity)
        # context.set_line_width(adj_sentiment)

    tag_index = {
        # Adjectives
        'JJ':  adj, 'JJR': floating_row_rectangles, 'JJS': floating_row_rectangles,
        # Adverbs
        'RB':  adj, 'RBR': adj, 'RBS': floating_row_rectangles,
        # Nouns
        'NN':  central_line, 'NNS':  floating_circle,
        'NNP': floating_row_rectangles,  'NNPS': floating_row_rectangles,
        # Pronoun
        'PRP': floating_circle, 'PRP$': None,
        # Verbs
        'VB':  None, 'VBD': None, 'VBG': None,
        'VBN': None, 'VBP': None, 'VBZ': None,
        # Stop-tags -> Tags we skip in the visualization
        'WDT': None, 'WP':  None, 'WP$': None, 'WRB': None,
        'SYM': None, 'TO':  None, 'UH':  None, 'RP':  None,
        'LS':  None, 'MD':  None, 'CC':  None, 'CD':  None,
        'DT':  None, 'EX':  None, 'FW':  None, 'IN':  None,
        'PDT': None, 'POS': None,
    }

    if tag_index[tag]:
        tag_index[tag]()  # Runs our inner function or returns False

