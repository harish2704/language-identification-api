

## Prerequisite
* python3


## Installation

To avoid local package pollution, it would be better to create virtual environment for this installation

```bash
pip3 install virtualenv

# Create a virtual env in ./venv directory
virtualenv ./venv

# Activate virtualenv
. ./venv/bin/activate
```

Then install dependencies

```bash
pip3 install -r ./requirements.txt
```

## Running server

```bash
./run-server.sh 

# INFO:language-detector:Training model ...
# INFO:language-detector:Downloading dataset from url ...
# INFO:language-detector:Saved dataset to cache ...
# INFO:language-detector:Training complete. Feature count: 6109840
# INFO:language-detector:saved model lang-detect-MNB.pkl
# INFO:     Started server process [1780455]
# INFO:uvicorn.error:Started server process [1780455]
# INFO:     Waiting for application startup.
# INFO:uvicorn.error:Waiting for application startup.
# INFO:     Application startup complete.
# INFO:uvicorn.error:Application startup complete.
# INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
# INFO:uvicorn.error:Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)

```

## checking API response from terminal

```bash
curl -X POST  -H "Accept: application/json"  -H "Content-Type: application/json"  "http://localhost:8000/api/language-detect"  -d '{"text": "Hello how old are you"}'

# {"lang": "English", "score": 0.9998260997236165}
```
