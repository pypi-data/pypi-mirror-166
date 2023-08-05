# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['git_darcs']
install_requires = \
['Flake8-pyproject>=1.1.0.post0,<2.0.0',
 'click>=8.1.3,<9.0.0',
 'tqdm>=4.64.0,<5.0.0']

entry_points = \
{'console_scripts': ['git-darcs = git_darcs:main']}

setup_kwargs = {
    'name': 'git-darcs',
    'version': '0.5.0',
    'description': 'Incremental import of git into darcs',
    'long_description': 'git-darcs - Incremental import of git into darcs\n================================================\n\n[![Test](https://github.com/ganwell/git-darcs/actions/workflows/test.yml/badge.svg)](https://github.com/ganwell/git-darcs/actions/workflows/test.yml) [![CodeQL](https://github.com/ganwell/git-darcs/actions/workflows/codeql-analysis.yml/badge.svg)](https://github.com/ganwell/git-darcs/actions/workflows/codeql-analysis.yml)\n\n[git-darcs on pypi](https://pypi.org/project/git-darcs/)\n\nJust call `git-darcs update`, it will import the current git-commit into darcs.\nIf you get new commits eg. using `git pull`, you can call `git-darcs update` and\nit will import each commit into darcs.\n\nBy default the first import is shallow, only importing the current git-commit.\nIf you want to import the whole history use `git-darcs update --no-shallow`,\nsince we **linearize** the history by checking out each commit this can take\nvery long.\n\nOn the first import you can also supply a custom base-commit `git-darcs update\n--base fa2b982` ignoring history you are not interested in.\n\nThe options `base` and `shallow` are ignored after the first import.\n\nUse a global `gitignore` to ignore `_darcs` in all your depositories.\n\nWith `git-darcs clone <source> <destination>` you can clone a darcs/git dual\nrepository locally. Both git and darcs will make sure no history-data is\nduplicated on disk.\n\nThe tool is intentionally very minimal, it is for devs. They can read tracebacks\nor change the code to fit better. To create git patches from my\nworking-repositories I use `darcs rebase suspend` and `git commit -a -v`.\n\nBut why\n-------\n\nI prefer to group changes by topic, so I am constantly amending patches. This is\nvery easy in darcs and more complicated in git. Yes, I know about `--fixup` and\n`--autosquash` in git. Also I can find independent low-risk patches easily with\n`darcs show dependencies`, so I can constantly make PRs. Making the final\n_breaking_ change/PR much smaller. This is less tedious for the reviewers.\n\nFor darcs beginners\n-------------------\n\n* There is a great [video](https://hikari.acmelabs.space/videos/hikari-darcs.mp4) by\n  [raichoo](https://hub.darcs.net/raichoo) the maintainer of\n  [hikari](https://hikari.acmelabs.space/)\n* You have to read the [darcs book](https://darcsbook.acmelabs.space/), you just\n  have to\n* `_darcs/pref/boring` is the equivalent of `.gitignore`, but has quite a wide\n  definition of boring by default\n\nDarcs does not handle `chmod` or symbolic-links. The easiest way to workaround\nthis, is letting `git` do the work. I have two git/darcs repositories for each\nproject.\n\n* `project` (the repository I work in) containing a `.git` and a `_darcs`\n* `project-tracking` (the repository that tracks changes from upstrream,\n   also containing a `.git` and a `_darcs`\n\nI then pull new darcs-patches from `project-tracking` into `project`. Once my\nthe changes are in upstream, I obliterate everything to the checkpoint (tag) I\nstarted with and pull the patches (now via `git`) from `project-tracking`. Or I\nremove `project` and clone it again from `project-tracking`.\n\nSince I always make git-commits from the darcs-patches `git` will track `chmod`\nand symbolic-links for me.\n\nUsage\n-----\n\n<a href="https://asciinema.org/a/518694" target="_blank"><img\nsrc="https://asciinema.org/a/518694.svg" /></a>\n\nNote: this asciinema was made before `shallow` was default.\n\n```\n$> git-darcs --help\nUsage: git-darcs [OPTIONS] COMMAND [ARGS]...\n\n  Click entrypoint.\n\nOptions:\n  --help  Show this message and exit.\n\nCommands:\n  clone   Locally clone a tracking repository to get a working-repository.\n  update  Incremental import of git into darcs.\n```\n\n```\n$> git-darcs update --help\nUsage: git-darcs update [OPTIONS]\n\n  Incremental import of git into darcs.\n\n  By default it imports a shallow copy (the current commit). Use `--no-\n  shallow` to import the complete history.\n\nOptions:\n  -v, --verbose / -nv, --no-verbose\n  -w, --warn / -nw, --no-warn     Warn that repository will be cleaned\n  -b, --base TEXT                 On first update import from (commit-ish)\n  -s, --shallow / -ns, --no-shallow\n                                  On first update only import current commit\n  --help                          Show this message and exit.\n```\n\n```\n$> git-darcs clone --help\nUsage: git-darcs clone [OPTIONS] SOURCE DESTINATION\n\n  Locally clone a tracking repository to get a working-repository.\n\nOptions:\n  -v, --verbose / -nv, --no-verbose\n  --help                          Show this message and exit.\n```\n\nLinearized history\n------------------\n\nCurrently we traverse the repository with this secret sauce:\n\n```bash\ngit rev-list\n    --reverse\n    --topo-order\n    --ancestry-path\n```\n\nIt can lead to quite confusing results. There is no way for a perfect result,\nbut I am still experimenting.\n',
    'author': 'Jean-Louis Fuchs',
    'author_email': 'jean-louis.fuchs@adfinis.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/ganwell/git-darcs',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
