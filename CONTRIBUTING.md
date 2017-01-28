# Contributing

In the following sections, the conventions and setup required for contributing to the NEAT project are outlined.


---

## Conventions

Below are standards set for the NEAT project to ensure ease, consistency, maintainability, and robustness for future development teams.
Changes made to these standards are purely to the desire of the current development team.
But note, that change for the sake of change is akin to failure.


### Versioning

The NEAT project strictly follows [Semantic Versioning 2.0.0](http://semver.org/) as proposed by [Tom Preston-Werner](http://tom.preston-werner.com/).
The in-house development period is to follow the 0.x.x standard until the initial release of a full scale product (at which time will change to its first major release).


### Coding Conventions

NEAT source follows the [PEP8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/).
The only exception to this style guide is the rule on [line length](https://www.python.org/dev/peps/pep-0008/#maximum-line-length).
This rule has been omitted simply because of its occasional annoyance.
Code written in in this project should still try to adhere to the 79 character limit while documentation should stay under the 72 character limit.

You can disable the checking of line length by passing the error code `E501` as a value into the ignore list of `pep8`.
For example, `pep8 --ignore=E501 ./`.


### Documentation Conventions

In-code documentation utilizes Python's docstrings but does not follow [PEP 257](https://www.python.org/dev/peps/pep-0257/).
Instead, NEAT follows Sphinx's [info field lists](http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists) as its docstring format.
Please adhere to this standard as future documentation builds become more and more difficult to accurately make the more deviations are made away from this format.

In addition, Python source files identify themselves using the following header.

```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) 2017 NEAT Team
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

"""
{{filename_without_extension}}
.. module:: neat
    :platform: Linux, MacOS, Win32
    :synopsis:
    :created: {{created_time}}
    :modified: {{last_modified_time}}
.. moduleauthor:: NEAT Team
"""
```

_Where the following apply:_

<dl>
  <dt><code>{{filename_without_extension}}</code></dt>
  <dd>The current file's name disregarding any extensions (e.g. `__init__.py` would become `__init__`)</dd>
  <dt><code>{{created_time}}</code></dt>
  <dd>The timestamp at which the file was created, following the <a href="https://momentjs.com/">Moment.js</a> format <code>MM-DD-YYYY HH:mm:ss</code></dd>
  <dt><code>{{last_modified_time}}</code></dt>
  <dd>The timestamp at which the file was last modified, following the <a href="https://momentjs.com/">Moment.js</a> format <code>MM-DD-YYYY HH:mm:ss</code></dd>
</dl>

We understand that this header is a pain to manually add on each commit.
That is why we suggest you use a modern code editor such as [Sublime Text 3](https://www.sublimetext.com/3) or more preferably [Atom](https://atom.io/) and utilize their respective file header plugins [FileHeader](https://packagecontrol.io/packages/FileHeader) and [file-header](https://atom.io/packages/file-header).
Please follow this standard as it makes documentation 10x easier for current and future documentation systems.


### Testing Conventions

NEAT tests are written using Python's standard [unittest](https://docs.python.org/3.6/library/unittest.html) module.
However, tests are executed via the [nose](https://nose.readthedocs.io/en/latest/) framework.


---

## Setup

<!-- This section of the contributing document is continually subject to change -->

### Building Documentation

As stated previously, NEAT depends on Sphinx as its documentation builder.
This requires the sphinx toolkit to be installed on the user's system which is extremely easy to do.
By executing the following command outside of any Python virtual environments will ensure that the latest version of the Sphinx toolkit (and its dependencies) is installed and available on your system.

`pip install sphinx`

_This dependency is also already listed in the project's `requirements.txt`._

After you have the Sphinx toolkit, documentation can be built by executing the `make html` command within the documentation directory (docs).
However, changes outside of `autodoc`, which manages in-code docstrings, need to be written in [reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html) and pointed to by the `index.rst`.
For more information, simply go through Sphinx's [First Steps with Sphinx](http://www.sphinx-doc.org/en/stable/tutorial.html).