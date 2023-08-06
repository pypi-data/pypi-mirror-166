# Usage

```python
>>> import numpy as np
>>> from event_tools import get_events
>>>
>>> raw_data = np.load("tests/dRNA.npy").astype(np.float64)
>>> et = get_events(raw_data)
>>> et.start, et.end, et.n
(0, 12351, 12351)
>>> for event in et.event[:5]:
>>>     print(event.start, event.length, event.mean, event.stdv)
0 5.0 578.0 9.230384607372091
5 7.0 552.5714285714286 5.576920370275112
12 3.0 564.6666666666666 9.463379711055676
15 3.0 548.6666666666666 3.2998316455440815
18 4.0 553.75 4.205650960315181
```