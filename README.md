# Guide

## Setting Up Virtual Enviroment (If Wanted)

```python
python -m venv env
source env/bin/activate
```

## Installation

```python
pip install -r requirements
```

## Usage

### Interacting Directly with Python Script

#### Arguments

- "--hops"
  - Number of hops from root
- "--pages"
  - Number of pages
- "--seed"
  - Path to seed
- "--out"
  - Output directory
- "--threads"
  - Number of threads

#### Example

```python
python main.py --hops 6 --pages 10000 --seed seed.txt --out /output
```

### Using Crawler.sh

#### Set Up Permissions

```bash
chmod 700 crawler.sh
```

#### Arguments

- First Argument
  - Number of hops from root
- Second Argument
  - Number of pages
- Third Argument
  - Path to seed
- Fourth Argument
  - Output directory
- Fifth Argument
  - Number of threads

#### Example

```bash
./crawler.sh 6 10000 seed.txt /output/ 4
```