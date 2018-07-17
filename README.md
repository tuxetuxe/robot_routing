# Robot Routing

## Requirements

- Python 3.7+
- VirtualEnv


## Setup

Create virtual environment
```bash
virtualenv -p python3.6 venv
```

Activate virtual environment
```bash
source ./venv/bin/activate
```

Install requirements
```bash
pip install -r requirements.txt
```

## Build

Run the test suit
```bash
    pytest -v -s --cov-report term-missing --cov=robot_routing -r w tests
```

Build docker image
```bash
sudo docker build -t robot_routing .
```

## Execute

Execute the script directly in your machine

> Don't forget to follow the "Setup" steps!

```bash
    python robot_routing <problem file> <solution file>
```

Use the docker image to solve a problem
```bash
docker run \
    -v $(pwd)/problems:/problems \
    robot_routing \
    /problems/<problem file> \
    /problems/<solution file>
```

Solve all problems in the problems folder (except sample):
```bash
    ./solve_all_problems.sh
```