Getting Started
===============

End Users
---------
Typically end users should have to only configure the config file required by a client whose superclass is :class:`neat.client.AbstractClient`.
For example, NEAT comes with a :class:`neat.client.BasicClient` which uses `YAML <http://yaml.org>`_ to indicate what is required for the engine.

.. code-block:: yaml

  ---
  pipes:                                # List of desired pipes
    - $:           RethinkDBPipe          # Pipe class name
      ip:          localhost                # RethinkDB client IP
      port:        28015                    # RethinkDB client port
      table:       devices                  # RethinkDB storage table
      clean_delay: 300                      # Number of seconds between record cleaning
    - $:           MongoDBPipe            # Pipe class name
      ip:          localhost                # MongoDB client IP
      port:        27017                    # MongoDB client port
      table:       devices                  # MongoDB storage table
      entry_delay: 100                      # Number of seconds between record entries
  devices:                              # List for desired scheduler -> record mappings
    - scheduler:                          # The desired scheduler
        $:           SimpleDelayScheduler # Scheduler class name
        delay:       10.0                   # amount of seconds to wait between records
      requester:                          # The requester for the desired scheduler
        $:           ObviusRequester      # Requester class name
        device_id:   1                      # Device ID of the Obvius
        obvius_ip:   123.45.67.89           # IP address of the Obvius
        obvius_port: 80                     # HTTP port for the Obvius
        obvius_user: USER                   # Username to the Obvius
        obvius_pass: PASS                   # Read-only password to the Obvius
        name:        solar_therm.1          # Unique reference of the Obvius device
        type:        SOLAR_THERM            # Device type of the Obvius device
        lat:         -12.3                  # Latitude of the device
        lon:         12.3                   # Longitude of the device
        ttl:         300                    # Time the device records should stay alive
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
