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

NEAT source follows the [PEP8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/) the more recently named [pycodestyle](https://pypi.python.org/pypi/pycodestyle).
The only exception to this style guide is the rule on [line length](https://www.python.org/dev/peps/pep-0008/#maximum-line-length).
This rule has been omitted simply because of its occasional annoyance.
Code written in in this project should still try to adhere to the 79 character limit while documentation should stay under the 72 character limit.

You can disable the checking of line length by passing the error code `E501` as a value into the ignore list of `pep8`.
For example, `pep8 --ignore=E501 ./`.

We **highly** recommend you install a linter plugin for you editor that follows the pycodestyle (pep8) format.


### Documentation Conventions

In-code documentation utilizes Python's docstrings but does not follow [PEP 257](https://www.python.org/dev/peps/pep-0257/).
Instead, NEAT follows Sphinx's [info field lists](http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists) as its docstring format.
Please adhere to this standard as future documentation builds become more and more difficult to accurately make the more deviations are made away from this format.

In addition, Python source files identify themselves using the following header.

```python
#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# Copyright (c) {{year}} {{author}} ({{contact}})
# GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>
```

_Where the following apply:_

<dl>
  <dt><code>{{year}}</code></dt>
  <dd>The current year of editing the file</dd>
  <dt><code>{{author}}</code></dt>
  <dd>The author of the file</dd>
  <dt><code>{{contact}}</code></dt>
  <dd>A method of contacting the author, most likely email</dd>
</dl>

We understand that this header is a pain to manually add on each commit.
That is why we suggest you use a modern code editor such as [Sublime Text 3](https://www.sublimetext.com/3) or more preferably [Atom](https://atom.io/) and utilize their respective file header plugins [FileHeader](https://packagecontrol.io/packages/FileHeader) and [file-header](https://atom.io/packages/file-header).
Please follow this standard as it makes documentation 10x easier for current and future documentation systems.


### Testing Conventions

NEAT tests are written using Python's standard [unittest](https://docs.python.org/3.6/library/unittest.html) module.
However, tests are executed via the [nose](https://nose.readthedocs.io/en/latest/) framework.


---

## Setup

Below is several sub-sections which talk about how to get started contributing to NEAT's development.

<!-- This section of the contributing document is continually subject to change -->

### Installing Dependencies

NEAT depends on several packages provided by [PyPi](https://pypi.python.org/pypi) which need to be installed for NEAT to function correctly.
These should be installed into a virtual Python environment by using the `virtualenv` package.
To set this up, first install the `virtualenv` and `virtualenvwrapper` packages via pip.

`pip install virtualenv virtualenvwrapper`

**Note**, if working on Windows, it may be necessary to install the `virtualenvwrapper-win` module as well.
This simply takes the functionality of `virtualenvwrapper` and translates it to batch scripts which Windows systems can run.

After installing these packages you should now have access to several scripts such as `mkvirtualenv`, `workon`, `rmvirtualenv`, and [others](https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html).
However, it may also be necessary to set a environmental variable to tell the installed scripts where to setup all virtual environments.
This is typically done under the `WORKON_HOME` variable.

`export WORKON_HOME=~/.virtualenvs/`

This indicates that all virtual environments will be built and stored under the directory `~/.virtualenvs/`

NEAT is built and developed using Python 3, so it may be necessary to specify the version of Python to use when creating a virtual environment.

`mkvirtualenv --python=/usr/bin/python3 neat`

This will create and place your current shell into the context of a new virtual environment **neat** (if it doesn't exist already).
Note, most modern shells show an indication of what virtual environment you are currently located in. For example, a common shell prompt...

`/home/r/Documents/Github/neat $`

may be transformed to something resembling...

`(neat) /home/r/Documents/Github/neat $`

Once inside of this virtual environment it is possible to install dependencies.
All of NEATs dependencies are specified in the `requirements.txt` file located in the root of the repository.
This file follows pip's [requirements file format](https://pip.pypa.io/en/stable/reference/pip_install/#requirements-file-format).
The dependencies listed in this file can be automatically installed using the virtual environment's pip script by passing the path to the requirements file after giving pip the `-r` flag.

`pip install -r ./requirements.txt`

If the pip installation goes successfully, then all listed requirements should be successfully installed to the virtual environment.

To get out of the virtual environment, simply use the `deactivate` command (only available inside of a virtual environment).
To re-enter a virtual environment, use the `workon neat` command, where _neat_ is the name of the virtual environment you created.


### Building Documentation

As stated previously, NEAT depends on Sphinx as its documentation builder.
This requires the sphinx toolkit to be installed on the user's system which is extremely easy to do.
By executing the following command outside of any Python virtual environments will ensure that the latest version of the Sphinx toolkit (and its dependencies) is installed and available on your system.

`pip install sphinx`

_This dependency is also already listed in the project's `requirements.txt`._

After you have the Sphinx toolkit, documentation can be built by executing the `make html` command within the documentation directory (docs).
However, changes outside of `autodoc`, which manages in-code docstrings, need to be written in [reStructuredText](http://www.sphinx-doc.org/en/stable/rest.html) and pointed to by the `index.rst`.
For more information, simply go through Sphinx's [First Steps with Sphinx](http://www.sphinx-doc.org/en/stable/tutorial.html).


### Writing Tests

We test all code using [nose](https://nose.readthedocs.io/en/latest/) but write all tests using the standard [unittest](https://docs.python.org/3/library/unittest.html) module included in Python.
We have given an example for how to write test cases in `nose/tests/_example.py`.
Please follow the standard of keeping multiple related test cases within the same source file.


### Running Tests

Tests can be run using the `nosetests` command (once the dependency has be installed).
NEAT also depends on the `coverage` module, and can report code test coverage through executing the `nosetests --with-coverage` command.

We use a continuous integration system, [TravisCI](https://travis-ci.org/), to continually check test cases on public pushes to the GitHub repository.
We also utilize [codecov](https://codecov.io/gh), which presents code coverage as reported by TravisCI after each public push.
The configuration for continuous integration can be found in the standard `.travis.yml` file, found in the root of the repository.
