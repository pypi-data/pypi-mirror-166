from .event_tools import search_signals

def search_events(query, reference, output=1, alpha=.5):
    """
    Time series search method locates the k-best occurrences of a given query on a more extended sequence based on a
    distance measurement.

    Parameters
    ----------
    query : 1d-array
        Query signal
    sequence : 1d-array
        Sequence signal
    output : usize
        number of hits
    alpha : weight of derivative cost
        Cost = alpha * cost_n + (1 - alpha) * cost_d

    Returns
    -------
    start_index : usize
        Start of aligned path
    end_index : usize
        End of aligned path
    path_dist : f32
        DTW distance of path
    path : (p, q)
        Aligned path
    """
    st, en, path_dist, path = search_signals(query, reference, output, alpha)

    return st, en, path_dist, path
