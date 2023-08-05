# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gp_libs']

package_data = \
{'': ['*']}

entry_points = \
{'pytest11': ['sphinx = pytest_sphinx']}

setup_kwargs = {
    'name': 'gp-libs',
    'version': '0.0.1a1',
    'description': 'Internal utilities for projects following git-pull python package spec',
    'long_description': "# gp-libs &middot; [![Python Package](https://img.shields.io/pypi/v/gp-libs.svg)](https://pypi.org/project/gp-libs/) [![License](https://img.shields.io/github/license/git-pull/gp-libs.svg)](https://github.com/git-pull/gp-libs/blob/master/LICENSE) [![Code Coverage](https://codecov.io/gh/git-pull/gp-libs/branch/master/graph/badge.svg)](https://codecov.io/gh/git-pull/gp-libs)\n\nYou probably don't need these. These are internal helpers that are getting\n[dogfooded](https://en.wikipedia.org/wiki/Eating_your_own_dog_food) on projects\nfollowing git-pull's python package patterns, e.g. any python packages in\n[cihai](https://github.com/cihai), [vcs-python](https://github.com/vcs-python), or\n[tmux-python](https://github.com/tmux-python). They're unstable (APIs can change\nwithout warning). When stabilized they can be broken off into separate packages,\nmerged upstream, etc.\n\n## doctest helpers (for docutils)\n\nTwo parts:\n\n1. doctest module: Same specification as doctest, but can parse reStructuredText\n   and markdown\n2. pytest plugin: Collects pytest for reStructuredText and markdown files\n\n### doctest module\n\n...\n\nThis extends standard library `doctest` to support anything docutils can parse.\nIt can parse reStructuredText (.rst) and markdown (.md).\n\nIt supports two barebones directives:\n\n- docutils' `doctest_block`\n\n  ```rst\n  >>> 2 + 2\n  4\n  ```\n\n- `.. doctest::` directive\n\n  reStructuredText:\n\n  ```rst\n  .. doctest::\n\n     >>> 2 + 2\n     4\n  ```\n\n  Markdown (requires [myst-parser]):\n\n  ````markdown\n  ```{doctest}\n  >>> 2 + 2\n  4\n  ```\n  ````\n\n[myst-parser]: https://myst-parser.readthedocs.io/en/latest/\n\n### pytest plugin\n\n...\n\nThis plugin integrates with the above module.\n\n```console\n$ pytest docs/\n```\n\nLike the above module, it supports docutils' own `doctest_block` and a basic\n`.. doctest::` directive.\n\n## sphinx plugins\n\n### Plain-text issue linker\n\nWe need to parse plain text, e.g. #99999, to point to the project tracker at\nhttps://github.com/git-pull/gp-libs/issues/99999. This way the markdown looks\ngood anywhere you render it, including GitHub and GitLab.\n\n### Table of contents for autodoc\n\n`sphinx.ext.autodoc` doesn't link objects in the table of contents. So we need a\nplugin to help.\n\n## Install\n\n```console\n$ pip install --user gp-libs\n```\n\n### Developmental releases\n\nYou can test the unpublished version of g before its released.\n\n- [pip](https://pip.pypa.io/en/stable/):\n\n  ```console\n  $ pip install --user --upgrade --pre gp-libs\n  ```\n\n# More information\n\n- Python support: >= 3.7, pypy\n- Source: <https://github.com/git-pull/gp-libs>\n- Docs: <https://gp-libs.git-pull.com>\n- Changelog: <https://gp-libs.git-pull.com/history.html>\n- API: <https://gp-libs.git-pull.com/api.html>\n- Issues: <https://github.com/git-pull/gp-libs/issues>\n- Test Coverage: <https://codecov.io/gh/git-pull/gp-libs>\n- pypi: <https://pypi.python.org/pypi/gp-libs>\n- License: [MIT](https://opensource.org/licenses/MIT).\n\n[![Docs](https://github.com/git-pull/gp-libs/workflows/docs/badge.svg)](https://gp-libs.git-pull.com)\n[![Build Status](https://github.com/git-pull/gp-libs/workflows/tests/badge.svg)](https://github.com/git-pull/gp-libs/actions?query=workflow%3A%22tests%22)\n",
    'author': 'Tony Narlock',
    'author_email': 'tony@git-pull.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gp-libs.git-pull.com',
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
