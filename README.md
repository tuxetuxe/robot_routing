# Robot Routing

## Requirements

- Python 3.7+


## Setup

Install requirements
```bash
pip install -r requirements.txt
```

## Build

Bulld docker image
```bash
sudo docker build -t robot_routing .
```

## Execute
```bash
docker run \
    -v $(pwd)/problems:/problems \
    robot_routing \
    /problems/<problem file> \
    /problems/<solution file>
```

## Test

```bash
py.test -v -s --cov-report term-missing --cov=robot_routing -r w tests
