# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['tree_sitter_type_provider']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.7,<0.6.0', 'tree-sitter>=0.20.0,<0.21.0']

extras_require = \
{'dev': ['bumpver'],
 'test': ['pytest>=7.1.2,<8.0.0', 'pytest-golden>=0.2.2,<0.3.0']}

setup_kwargs = {
    'name': 'tree-sitter-type-provider',
    'version': '2.1.12',
    'description': 'Type providers for tree-sitter in Python.',
    'long_description': '# Type Providers for Tree Sitter\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/wenkokke/py-tree-sitter-type-provider/CI) ![GitHub tag (latest by date)](https://img.shields.io/github/v/tag/wenkokke/py-tree-sitter-type-provider) ![PyPI](https://img.shields.io/pypi/v/tree-sitter-type-provider)\n\nCreate a type AST from any `node-types.json` file, as well as a generic visitor class and a transformer class, and a function to convert to the AST from the `tree_sitter.Node` type.\n\nFor example, the following code defines a module named `tree_sitter_javascript` from `tree-sitter-javascript/src/nodes.json`:\n\n```python\nimport pathlib\nimport tree_sitter_type_provider as tstp\n\nnode_types_json = pathlib.Path("tree-sitter-javascript/src/node-types.json")\nnode_types = tstp.NodeType.schema().loads(node_types_json.read_text(), many=True)\n\ndef as_class_name(node_type_name: str) -> str:\n    class_name_parts: list[str] = ["Js"]\n    for part in node_type_name.split("_"):\n        class_name_parts.append(part.capitalize())\n    return "".join(class_name_parts)\n\nsys.modules[__name__] = tstp.TreeSitterTypeProvider(\n    "tree_sitter_javascript",\n    node_types,\n    error_as_node=True,          # Include ERROR as a node in the AST\n    as_class_name=as_class_name, # How to convert node types to Python class names\n    extra=["comment"],           # Nodes which are marked as \'extra\' in the grammar\n)\n```\n\nThe module contains a number of dataclasses which represent the AST nodes:\n\n```python\nimport tree_sitter as ts\nimport tree_sitter_type_provider as tstp\n\n@dataclass\nclass JsArray(tstp.Node):\n    text: str\n    type_name: str\n    start_position: tstp.Point\n    end_position: tstp.Point\n    children: list[Union[JsExpression, JsSpreadElement]]\n\n@dataclass\nclass JsDeclaration(tstp.Node):\n    text: str\n    type_name: str\n    start_position: tstp.Point\n    end_position: tstp.Point\n\n@dataclass\nclass JsWhileStatement(tstp.Node):\n    text: str\n    type_name: str\n    start_position: tstp.Point\n    end_position: tstp.Point\n    body: JsStatement\n    condition: JsParenthesizedExpression\n\n...\n```\n\nAs well as a function to convert to the AST:\n\n```python\ndef from_tree_sitter(self, tsvalue: ts.Tree | ts.Node | ts.TreeCursor, *, encoding: str = \'utf-8\') -> tstp.Node\n```\n',
    'author': 'Wen Kokke',
    'author_email': 'wenkokke@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/wenkokke/py-tree-sitter-type-provider',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
