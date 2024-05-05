# Guide

## Setting Up Virtual Enviroment (If Wanted)

Unix/Linux
```python
python -m venv env
source env/bin/activate
```

Windows
```python
python -m venv env
source env/Scripts/activate
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
python main.py --hops 6 --pages 10000 --seed https://en.wikipedia.org/wiki/Basketball --out output.json
```

### Using Crawler.sh/Crawler.bat

#### Set Up Permissions

Unix/Linux
```bash
chmod 700 crawler.sh
```

Windows
```bash
chmod 700 crawler.bat
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

Unix/Linux
```bash
./crawler.sh 6 10000 https://en.wikipedia.org/wiki/Basketball output.json 4
```

Windows
```bash
./crawler.bat 6 10000 https://en.wikipedia.org/wiki/Basketball output.json 4
```
