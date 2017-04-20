Getting Started
===============

End Users
---------
Typically end users should have to only configure the config file required by a client whose superclass is :class:`~neat.client.AbstractClient`.
For example, NEAT comes with a :class:`~neat.client.BasicClient` which uses `YAML <http://yaml.org>`_ to indicate what is required for the engine.

Developers
----------

New Devices
~~~~~~~~~~~
For every new type of device that doesn't go through the Obvius, a new concrete subclass of :class:`~neat.requester._common.AbstractRequester` must be defined in order to retrieve the devices status.
The amazing `Requests <http://docs.python-requests.org/en/master/>`_ package is provided by default in the installation of ``neat`` as well as `BeautifulSoup <https://www.crummy.com/software/BeautifulSoup/>`_ and `lxml <http://lxml.de>`_ for parsing XML typed content which should ease the effort of future developers.
It may also (most likely) be necessary to define a new concrete subclass of :class:`~neat.translator._common.AbstractTranslator`.
For each new type of device status format, a translator must be able to convert the status into a :class:`~neat.models.record.Record` object for the pipes to correctly handle.
