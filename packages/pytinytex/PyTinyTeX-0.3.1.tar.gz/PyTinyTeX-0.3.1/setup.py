# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytinytex']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pytinytex',
    'version': '0.3.1',
    'description': 'Thin wrapper for "TinyTeX" (MIT)',
    'long_description': '# PyTinyTeX\n\n![Build Status](https://github.com/JessicaTegner/PyTinyTeX/actions/workflows/ci.yaml/badge.svg)\n[![PyPI version](https://badge.fury.io/py/pytinytex.svg)](https://pypi.python.org/pypi/PyTinyTeX/)\n[![Development Status](https://img.shields.io/pypi/status/PyTinyTeX.svg)](https://pypi.python.org/pypi/PyTinyTeX/)\n[![Python version](https://img.shields.io/pypi/pyversions/PyTinyTeX.svg)](https://pypi.python.org/pypi/PyTinyTeX/)\n![License](https://img.shields.io/pypi/l/PyTinyTeX.svg)\n\nPyTinyTeX provides a thin wrapper for [TinyTeX](https://yihui.org/tinytex), A lightweight, cross-platform, portable, and easy-to-maintain LaTeX distribution based on TeX Live.\n\n### Installation\n\nInstallation through the normal means\n\n~~~\npip install pytinytex\n~~~\n\nOr through poetry\n\n~~~\npoetry add pytinytex\n~~~\n\n\n### Installing a version of TinyTeX\n\nEach version of TinyTeX contains three variations:\n* TinyTeX-0.* contains the infraonly scheme of TeX Live, without any LaTeX packages. If you install this variation, you may install any other packages via tlmgr (which is a utility included in this variation), e.g., tlmgr install latex-bin framed.\n* TinyTeX-1.* contains about 90 LaTeX packages enough to compile common R Markdown documents (which was the original motivation of the TinyTeX project).\n* TinyTeX-2-* contains more LaTeX packages requested by the community. The list of packages may grow as time goes by, and the size of this variation will grow correspondingly.\n\n\nBy default the variation PyTinyTeX will install is variation 1, but this can be changed.\n\n~~~\nimport pytinytex\n\npytinytex.download_tinytex()\n~~~\n\n\n### Getting the TinyTeX path\n\nAfter installing TinyTeX, you can get PyTinyTeX to pick it up with the following\n\n~~~\nimport pytinytex\n\n# from the current working dir\npytinytex.get_tinytex_path()\n\n# Or from a specific starting base\npytinytex.get_tinytex_path("../../")\n~~~\n\nYou can then use the returned string (which is the path to the installed TinyTeX distributions "bin" directory), with other libraries or programs.\n\n\n### TODO\n\n* Write docs, since this looks to be a bigger wrapper than PyPandoc\n* Wrap the tlmgr interface\n* Wrap the PDFLatex engine\n\n\n### Contributing\n\nContributions are welcome. When opening a PR, please keep the following guidelines in mind:\n\n1. Before implementing, please open an issue for discussion.\n2. Make sure you have tests for the new logic.\n3. Add yourself to contributors at README.md unless you are already there. In that case tweak your \n\n\n### Contributors\n* [Jessica Tegner](https://github.com/JessicaTegner) - Maintainer and original creator of PyTinyTeX\n\n### License\nPyTinyTeX is available under MIT license. See [LICENSE](https://raw.githubusercontent.com/JessicaTegner/PyTinyTeX/master/LICENSE) for more details. TinyTeX itself is available under the GPL-2 license.\n',
    'author': 'JessicaTegner',
    'author_email': 'jessica.tegner@outlook.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/JessicaTegner/PyTinyTeX',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
