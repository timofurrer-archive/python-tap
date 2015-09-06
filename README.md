# python-tap
> Pythonic module to produce TAP (Test Anything Protocol) result files

***

[![Build Status](https://travis-ci.org/timofurrer/python-tap.svg)](https://travis-ci.org/timofurrer/python-tap)

## Install python-tap

Using pip:

    pip install tap


## How to use

You can integrate `python-tap` into every testing framework. The only thing you need is that you have access to the result results.

```python
import tap
```

### Create TAP Result file by adding Procedures

```python
import tap

result = tap.TAPResult()
result += tap.TAPProcedure(True, "Some test scenario")
result += tap.TAPProcedure(True, "Some other test scenario")
result += tap.TAPProcedure(False, "Some failed test scenario")
result += tap.TAPProcedure(False, "Some not implemented test scenario", "TODO")
result += tap.TAPProcedure(False, "Some skipped test scenario", "SKIP")
result += tap.TAPProcedure(False, "Some failed test scenario", data={"message": "Failed because ...", "severity": "error"})
print(result)
```

As result you will get:

```tap
TAP version 13
1..6
ok 1 - Some test scenario
ok 2 - Some other test scenario
not ok 3 - Some failed test scenario
not ok 4 - Some not implemented test scenario # TODO
not ok 5 - Some not implemented test scenario # SKIP
not ok 6 - Some failed test scenario
  ---
  message: Failed because ...
  severity: error
  ...
```
