# numcertainties

This project aims to unify the use of several error propagation libraries in python:

- <https://github.com/HDembinski/jacobi>
- <https://github.com/lebigot/uncertainties/>
- <https://github.com/tisimst/mcerp>
- (<https://github.com/tisimst/soerp>)

In future general differentiation routines could be used to get the jacobian similar to the `jacobi` package to get uncertainties from there:

- <https://pypi.org/project/numdifftools/>
- scipy
- (sympy for analytic derivatives i.e. as we store the operations we can do an anlytic derivative?, though eg. exp will be difficult)

TODO:
- p values / confidence
- handle mixed types of uncertainties
