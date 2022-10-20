# Billing AI

## Requirement
Python 3.6+

## Installation

### Download

```
$ git clone https://github.com/n-eagle/billing-ai.git
```

### Virtual Environment
Create and populate development virtualenv.

```
$ cd ~
$ python3 -m venv venv
$ . ~/venv/bin/activate
$ cd billing-ai
$ pip install -r requirement.txt
```

## Run
Run gunicorn server with:
```
$ . run_gunicorn.sh
```

Open your browser and navigate to [http://127.0.0.1:5001/test](http://127.0.0.1:5001/test).