# DIGITAL DISPLAY

send display to API


## Authors

- [@hackolite](https://www.github.com/hackolite)


## Installation

Install Display via pip


```bash
  git clone https://github.com/hackolite/display_interactive.git
  cd ./display_interactive/project
  python3.8 -m pip install .
  export OPEN_API_KEY = "1234"
```
    
## EXECUTION

check that customers.csv and purchases.csv are in data folder

```bash
  cd data
  send_display --url http://google.com --flight AF1234
```

## TEST
Test json body validation

```bash
  cd ..
  pytest tests
```