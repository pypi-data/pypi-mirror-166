from .event_tools import split_signals

def get_events(data, is_rna=True):
    """
    Time series search method locates the k-best occurrences of a given query on a more extended sequence based on a
    distance measurement.

    Parameters
    ----------
    data : 1d-array
        Query signal
    is_rna : bool
        is signals from rna or dna sequence

    Returns
    -------
    et : EventTable
        event table
    """
    return split_signals(data, is_rna)
