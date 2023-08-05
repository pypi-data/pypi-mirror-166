# AutoDocker

Simple program to quickly dock ligands using Autodock Vina.

[![PyPI version](https://badge.fury.io/py/AutoDocker.svg)](https://badge.fury.io/py/AutoDocker) [![Downloads](https://pepy.tech/badge/autodocker)](https://pepy.tech/project/autodocker)

## Installation:

```
pip install AutoDocker
```

## Usage:

#### Prepare receptor PDBQT

```
AutoDocker.protpdb2pdbqt("receptor.pdb")
```

#### Run single docking calculation

```
AutoDocker.RunAutoDocker("receptor.pdb","ligand.sdf","config.txt","path-to-vina-executable")
OR
AutoDocker.RunVina("path-to-vina-executable","receptor.pdbqt","ligand.pdbqt","config.txt")
```

#### Run docking calculation for database (Only sdf format supported)

```
AutoDocker.RunAutoDocker("receptor.pdb","database.sdf","config.txt","path-to-vina-executable")
```
