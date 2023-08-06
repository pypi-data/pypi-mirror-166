import numpy as np
from pathlib import Path
from event_tools import get_events

def test_event():
    cwd = Path(__file__)
    rna_npy = cwd.parent / "dRNA.npy"
    rna_signal = np.load(rna_npy).astype(np.float32)

    et = get_events(rna_signal, True)
    print(et.n, et.start, et.end)
    for event in et.event[:5]:
        print(event.start, event.length, event.mean, event.stdv, event.pos, event.state)
    return 0


def test_event2():
    rna_signal = np.arange(100).astype(np.float32)

    et = get_events(rna_signal, True)
    print(et.n, et.start, et.end)
    for event in et.event[:5]:
        print(event.start, event.length, event.mean, event.stdv, event.pos, event.state)
    return 0