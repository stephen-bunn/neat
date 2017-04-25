===============
Getting Started
===============

.. _getting_started-developers:

Developers
----------
The following subsections detail what is required for various tasks during development.

Licensing
~~~~~~~~~
The ``neat`` framework is licensed under the `GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>`_ license.
This is a strong copyleft license which basically means that permissions are conditioned on making available **complete** source code of licensed works and modifications (including larger works).
This license was chosen with upmost care as we feel that the potential of this project may encourage future use of renewable energy appliances in conjunction with this system. We found our decision on the basis that any form of software built to aid the future of renewable energy adoption should be free and open to the public for consumption.

Versioning
~~~~~~~~~~
The ``neat`` framework strictly follows `Semantic Versioning 2.0.0 <http://semver.org>`_ as proposed by Tom Preston-Werner.
The in-house development period is to follow the 0.x.x standard until the initial release of a full scale product (at which time will change to its first major release).

Coding Conventions
~~~~~~~~~~~~~~~~~~
NEAT source follows the `PEP8 - Style Guide for Python Code <https://www.python.org/dev/peps/pep-0008/>`_ the more recently named `pycodestyle <https://pypi.python.org/pypi/pycodestyle>`_.
The only exception to this style guide is the rule on `line length <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_. This rule has been omitted simply because of its occasional annoyance.
Code written in in this project should still try to adhere to the 79 character limit while documentation should stay under the 72 character limit.

You can disable the checking of line length by passing the error code ``E501`` as a value into the ignore list of pep8. For example ``pep8 --ignore=E501 ./``.
We highly recommend you install a linter plugin for you editor that follows the pycodestyle (pep8) format.


Documentation Conventions
~~~~~~~~~~~~~~~~~~~~~~~~~
In-code documentation utilizes Python's docstrings but does not follow `PEP 257 <https://www.python.org/dev/peps/pep-0257/>`_.
Instead, NEAT follows Sphinx's `info field lists <http://www.sphinx-doc.org/en/stable/domains.html#info-field-lists>`_ as its docstring format. Please adhere to this standard as future documentation builds become more and more difficult to accurately make the more deviations are made away from this format.

In addition, Python source files identify themselves using the following header.

.. code-block:: python3

  #!/usr/bin/env python
  # -*- encoding: utf-8 -*-
  #
  # Copyright (c) 2017 {{author}} ({{contact}})
  # GNU GPLv3 <https://www.gnu.org/licenses/gpl-3.0.en.html>

*Where the following apply:*
  ``{{author}}``
    The initial author of the file
  ``{{contact}}``
    The contact email for the initial author of the file

We understand that this header is a pain to manually add on each commit.
That is why we suggest you use a modern code editor such as `Sublime Text 3 <https://www.sublimetext.com/3>`_ or more preferably `Atom <https://atom.io/>`_ and utilize their respective file header plugins `FileHeader <https://packagecontrol.io/packages/FileHeader>`_ and `file-header <https://atom.io/packages/file-header>`_.
Please follow this standard as it makes documentation 10x easier for current and future documentation systems.

NEAT depends on `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ as its documentation builder.
This requires the sphinx toolkit to be installed on the user's system which is extremely easy to do.
By executing the following command outside of any Python virtual environments will ensure that the latest version of the Sphinx toolkit (and its dependencies) is installed and available on your system.
::

  pip install sphinx

*This dependency is also already listed in the project's* ``requirements.txt``.

After you have the Sphinx toolkit, documentation can be built by executing the ``make html`` command within the documentation directory (docs).
However, changes outside of ``autodoc``, which manages in-code docstrings, need to be written in `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_ and pointed to by the ``index.rst``.
For more information, simply go through Sphinx's `First Steps with Sphinx <http://www.sphinx-doc.org/en/stable/tutorial.html>`_.

Testing Conventions
~~~~~~~~~~~~~~~~~~~
NEAT tests are written using Python's standard `unittest <https://docs.python.org/3.6/library/unittest.html>`_ module.
However, tests are executed via the `nose <https://nose.readthedocs.io/en/latest/>`_ framework.

Unittests for ``neat`` require both nose and `codecov <https://pypi.python.org/pypi/codecov>`_.
These packages are not listed
Tests should be run from the root directory of the repository using the following command:
::

  nosetests --with-coverage

The ``.coveragerc`` file defines what folders to run tests for and what files to avoid testing.

We use a continuous integration system, `TravisCI <https://travis-ci.org/>`_, to continually check test cases on public pushes to the GitHub repository.
We also utilize codecov, which presents code coverage as reported by TravisCI after each public push. The configuration for continuous integration can be found in the standard ``.travis.yml`` file, found in the root of the repository.

Logging Conventions
~~~~~~~~~~~~~~~~~~~
Logging is enabled by default and runs on the :class:`logging.Logger` ``DEBUG`` level.
The default logging format is:
::

  %(asctime)s - %(levelname)s - %(filename)s:%(lineno)s<%(funcName)s> %(message)s

The ``neat`` framework also comes with a custom logging exception handler which logs exceptions.
All of these logging properties can be modified by changing the values of the ``neat`` constants:

.. code-block:: python

  import logging
  import neat

  # log any exceptions that occur
  neat.const.log_exceptions = True

  # update the logging level so just INFO and greater logs are displayed
  neat.const.log_level = logging.INFO

  # update the logging format so just the message is displayed
  neat.const.log_format = '%(message)s'

Logs are stored on ``stdout`` as well as stored in a rotating file handler.
A certain days logs are stored under the ``/logs/{year}/{month}`` directory in the ``{month}{day}{year}.log`` files.
For example, the following log file path is for logs created on April 1, 2017:
::

  /logs/2017/4/04012017.log

Log files are split every ``1024 * 1024`` bytes.

* Logs should primarily relay information about signal calls, and record transforms on the ``DEBUG`` level via ``logging.debug('...')``.
* Any information about pipe connection status or general startup/shutdown information should be on the ``INFO`` level via ``logging.info('...')``.
* Invalid input, data, configuration that doesn't cause the runtime to crash should be on the ``WARNING`` level via ``logging.warning('...')``.
* Any invalid state or unexpected error that causes the runtime to skip over some important logic should be on the ``ERROR`` level via ``logging.error('...')``.
* Any state causing the framework to crash should be on the ``CRITICAL`` level via ``logging.critical('...')``.
* Finally, any caught exceptions that are used as quick fixes to errors should be logged on the ``EXCEPTION`` level via ``log.exception('...')``.

Log lines typically also have ``...`` appended to the end in order to accomodate external logging parsers.
This line ending is separated from the message of the log line by a space.

Installing Dependencies
~~~~~~~~~~~~~~~~~~~~~~~
NEAT depends on several packages provided by `PyPi <https://pypi.python.org/pypi>`_ which need to be installed for NEAT to function correctly. These should be installed into a virtual Python environment by using the ``virtualenv`` package. To set this up, first install the ``virtualenv`` and ``virtualenvwrapper`` packages via pip.
::

  pip install virtualenv virtualenvwrapper

Note, if working on Windows, it may be necessary to install the ``virtualenvwrapper-win`` module as well.
This simply takes the functionality of ``virtualenvwrapper`` and translates it to batch scripts which Windows systems can run.

After installing these packages you should now have access to several scripts such as ``mkvirtualenv``, ``workon``, ``rmvirtualenv``, and `others <https://virtualenvwrapper.readthedocs.io/en/latest/command_ref.html>`_.
However, it may also be necessary to set a environmental variable to tell the installed scripts where to setup all virtual environments. This is typically done under the ``WORKON_HOME`` variable.
::

  export WORKON_HOME=~/.virtualenvs/

This indicates that all virtual environments will be built and stored under the directory ``~/.virtualenvs/``

NEAT is built and developed using `Python 3.5+ <https://www.python.org/downloads/>`_, so it may be necessary to specify the version of Python to use when creating a virtual environment.
::

  mkvirtualenv --python=/usr/bin/python3 neat

This will create and place your current shell into the context of a new virtual environment neat (if it doesn't exist already). Note, most modern shells show an indication of what virtual environment you are currently located in. For example, a common shell prompt...
::

  /home/r/Documents/Github/neat $

may be transformed to something resembling...
::

  (neat) /home/r/Documents/Github/neat $

Once inside of this virtual environment it is possible to install dependencies. All of NEATs dependencies are specified in the ``requirements.txt`` file located in the root of the repository. This file follows pip's requirements file format.
The dependencies listed in this file can be automatically installed using the virtual environment's pip script by passing the path to the requirements file after giving pip the -r flag.
::

  pip install -r ./requirements.txt

If the pip installation goes successfully, then all listed requirements should be successfully installed to the virtual environment.
To get out of the virtual environment, simply use the ``deactivate`` command (only available inside of a virtual environment).
To re-enter a virtual environment, use the ``workon neat`` command, where neat is the name of the virtual environment you created.

In order for the pipes to function correctly, the servers for a pipe's database is required and must be running.

* `RethinkDB <https://www.rethinkdb.com/docs/install/>`_ for the :class:`~neat.pipe.rethinkdb.RethinkDBPipe`
* `MongoDB <https://www.mongodb.com/download-center?jmp=nav>`_ for the :class:`~neat.pipe.mongodb.MongoDBPipe`


Contributing
------------
The following subsections are for people who wish to contribute to the ``neat`` framework.
We assume that if you want to contribute, you will abide by the standards discussed in :ref:`getting_started-developers`.

Issues
~~~~~~
Best issues are a `short, self contained, correct example <http://sscce.org>`_ of the problem.
Providing logs for when the error occured is also very helpful.

Pull Requests
~~~~~~~~~~~~~
All pull requests must be done on the `dev <https://github.com/ritashugisha/neat/tree/dev>`_ branch.
Pull requests on the ``master`` branch should be ignored


Extending NEAT
--------------
The following subsections detail tasks required for extending the ``neat`` framework.

New Devices
~~~~~~~~~~~
For every new type of device that doesn't go through the Obvius, a new concrete subclass of :class:`~neat.requester._common.AbstractRequester` must be defined in order to retrieve the devices status.
The amazing `Requests <http://docs.python-requests.org/en/master/>`_ package is provided by default in the installation of ``neat`` as well as `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/>`_ and `lxml <http://lxml.de>`_ for parsing XML typed content which should ease the effort of future developers.
It may also (most likely) be necessary to define a new concrete subclass of :class:`~neat.translator._common.AbstractTranslator`.
For each new type of device status format, a translator must be able to convert the status into a :class:`~neat.models.record.Record` object for the pipes to correctly handle.

New Pipes
~~~~~~~~~
If other forms of storage are needed, a new concrete subclass of :class:`~neat.pipe._common.AbstractPipe` must be defined.
These typically need to handle all the logic of starting and maintaining a connection to the database (if developing a database-based pipe) and creation and deletion of databases, tables, users and potentially entries.
The only thing provided to the database is a :class:`~neat.models.record.Record` instance which must be deconstructed in however necessary to pass it through the pipe.


End Users
---------
Typically end users should have to only configure the config file required by a client whose superclass is :class:`~neat.client.AbstractClient`.
For example, NEAT comes with a :class:`~neat.client.BasicClient` which uses `YAML <http://yaml.org>`_ to indicate what is required for the engine.

Starting the project can be done using a simple Python script which starts the client.

.. code-block:: python3

  import neat
  client = neat.BasicClient.from_config('PATH TO CONFIG')
  client.start()

Logging and other configuration can be done by editing the constants before starting the client

.. code-block:: python3

  import neat
  import logging

  neat.const.log_exceptions = True
  neat.const.log_level = logging.DEBUG

In order for pipes to function correctly, the client servers for the desired pipes must be started before running the ``neat`` client.
This can be done by starting the RethinkDB and MongoDB pipes in a separate process like the following:
::

  rethinkdb -d /path/to/rethinkdb/storage/directory
  mongodb --dp-path=/path/to/mongodb/storage/directory
