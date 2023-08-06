# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['cq_server']

package_data = \
{'': ['*'],
 'cq_server': ['static/*', 'static/images/*', 'static/vendor/*', 'templates/*']}

install_requires = \
['Flask>=2.2.2,<3.0.0',
 'cadquery-massembly>=0.9.0,<0.10.0',
 'jupyter-cadquery>=3.2.2,<4.0.0',
 'matplotlib>=3.5.3,<4.0.0',
 'minify-html>=0.10.0,<0.11.0']

extras_require = \
{'cadquery': ['cadquery==2.2.0b0', 'casadi==3.5.5']}

entry_points = \
{'console_scripts': ['cq-server = cq_server.cli:main']}

setup_kwargs = {
    'name': 'cadquery-server',
    'version': '0.3',
    'description': 'A web server used to render 3d models from CadQuery code loaded dynamically.',
    'long_description': "# CadQuery Server\n\nA web server used to render 3d models from CadQuery code loaded dynamically.\n\nIt has been created for the [Cadquery VSCode extension](https://open-vsx.org/extension/roipoussiere/cadquery), but can be used as standalone.\n\nExample usage with Kate on the left and Firefox on the right:\n\n![](./images/screenshot.png)\n\n## About CadQuery Server\n\n### Features\n\n- fast response time\n- built-in file-watcher\n- live-reload\n- use your favorite text editor or IDE\n- display model on an external monitor or other device\n- compatible with VSCode built-in browser\n\nPlease note that the web server is intended for personal use and it's absolutely not safe to open it to a public network.\n\n### Functionning\n\nCadQuery Server dynamically loads your CadQuery code and renders the model on the browser using [three-cad-viewer](https://github.com/bernhard-42/three-cad-viewer) (the same used in [jupyter-cadquery](https://github.com/bernhard-42/jupyter-cadquery)). It includes a file watcher that reloads the Python code and updates the web page when the file is updated.\n\nThis approach allows users to work on any IDE, and render the model on any web browser. It also allow them to display the model in an other monitor, or even in an other computer on the same local network (for instance a tablet on your desktop).\n\nThe project was originally started for the VSCode extension, but since it doesn't depend on VSCode anymore, it's now a project as it own.\n\n### About CadQuery\n\nFrom the [CadQuery readme](https://github.com/CadQuery/cadquery/blob/master/README.md):\n\n> CadQuery is an intuitive, easy-to-use Python module for building parametric 3D CAD models. Using CadQuery, you can write short, simple scripts that produce high quality CAD models. It is easy to make many different objects using a single script that can be customized.\n\nRead [CadQuery documentation](https://cadquery.readthedocs.io/en/latest/) for more information about CadQuery and its usage.\n\n## Installation\n\n### Create a virtual environment (recommended)\n\n    python -m venv .venv\n    source .venv/bin/activate\n\n### Upgrade pip and setuptools\n\n    pip install --upgrade pip setuptools\n\n### Install with pip\n\nIf you already have CadQuery installed on your system:\n\n    pip install cadquery-server\n\nIf you want to install both cq-server and CadQuery:\n\n    pip install 'cadquery-server[cadquery]'\n\n### Install with Docker\n\n    docker pull cadquery/cadquery-server\n\nThen add a volume and port when running the container. Typically:\n\n    docker run -p 5000:5000 -v $(pwd)/examples:/data cadquery/cadquery-server\n\nWhere `examples` is in your current directory and contains CadQuery scripts.\n\n### Install from sources\n\n    git clone https://github.com/roipoussiere/cadquery-server.git\n    cd cadquery-server\n\nIf you already have CadQuery installed on your system:\n\n    pip install .\n\nIf you want to install both cq-server and CadQuery:\n\n    pip install '.[cadquery]'\n\n## Usage\n\n### Starting the server\n\nOnce installed, the `cq-server` command should be available on your system.\n\nIt takes only one optional argument: the target, which can be a folder or a file. Defaults to the current directory (`.`).\n\nThen the root endpoint (ie. `http://127.0.0.1`) will display:\n- if `target` is a folder: an index page from which you can select a file to render;\n- if `target` is a file: the root endpoint will render the corresponding file.\n\nServer options:\n\n- `-p`, `--port`: Server port (default: 5000);\n\nExample:\n\n    cq-server -p 8080 ./examples/box.py\n\nThis command will run the server on the port `8080`, then load and render `./examples/box.py`. The file to load can be overridden by url parameter if necessary (see below).\n\nUse `cq-server -h` to list all available options.\n\n### Exporting static html\n\nYou can use `-e` / `--export` cli option to obtain an html file that work as a standalone and doesn't require a running server.\n\n### UI cli options\n\nOther cli options are available to change the UI appearence:\n\n- `--ui-hide`: a comma-separated list of buttons to disable, among: `axes`, `axes0`, `grid`, `ortho`, `more`, `help`;\n- `--ui-glass`: activate tree view glass mode;\n- `--ui-theme`: set ui theme, `light` or `dark` (default: browser config);\n- `--ui-trackball`: set control mode to trackball instead orbit;\n- `--ui-perspective`: set camera view to perspective instead orthogonal;\n- `--ui-grid`: display a grid in specified axes (`x`, `y`, `z`, `xy`, etc.);\n- `--ui-transparent`: make objects semi-transparent;\n- `--ui-black-edges`: make edges black.\n\nExample:\n\n    cq-server --ui-hide ortho,more,help --ui-glass --ui-theme light --ui-grid xyz\n\n### Writing a CadQuery code\n\nCadQuery Server renders the model defined in the `show_object()` function (like in CadQuery Editor).\n\nYou **must** import it before from the `cq_server.ui` module, among with the `UI` class, which is used by the server to load the model.\n\nMinimal working example:\n\n```py\nimport cadquery as cq\nfrom cq_server.ui import UI, show_object\n\nshow_object(cq.Workplane('XY').box(1, 2, 3))\n```\n\nPlease read the [CadQuery documentation](https://cadquery.readthedocs.io/en/latest/) for more details about the CadQuery library.\n\n### Using with the web server\n\nOnce the server is started, go to its url (ie. `http://127.0.0.1`).\n\nOptional url parameters:\n\n- `m`: name of an other module to load;\n\nexample: `http://127.0.0.1?m=box`).\n\nOther endpoints:\n\n- `/json?m=box`: returns the model as a threejs json object. Used internally to retrieve the model.\n- `/html?m=box`: returns a static html page that doesn't require the CadQuery Server running.\n\n### Using with VSCode\n\nThe web page can be displayed within VSCode IDE using [LivePreview extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode.live-server):\n\n1. install the LivePreview VSCode extension;\n2. `ctrl+shift+P` -> *Simple Browser: Show*;\n3. update the url according to your running CadQuery server instance (ie. `127.0.0.1:5000`).\n\n## About\n\n- contact:\n    - ping user `@roipoussiere` on channel `other-gui` in the CadQuery Discord;\n    - [Mastodon](https://mastodon.tetaneutral.net/@roipoussiere);\n- license: [MIT](./LICENSE);\n- source: both on [Framagit](https://framagit.org/roipoussiere/cadquery-server) (Gitlab instance) and [Github](https://github.com/roipoussiere/cadquery-server);\n- issue tracker: both on [Framagit](https://framagit.org/roipoussiere/cadquery-server/-/issues) and [Github](https://github.com/roipoussiere/cadquery-server/issues)\n",
    'author': 'Roipoussiere',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://open-vsx.org/extension/roipoussiere/cadquery',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<3.11',
}


setup(**setup_kwargs)
