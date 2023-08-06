[![Tests](https://github.com/Rionzagal/MedSig/actions/workflows/tests.yml/badge.svg)](https://github.com/Rionzagal/MedSig/actions)
[![Publish](https://github.com/Rionzagal/Med-Signal/actions/workflows/publish.yml/badge.svg)](https://github.com/Rionzagal/Med-Signal/actions/workflows/publish.yml)
[![Issues](https://img.shields.io/github/issues/Rionzagal/MedSig)](https://github.com/Rionzagal/MedSig/issues)
[![License](https://img.shields.io/github/license/Rionzagal/MedSig)](./LICENSE)

# Med-Signal package for biological signals processing and simulation
This module focuses on the simulation and specific processing of known biological signals, such as EEG and ECG. This module is aimed for the study and processing of biological signals by the usage of known methods.

# Contents
- [Med-Signal package for biological signals processing and simulation](#med-signal-package-for-biological-signals-processing-and-simulation)
- [Contents](#contents)
  - [EEG module](#eeg-module)
    - [Izhikevich simulation module](#izhikevich-simulation-module)
  - [Installation](#installation)
    - [Package Requirements](#package-requirements)

## EEG module
This module contains the necesary actions for the processing and evaluation of *EEG* signals contained in a **numpy** array. The main functionality of this module is to let the user process analyze and generate simulations of *EEG* signals in a single package. This module implements actions such as:

- Read and store the signal found from a valid _.txt_, _.csv_ file containing the signal.
- Calculate the main frequencies and relevant information from the signal.
- Retrieve the relevant information and calculate the wave type based on Polar Statistics.

### Izhikevich simulation module
This module focuses on generating a model in which the user can use the Izhikevich neurons and visualize their behavior either as a **single unit** or as a **network of multiple units**. The simulation includes settings such as input value, neuron positions and *Field Voltage Response*, as well as *Single Voltage Response*. The functionality of this module is based in three data-classes functioning as models to describe the neural response based on the **Izhikevich Equations** for neural response. The classes are listed as follow:

- **NeuronTypes:** Provides the neural constants which determine the behavior of the neuron model.
- **Neuron:** The actual neural model descrved by Izhikevich. An object with this type will represent a neuron model with constants provided by the the NeuronTypes class. This is the unit that will provide the *Single Voltage Response* with a given time and input.
- **Network:** Represents a group of *Neurons* interconnected with each other. An object with this type provides a *Field Voltage Response* with its given neurons and connections.

## Installation
In order to install and make use of this package, just enter `python -m pip install med-signal` and you will be good to go! This package uses various dependencies for its optimal functions. These requirements are listed in the [section below](#package-requirements).
In order to successfuly use this package, a set of requirements are needed for its usage. These requirements will be automatically installed or upgraded *(if you already have one of the dependencies)* as the package is installed. The minimum python version needed to correctly use this package is `python 3.10`.

The following list provides the required packages with their minimal required version needed to install **MedSig**.
- Pandas - *1.4.1*
- Matplotlib - *3.5.1*
- Scipy - *1.8.0*
- Numpy - *1.22.3*
