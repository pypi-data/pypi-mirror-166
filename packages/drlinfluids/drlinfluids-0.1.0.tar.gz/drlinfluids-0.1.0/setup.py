# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['drlinfluids',
 'drlinfluids.environments',
 'drlinfluids.resources',
 'drlinfluids.trainer']

package_data = \
{'': ['*']}

install_requires = \
['PeakUtils>=1.3.3',
 'numpy>=1.18.5',
 'pandas>=1.3.3',
 'scipy>=1.4.1',
 'sympy>=1.10.1',
 'tensorforce==0.6.0']

setup_kwargs = {
    'name': 'drlinfluids',
    'version': '0.1.0',
    'description': 'A flexible platform to utilize Deep Reinforcement Learning in the field of Computational Fluid Dynamics.',
    'long_description': '# DRLinFluids\n[![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)](https://github.com/venturi123/DRLinFluids/blob/main/LICENSE)\n\nDRLinFluids is a flexible and scalable package to utilize Deep Reinforcement Learning in the field of Computational Fluid Dynamics (CFD).\n\nNote: This package is still in development. The API is not stable yet. We invite all users to discuss further and ask for help directly on GitHub, through the issue system, and we commit to helping develop a community around the DRLinFluids framework by providing in-depth documentation and help to new users.\n\nThe package is developed under Ubuntu 20.04 LTS and OpenFOAM 8.\n\n\n## Table of contents\n\n- [Introduction](#introduction)\n- [Installation](#installation)\n- [How to cite](#how-to-cite)\n- [Core development team and contributors](#core-development-team-and-contributors)\n- [Contributing](#contributing)\n- [License](#license)\n\n\n## Introduction\n\nReinforcement learning is a field of machine learning. It studies by interacting with the environment. It emphasizes how to make corresponding behavior in a specific environment in order to maximize the expected benefits. However, for reinforcement learning, it is necessary to define a specific interaction environment for specific problems, which is rather cumbersome and takes up a lot of time of researchers in related fields, and delays the research speed of researchers in reinforcement learning and fluid cross field. For this purpose, a reinforcement learning platform based on open source computational fluid dynamics software OpenFOAM is proposed, which is DRLinFluids. The platform has the characteristics of automation, quickness and simplicity, and can quickly call reinforcement learning for different research problems.\n\nDifferent from TensorFlow, PyTorch and other general machine learning frameworks, this platform takes OpenFOAM as an interactive environment, and further develops **a general CFD reinforcement learning package**.\n\n[OpenFOAM](https://en.wikipedia.org/wiki/OpenFOAM) (for "Open-source Field Operation And Manipulation") is a C++ toolbox for the development of customized numerical solvers, and pre-/post-processing utilities for the solution of continuum mechanics problems, most prominently including computational fluid dynamics (CFD). In fact, due to the versatility of OpenFOAM, in addition to computational fluid dynamics problems, it can also deal with any ODE or PDE problems. Users can create their own solver for practical application by setting the control equations and boundary conditions of specific problems. This also gives DRLinFluids a wider usage.\n\n\n## Installation\n\n### From PyPI\n\n```bash\npip install drlinfluids\n```\n\n### From Source code\n\n```\ngit clone https://github.com/venturi123/DRLinFluids.git\npip3 install -e drlinfluids\n```\n\n\n## Examples\n\nPlease see `/examples` directory for quick start.\n\n\n## How to cite\n\nPlease cite the framework as follows if you use it in your publications:\n\n```\nQiulei Wang (王秋垒), Lei Yan (严雷), Gang Hu (胡钢), Chao Li (李朝), Yiqing Xiao (肖仪清), Hao Xiong (熊昊), Jean Rabault, and Bernd R. Noack , "DRLinFluids: An open-source Python platform of coupling deep reinforcement learning and OpenFOAM", Physics of Fluids 34, 081801 (2022) https://doi.org/10.1063/5.0103113\n```\n\nFor more formats, please see https://aip.scitation.org/action/showCitFormats?type=show&doi=10.1063%2F5.0103113.\n\n\n## Core development team and contributors\n\nDRLinFluids is currently developed and maintained by \n\n[AIWE Lab, HITSZ](http://aiwe.hitsz.edu.cn)\n\n- [Qiulei Wang](https://github.com/venturi123)\n\n- [Lei Yan](https://github.com/1900360)\n\n- [Gang Hu](http://faculty.hitsz.edu.cn/hugang)\n\n[Jean Rabault](https://github.com/jerabaul29)\n\n[Bernd Noack](http://www.berndnoack.com/)\n\n\n## Contributing\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\nWe invite all users to further discuss and ask for help directly on Github, through the issue system, and we commit to helping develop a community around the DRLinFluids framework by providing in-depth documentation and help to new users.\n\n\n## License\n`DRLinFluids` is licensed under the terms of the Apache License 2.0 license.\n',
    'author': 'Qiulei Wang et al.',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
