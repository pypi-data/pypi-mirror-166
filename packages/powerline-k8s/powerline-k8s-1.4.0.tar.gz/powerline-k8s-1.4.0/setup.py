# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['powerline_k8s']

package_data = \
{'': ['*']}

install_requires = \
['kubernetes>=24.2.0,<25.0.0', 'powerline-status>=2.7,<3.0']

setup_kwargs = {
    'name': 'powerline-k8s',
    'version': '1.4.0',
    'description': 'A custom Powerline segment for displaying the current Kubernetes context and namespace',
    'long_description': '# powerline-k8s\n\n[![PyPI](https://img.shields.io/pypi/v/powerline-k8s)](https://pypi.org/project/powerline-k8s/)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/powerline-k8s)\n[![codecov](https://codecov.io/gh/j4ckofalltrades/powerline-k8s/branch/main/graph/badge.svg?token=J5GLE5ZY2V)](https://codecov.io/gh/j4ckofalltrades/powerline-k8s)\n\nA custom [Powerline](https://github.com/powerline/powerline) segment for displaying the current Kubernetes context and namespace.\n\n![](https://res.cloudinary.com/j4ckofalltrades/image/upload/v1623588713/foss/powerline-k8s_uc0cxj.png)\n\n## Installation\n\n### Using pip\n\n`$ pip install powerline-k8s`\n\n## Configuration\n\n### Colorscheme\n\nAdd the following config items to your Powerline colorscheme config file (usually located at `~/.config/powerline/colorschemes/`),\nsee [Powerline Colorschemes](https://powerline.readthedocs.io/en/master/configuration/reference.html#colorschemes) for more info.\n\n```json\n{\n  "k8s":           { "fg": "solarized:blue", "bg": "solarized:base02", "attrs": [] },\n  "k8s_namespace": { "fg": "solarized:red",  "bg": "solarized:base02", "attrs": [] },\n  "k8s_context":   { "fg": "solarized:blue", "bg": "solarized:base02", "attrs": [] },\n  "k8s:divider":   { "fg": "gray4",          "bg": "solarized:base02", "attrs": [] }\n}\n```\n\n### Segment\n\nAdd the following config item to your Powerline segments config file,\nsee [Powerline Segment reference](https://powerline.readthedocs.io/en/master/configuration/segments.html#segment-reference) for more info.\n\n```json\n{\n  "function": "powerline_k8s.k8s",\n  "priority": 30\n}\n```\n\n- If adding the segment to the shell, edit `~/.config/powerline/themes/shell/default.json`.\n- If adding the segment to the tmux status line, edit `~/.config/powerline/themes/tmux/default.json`.\n\n### Toggle visibility\n\nToggle entire segment or specific section\'s visibility with the following environment variables:\n\n- `POWERLINE_K8S_SHOW`\n- `POWERLINE_K8S_SHOW_NS`\n\nNote: Full segment visibility takes precedence over namespace section visibility.\n\n```shell\n# toggle segment visibility\n$ POWERLINE_K8S_SHOW=0 powerline-daemon --replace # hide powerline-k8s segment\n$ POWERLINE_K8S_SHOW=1 powerline-daemon --replace # show powerline-k8s segment (default)\n\n# toggle namespace section visibility\n$ POWERLINE_K8S_SHOW_NS=0 powerline-daemon --replace # hide namespace section\n$ POWERLINE_K8S_SHOW_NS=1 powerline-daemon --replace # show namespace section (default)\n```\n\nAlternatively you can add the following function to your shell for easier toggling:\n\n```shell\ntoggle_powerline_k8s() {\n  case "$1" in\n    # pass the \'-ns\' flag to toggle namespace visibility\n    "-ns" | "--namespace")\n      if [[ "${POWERLINE_K8S_SHOW_NS:-1}" -eq 1 ]]; then\n        export POWERLINE_K8S_SHOW_NS=0\n      else\n        export POWERLINE_K8S_SHOW_NS=1\n      fi\n    ;;\n    *)\n      # toggle segment visibility\n      if [[ "${POWERLINE_K8S_SHOW:-1}" -eq 1 ]]; then\n        export POWERLINE_K8S_SHOW=0\n      else\n        export POWERLINE_K8S_SHOW=1\n      fi\n    ;;\n  esac\n}\n```\n\n## Docs\n\nFor more detailed documentation see [https://j4ckofalltrades.github.io/powerline-k8s](https://j4ckofalltrades.github.io/powerline-k8s)\n\n## Demo\n\n[![asciicast](https://asciinema.org/a/424536.svg)](https://asciinema.org/a/424536?autoplay=1&speed=2)\n\n\n## Stats\n\n![Alt](https://repobeats.axiom.co/api/embed/fbba579306e9c836bd6aa443e43637a0131c45f3.svg "Repobeats analytics image")\n',
    'author': 'Jordan Duabe',
    'author_email': 'me@jduabe.dev',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
