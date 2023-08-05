"""
Treer
===

Ascii Tree Tool for Python!

Powered by [Yamato Nagata](https://twitter.com/514YJ)

[GitHub](https://github.com/nagataaaas/Treer)

```python
from treer import Tree

root = Tree.from_path("tests")
root.colorize = False
print(root.draw())
# tests
#  ├── test.py
#  └── test_dir
#       ├── dir1
#       │    ├── dir1-1
#       │    │    └── dir1-1-1
#       │    ├── dir1-2
#       │    └── *dir1-3
#       ├── dir1-1
#       └── dir2
#            ├── dir2-1
#            └── dir2-2

root = Tree.from_mapping({
            'root': {
                'dir1': {
                    'file1': None,
                    'file2': None,
                    'dir1-2': {
                        'file3': None,
                    },
                },
                'dir3': [
                    'file4',
                    'file5',
                ],
                'dir4': 'file6'
            }
        })
root.colorize = False
print(root.draw())
# root
#  ├── dir1
#  │    ├── file1
#  │    ├── file2
#  │    └── dir1-2
#  │         └── file3
#  ├── dir3
#  │    ├── file4
#  │    └── file5
#  └── dir4
#       └── file6
```

**colored example**

![output](https://github.com/nagataaaas/Treer/blob/main/assets/capture1.png?raw=true)

# Installation

    $ pip install treer

"""

from setuptools import setup
from os import path

about = {}
with open("treer/__about__.py") as f:
    exec(f.read(), about)

here = path.abspath(path.dirname(__file__))

setup(name=about["__title__"],
      version=about["__version__"],
      url=about["__url__"],
      license=about["__license__"],
      author=about["__author__"],
      author_email=about["__author_email__"],
      description=about["__description__"],
      long_description=__doc__,
      long_description_content_type="text/markdown",
      install_requires=["iro==0.8.1"],
      packages=["treer"],
      zip_safe=True,
      platforms="any",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Other Environment",
          "Intended Audience :: Developers",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
          "Programming Language :: Python :: 3",
          "Programming Language :: Python",
          "Topic :: Software Development :: Libraries :: Python Modules",
          "Environment :: Console"
      ])
