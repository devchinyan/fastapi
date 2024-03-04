# python fastapi and MongoDB Template
Notes:
    - this was originally written to host in vercel as serverless
    - to run as a dedicated server in EC2 or GoogleCloud, run python cluster.py or cluster.py 1
    - this server support cluster mode for scaling based on number of cpu core run python cluster.py max

## Getting started
### 1. setup virtual env
```shell
    python3 -m venv fastapi_venv
```

### 2. activate virtual env
```shell
    source fastapi_venv/bin/activate
```
### 3. Installing Dependancy
```shell
    pip install -r requirements.txt 
```

### 4. Invoke Makefile commend
note: for information refer to Makefile 
```shell
    make start
```


## Unit Testing
### integration test
```shell
    pytest -v
```