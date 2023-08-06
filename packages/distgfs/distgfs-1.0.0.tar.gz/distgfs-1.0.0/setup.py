# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['distgfs']
install_requires = \
['distwq>=1.0.3,<2.0.0',
 'dlib>=19.24.0,<20.0.0',
 'h5py>=3.7.0,<4.0.0',
 'mpi4py>=3.1.3,<4.0.0',
 'numpy>=1.23.3,<2.0.0']

setup_kwargs = {
    'name': 'distgfs',
    'version': '1.0.0',
    'description': 'Distributed global function search via dlib',
    'long_description': '# distgfs\n\nDistributed computing framework for the\n[Global Function Search](http://dlib.net/optimization.html#global_function_search) \n(GFS) hyperparameter optimizer from the [Dlib](http://dlib.net) library.\nBased on [gfsopt](https://github.com/tsoernes/gfsopt).\n\nProvides the following features:\n* Parallel optimization: Run distributed hyperparameter searches via [mpi4py](https://github.com/mpi4py/mpi4py).\n* Save and restore progress: Save/restore settings, parameters and optimization progress to/from HDF5 file. \n* Average over multiple runs: Run a stochastic objective function using the same\nparameters multiple times and report the average to Dlib\'s Global Function\nSearch. Useful in highly stochastic domains to avoid biasing the search towards\nlucky runs.\n\nFor theoretical background of GFS, see [\'A Global Optimization Algorithm Worth Using\'](http://blog.dlib.net/2017/12/a-global-optimization-algorithm-worth.html) and [Malherbe & Vayatis 2017: Global optimization of Lipschitz functions](https://arxiv.org/abs/1703.02628)\n\n# Example usage\nA basic example where we maximize Levi\'s function with as many parallel processes as there are logical cores, and save progress to file.\n\n```python\nimport math, distgfs\n\ndef levi(x, y):\n    """\n    Levi\'s function (see https://en.wikipedia.org/wiki/Test_functions_for_optimization).\n    Has a global _minimum_ of 0 at x=1, y=1.\n    """\n    a = math.sin(3. * math.pi * x)**2\n    b = (x - 1)**2 * (1 + math.sin(3. * math.pi * y)**2)\n    c = (y - 1)**2 * (1 + math.sin(2. * math.pi * y)**2)\n    return a + b + c\n\n\ndef obj_fun(pp, pid):\n    """ Objective function to be _maximized_ by GFS. """\n    x = pp[\'x\']\n    y = pp[\'y\']\n\n    res = levi(0.4*x, y)\n    print(f"Iter: {pid}\\t x:{x}, y:{y}, result:{res}")\n    # Since Dlib maximizes, but we want to find the minimum,\n    # we negate the result before passing it to the Dlib optimizer.\n    return -res\n\n# For this example, we pretend that we want to keep \'y\' fixed at 1.0\n# while optimizing \'x\' in the range -4.5 to 4.5\nspace = {\'x\': [-4.5, 4.5]}\nproblem_parameters = {\'y\': 1.}\n    \n# Create an optimizer parameter set\ndistgfs_params = {\'opt_id\': \'distgfs_levi\',\n                  \'obj_fun_name\': \'obj_fun\',\n                  \'obj_fun_module\': \'example_distgfs_levi_file\',\n                  \'problem_parameters\': problem_parameters,\n                  \'space\': space,\n                  \'n_iter\': 10,\n                  \'file_path\': \'distgfs.levi.h5\',\n                  \'save\': True,\n                 }\n\ndistgfs.run(distgfs_params, verbose=True)\n```\n\nFor additional examples, see [examples](https://github.com/iraikov/distgfs/tree/master/examples).\n',
    'author': 'Ivan Raikov',
    'author_email': 'ivan.g.raikov@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'py_modules': modules,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
