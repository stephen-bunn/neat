Getting Started
===============

End Users
---------
Typically end users should have to only configure the config file required by a client whose superclass is :class:`~neat.client.AbstractClient`.
For example, NEAT comes with a :class:`~neat.client.BasicClient` which uses `YAML <http://yaml.org>`_ to indicate what is required for the engine.

.. code-block:: yaml

  ---
  pipes:
    - $:           RethinkDBPipe
      ip:          localhost
      port:        28015
      table:       devices
      clean_delay: 300
    - $:           MongoDBPipe
      ip:          localhost
      port:        27017
      table:       devices
      entry_delay: 100
  devices:
    - scheduler:
        $:           SimpleDelayScheduler
        delay:       10.0
      requester:
        $:           ObviusRequester
        device_id:   18
        obvius_ip:   123.456.78.90
        obvius_port: 80
        obvius_user: user
        obvius_pass: pass
        name:        solar_therm.1
        type:        SOLAR_THERM
        lat:         -12.3
        lon:         12.3
        ttl:         300
        parsed:
          energy_total:
            point: 5
            unit:  btu
          energy_rate:
            point: 0
            unit:  btu / hour
          flow_rate:
            point: 1
            unit:  gallon / minute
          supply_temp:
            point: 3
            unit:  degF
          return_temp:
            point: 4
            unit:  degF


Developers
----------
The following subsections detail what is required for various tasks during development.

Setting Up
~~~~~~~~~~
The ``neat`` framework currently requires `Python 3.5+ <https://www.python.org/downloads/>`_ and should be developed within a virtual environment.
This can be done by installing the `virtualenv <https://virtualenv.pypa.io/en/stable/>`_ and `virtualenvwrapper <https://virtualenvwrapper.readthedocs.io/en/latest/>`_ packages using `pip <https://pip.pypa.io/en/stable/>`_ using the following command (may be different for Windows):
::

  pip install virtualenv virtualenvwrapper

A virtual environment named ``neat`` for Python 3.6 can be created using the ``virtualenvwrapper`` added scripts:
::

  mkvirtualenv neat --python=/usr/bin/python3.6

Installing the required development dependencies can be done using pip:
::

  pip install -r ./requirements.txt

In order for the pipes to function correctly, the servers for a pipe's database is required and must be running.

* `RethinkDB <https://www.rethinkdb.com/docs/install/>`_ for the :class:`~neat.pipe.rethinkdb.RethinkDBPipe`
* `MongoDB <https://www.mongodb.com/download-center?jmp=nav>`_ for the :class:`~neat.pipe.mongodb.MongoDBPipe`

Running Tests
~~~~~~~~~~~~~
Unittests for ``neat`` require both `nose <http://nose.readthedocs.io/en/latest/>`_ and `codecov <https://pypi.python.org/pypi/codecov>`_.
These packages are not listed
Tests should be run from the root directory of the repository using the following command:
::

  nosetests --with-coverage

The ``.coveragerc`` file defines what folders to run tests for and what files to avoid testing.


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
