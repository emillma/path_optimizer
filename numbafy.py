#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 17:22:08 2019
https://github.com/jankoslavic/numbafy/blob/master/numbafy.py
@author: emil
"""


import sympy as sp
from numba import jitclass


def numbafy(expression, parameters=None, constants=None, use_cse=True, new_function_name='numbafy_func'):
    # cse = sp.cse(expression)

    code_parameters = ''
    code_constants = ''
    code_cse = ''

    if parameters:
        code_parameters = ', '.join(f'{p}' for p in parameters)

    if constants:
        code_constants = []
        for k, v in constants.items():
            code_constants.append(f'{k} = {v}')
        code_constants = '\n    '.join(code_constants)

    if use_cse:
        expressions = sp.cse(expression, optimizations = 'basic')
        code_cse = []
        for e in expressions[0]:
            k, v = e
            code_cse.append(f'{k} = {v}')
        code_cse = '\n    '.join(code_cse)
        code_expression = f'{expressions[1][0]}'
    else:
        code_expression = f'{expression}'


    template = f"""@jit
def {new_function_name}({code_parameters}):
    {code_constants}
    {code_cse}
    return {code_expression}"""

    return template


if __name__ == '__main__':
    import sympy as sym
    from numba import jit

    # this is a very basic example; numbafy shines with huge expression
    a, b, c = sp.symbols('a, b, c')

    constants = {c: 1.4}

    expression = c * a**b
    parameters = (a, b)

    num = numbafy(expression=expression, parameters=parameters, constants=constants, use_cse=True)
    numbafy_func = None
    exec(num)
    result = numbafy_func(a=2.0, b=3.0)
    print(result)