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
