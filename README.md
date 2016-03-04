# PyLUAc
Python to LUA transpiler

[![Build Status](https://travis-ci.org/grigi/PyLUAc.svg?branch=master)](https://travis-ci.org/grigi/PyLUAc)
[![Coverage Status](https://coveralls.io/repos/github/grigi/PyLUAc/badge.svg?branch=master)](https://coveralls.io/github/grigi/PyLUAc?branch=master)


## Plans for this project
LUA is a great VM, it embeds nicely and securely, is easy to integrate. Just... that syntax.
So this is a project where I experiment using a Python-like syntax that compiles to LUA bytecode.

### To get there we propose a few stages:

1. Build a basic parser that can build LUA functions
2. Extend the parser to handle Classes (using metatables)
3. Ensure that all the used functionality of metatables is supported (e.g. operator overloading, default getters, etc...)
4. Extend the parser to generate generators (if possible in LUA)
5. Extend the parser to generate co-routines (make it clean using async and await statements)

Once/If we get there, and the parser works reliably for many edge cases, introduce this to the LUA community and start a project to port this to C, so that it can be embedded just like LUA/LUAjit.

### Why did we not use the python AST parser, and then just work from there?

Python is such a dynamic language, that many of the nuances just won't translate to LUA. We considered this, but decided that there will need to be subtle differences in operation and introspection, so the language technically won't be Python, but a heavily Python-inspired LUA implementation.
