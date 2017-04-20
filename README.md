# NEAT
_Appstate's networked energy appliance translator (NEAT)._

[![Build Status](https://travis-ci.org/ritashugisha/neat.svg?branch=master)](https://travis-ci.org/ritashugisha/neat)
[![codecov](https://codecov.io/gh/ritashugisha/neat/branch/master/graph/badge.svg)](https://codecov.io/gh/ritashugisha/neat)
[![Requirements Status](https://requires.io/github/ritashugisha/neat/requirements.svg?branch=master)](https://requires.io/github/ritashugisha/neat/requirements/?branch=master)
[![Documentation Status](https://readthedocs.org/projects/appstate-neat/badge/?version=latest)](http://appstate-neat.readthedocs.io/en/latest/?badge=latest)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](http://www.gnu.org/licenses/gpl-3.0)



[Appalachian State University](http://www.appstate.edu/) as of 2016 is considered by [AASHE](http://www.aashe.org/) to have the best sustainable campus out of their selection pool.[^1]
In order to achieve this, Appstate has had to mount renewable energy appliances (along with sensors) across their campus in order to ensure their devices are functioning optimally.
Along with this, several machines have been set up to continually pipe the sensory information provided by these devices to a simple file server.
Because these devices come from different vendors and from various time periods, it becomes increasingly difficult to store the **actually useful** sensory information provided by these devices as more and more of them are added to the network.

### Goal

> The goal of the NEAT system, is to take sensory output from the already present renewable energy appliances applying translation, simplification, and optimal storage of the data into a real-time database.

We hope to provide a modular enough architecture to be built upon horizontally in a fashion which is easy for novice and experienced developers to "get their hands dirty" using the system as soon as possible.
Removing as much complexity as possible from the developer trying to retrieve useful data, greatly eases the ability for future visualization and analysis.


### Licensing

This project is licensed by the [GNU GPLv3](https://www.gnu.org/licenses/gpl-3.0.en.html) license.
This is a strong copyleft license which basically means that permissions are conditioned on making available **complete** source code of licensed works and modifications (including larger works).
This license was chosen with upmost care as we feel that the potential of this project may encourage future use of renewable energy appliances in conjunction with this system.
We found our decision on the basis that any form of software built to aid the future of renewable energy adoption should be free and open to the public for consumption.


### Documentation

Documentation for such a project is vital.
Unfortunately, since the team performing starting work on this project have only a single cycle of 10 weeks for development (meeting for less than 10 hours a week) there isn't much time to build an exceptional product.
Because of this, we have put a heavy focus on documentation (as opposed to our belief in Agile development).
Because potentially different teams of students will be taking up the reigns of this project every semester, it is important to convey as much useful information as possible to the current developing team.
For our documentation purposes, we have decided to utilize both the GitHub repositories wiki as well as in-code [Sphinx](http://www.sphinx-doc.org/en/stable/) documentation.


### Development

For an overview of development standards to adhere to, please thoroughly read through our [CONTRIBUTING.md](./.github/CONTRIBUTING.md).


### Contributors

The following people are _listed_ contributors of this project.
**Note**, that there may be people who aided greatly in the development cycles of this project but have not been listed for various reasons.

<!-- A note to editors of this list, please keep to the list format as much as possible -->

- Sierra Milosh <[SierraMilosh](https://github.com/SierraMilosh)> ([miloshsr1@appstate.edu](mailto:miloshsr1@appstate.edu))
- Stephen Bunn <[ritashugisha](https://github.com/ritashugisha)> ([ritashugisha@gmail.com](mailto:ritashugisha@gmail.com))
- Nathan Davis <[Kanthalon](https://github.com/Kanthalon)> ([davisna1@appstate.edu](mailto:davisna1@appstate.edu))
- James Ward <[thehunte199](https://github.com/thehunte199)> ([wardja2@appstate.edu](mailto:wardja2@appstate.edu))



[^1]: http://appalachianmagazine.org/stories/id/683
