# Search Engine

## Description

Yahoo Stock Market News Search Engine built with PyLucene.

## Usage

### Steps

1. Crawl Yahoo Stock Market News
2. Start Backend for indexing and API endpoint
3. Start frontend to interact with API

### Crawler

#### Setting Up Virtual Enviroment (If Wanted)

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

#### Installation

```python
pip install -r requirements

brew install subversion

svn co https://svn.apache.org/repos/asf/lucene/pylucene/trunk/jcc jcc
```

#### Usage

##### Interacting Directly with Python Script

###### Arguments

- "--hops"
  - Number of hops from root
- "--seed"
  - URL for root
- "--out"
  - Output directory
- "--threads"
  - Number of threads
- "--mb"
  - Size of output file in MB
- "--pages"
  - Number of pages to scrape
  
###### Example

```python
python main.py --hops 3 --seed https://finance.yahoo.com/topic/stock-market-news/ --out output.json --threads 4 --mb 2 --pages 10000
```

##### Using Crawler.sh/Crawler.bat

###### Set Up Permissions

Unix/Linux
```bash
chmod 700 crawler.sh
```

Windows
```bash
chmod 700 crawler.bat
```

###### Arguments

- First Argument
  - Number of hops from root
- Second Argument
  - URL for root
- Third Argument
  - Output directory
- Fourth Argument
  - Number of threads
- Fifth Argument
  - Size of output file in MB
- Sixth Argument
  - Max number of pages to scrape
  
###### Example

Unix/Linux
```bash
./crawler.sh 3 https://finance.yahoo.com/topic/stock-market-news/ output.json 4 0.8 10000
```

Windows
```bash
./crawler.bat 3 https://finance.yahoo.com/topic/stock-market-news/ output.json 4 0.8 10000   
```


### Backend 


#### Setting Up Virtual Enviroment (If Wanted)

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

#### Installation

```python
pip install -r requirements
```

#### Usage

**May need to change request url in front end to match backend url - frontend is set up to request from class-067 server**

```python
python3 app.py
```

### Frontend

#### Installation

```
npm i
```

#### Usage

**Make sure you are running this on campus or using UCR's VPN**

```
npm run dev
```
