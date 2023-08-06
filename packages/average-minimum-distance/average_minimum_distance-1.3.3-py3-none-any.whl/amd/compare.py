"""Functions for comparing AMDs and PDDs of crystals.
"""

import warnings
from typing import List, Optional, Union
from functools import partial
from itertools import combinations
import os

import numpy as np
import pandas as pd
from scipy.spatial.distance import cdist, pdist, squareform
from joblib import Parallel, delayed
from progressbar import ProgressBar

from .io import CifReader, CSDReader
from .calculate import AMD, PDD
from ._emd import network_simplex
from .periodicset import PeriodicSet


def compare(
        crystals,
        crystals_=None,
        by='AMD',
        k=100,
        **kwargs
) -> pd.DataFrame:
    r"""Given one or two sets of periodic set(s), refcode(s) or cif(s), compare them
    returning a DataFrame of the distance matrix. Default is to comapre by PDD
    with k=100. Accepts most keyword arguments accepted by the CifReader, CSDReader
    and compare functions, for a full list see the documentation Quick Start page.
    Note that using refcodes requires csd-python-api.

    Parameters
    ----------
    crystals : array or list of arrays
        One or a collection of paths, refcodes, file objects or :class:`.periodicset.PeriodicSet` s.
    crystals\_ : array or list of arrays, optional
        One or a collection of paths, refcodes, file objects or :class:`.periodicset.PeriodicSet` s.
    by : str, default 'AMD'
        Invariant to compare by, either 'AMD' or 'PDD'.
    k : int, default 100
        k value to use for the invariants (length of AMD, or number of columns in PDD).

    Returns
    -------
    df : pandas.DataFrame
        DataFrame of the distance matrix for the given crystals compared by the chosen invariant.

    Raises
    ------
    ValueError
        If by is not 'AMD' or 'PDD', if either set given have no valid crystals
        to compare, or if crystals or crystals\_ are an invalid type.

    Examples
    --------
    Compare everything in a .cif (deafult, AMD with k=100)::

        df = amd.compare('data.cif')

    Compare everything in one cif with all crystals in all cifs in a directory (PDD, k=50)::

        df = amd.compare('data.cif', 'dir/to/cifs', by='PDD', k=50)

    **Examples (csd-python-api only)**

    Compare two crystals by CSD refcode (PDD, k=50)::

        df = amd.compare('DEBXIT01', 'DEBXIT02', by='PDD', k=50)

    Compare everything in a refcode family (AMD, k=100)::

        df = amd.compare('DEBXIT', families=True)
    """

    by = by.upper()
    if by not in ('AMD', 'PDD'):
        raise ValueError(f"parameter 'by' accepts 'AMD' or 'PDD', was passed {by}")

    reader_kwargs = {
        'reader': 'ase',
        'families': False,
        'remove_hydrogens': False,
        'disorder': 'skip',
        'heaviest_component': False,
        'molecular_centres': False,
        'show_warnings': True,
    }

    calc_kwargs = {
        'collapse': True,
        'collapse_tol': 1e-4,
        'lexsort': False,
    }

    compare_kwargs = {
        'metric': 'chebyshev',
        'n_jobs': None,
        'verbose': 0,
        'low_memory': False,
    }

    for default_kwargs in (reader_kwargs, calc_kwargs, compare_kwargs):
        for key in kwargs.keys() & default_kwargs.keys():
            default_kwargs[key] = kwargs[key]

    crystals = _unwrap_periodicset_list(crystals, **reader_kwargs)
    if not crystals:
        raise ValueError('No valid crystals to compare in first set.')
    names = [s.name for s in crystals]

    if crystals_ is None:
        names_ = names
    else:
        crystals_ = _unwrap_periodicset_list(crystals_, **reader_kwargs)
        if not crystals_:
            raise ValueError('No valid crystals to compare in second set.')
        names_ = [s.name for s in crystals_]

    if reader_kwargs['molecular_centres']:
        crystals = [(c.molecular_centres, c.cell) for c in crystals]
        if crystals_:
            crystals_ = [(c.molecular_centres, c.cell) for c in crystals_]

    if by == 'AMD':

        invs = [AMD(s, k) for s in crystals]
        compare_kwargs.pop('n_jobs', None)
        compare_kwargs.pop('verbose', None)

        if crystals_ is None:
            dm = squareform(AMD_pdist(invs, **compare_kwargs))
        else:
            invs_ = [AMD(s, k) for s in crystals_]
            dm = AMD_cdist(invs, invs_, **compare_kwargs)

    elif by == 'PDD':

        invs = [PDD(s, k, **calc_kwargs) for s in crystals]
        compare_kwargs.pop('low_memory', None)

        if crystals_ is None:
            dm = squareform(PDD_pdist(invs, **compare_kwargs))
        else:
            invs_ = [PDD(s, k) for s in crystals_]
            dm = PDD_cdist(invs, invs_, **compare_kwargs)

    return pd.DataFrame(dm, index=names, columns=names_)


def EMD(
        pdd: np.ndarray,
        pdd_: np.ndarray,
        metric: Optional[str] = 'chebyshev',
        return_transport: Optional[bool] = False,
        **kwargs):
    r"""Earth mover's distance (EMD) between two PDDs, also known as
    the Wasserstein metric.

    Parameters
    ----------
    pdd : numpy.ndarray
        PDD of a crystal.
    pdd\_ : numpy.ndarray
        PDD of a crystal.
    metric : str or callable, default 'chebyshev'
        EMD between PDDs requires defining a distance between PDD rows.
        By default, Chebyshev (L-infinity) distance is chosen as with AMDs.
        Accepts any metric accepted by :func:`scipy.spatial.distance.cdist`.
    return_transport: bool, default False
        Return a tuple ``(distance, transport_plan)`` with the optimal transport.

    Returns
    -------
    emd : float
        Earth mover's distance between two PDDs.

    Raises
    ------
    ValueError
        Thrown if ``pdd`` and ``pdd_`` do not have the same number of 
        columns (``k`` value).
    """

    dm = cdist(pdd[:, 1:], pdd_[:, 1:], metric=metric, **kwargs)
    emd_dist, transport_plan = network_simplex(pdd[:, 0], pdd_[:, 0], dm)

    if return_transport:
        return emd_dist, transport_plan

    return emd_dist


def AMD_cdist(
        amds: Union[np.ndarray, List[np.ndarray]],
        amds_: Union[np.ndarray, List[np.ndarray]],
        metric: str = 'chebyshev',
        low_memory: bool = False,
        **kwargs
) -> np.ndarray:
    r"""Compare two sets of AMDs with each other, returning a distance matrix.
    This function is essentially identical to :func:`scipy.spatial.distance.cdist`
    with the default metric ``chebyshev``.

    Parameters
    ----------
    amds : array_like
        A list of AMDs.
    amds\_ : array_like
        A list of AMDs.
    metric : str or callable, default 'chebyshev'
        Usually AMDs are compared with the Chebyshev (L-infinitys) distance.
        Can take any metric accepted by :func:`scipy.spatial.distance.cdist`.
    low_memory : bool, default False
        Use a slower but more memory efficient method for
        large collections of AMDs (Chebyshev metric only).

    Returns
    -------
    dm : numpy.ndarray
        A distance matrix shape ``(len(amds), len(amds_))``.
        ``dm[ij]`` is the distance (given by ``metric``) 
        between ``amds[i]`` and ``amds[j]``.
    """

    amds, amds_ = np.asarray(amds), np.asarray(amds_)

    if len(amds.shape) == 1:
        amds = np.array([amds])
    if len(amds_.shape) == 1:
        amds_ = np.array([amds_])

    if low_memory:
        if metric != 'chebyshev':
            warnings.warn("Using only allowed metric 'chebyshev' for low_memory", UserWarning)

        dm = np.empty((len(amds), len(amds_)))
        for i, amd_vec in enumerate(amds):
            dm[i] = np.amax(np.abs(amds_ - amd_vec), axis=-1)
    else:
        dm = cdist(amds, amds_, metric=metric, **kwargs)

    return dm


def AMD_pdist(
        amds: Union[np.ndarray, List[np.ndarray]],
        metric: str = 'chebyshev',
        low_memory: bool = False,
        **kwargs
) -> np.ndarray:
    """Compare a set of AMDs pairwise, returning a condensed distance matrix.
    This function is essentially identical to :func:`scipy.spatial.distance.pdist`
    with the default metric ``chebyshev``.

    Parameters
    ----------
    amds : array_like
        An array/list of AMDs.
    metric : str or callable, default 'chebyshev'
        Usually AMDs are compared with the Chebyshev (L-infinity) distance.
        Can take any metric accepted by :func:`scipy.spatial.distance.pdist`.
    low_memory : bool, default False
        Optionally use a slightly slower but more memory efficient method for
        large collections of AMDs (Chebyshev metric only).

    Returns
    -------
    numpy.ndarray
        Returns a condensed distance matrix. Collapses a square distance
        matrix into a vector, just keeping the upper half. See
        :func:`scipy.spatial.distance.squareform` to convert to a square 
        distance matrix or for more on condensed distance matrices.
    """

    amds = np.asarray(amds)

    if len(amds.shape) == 1:
        amds = np.array([amds])

    if low_memory:
        m = len(amds)
        if metric != 'chebyshev':
            warnings.warn("Using only allowed metric 'chebyshev' for low_memory", UserWarning)
        cdm = np.empty((m * (m - 1)) // 2, dtype=np.double)
        ind = 0
        for i in range(m):
            ind_ = ind + m - i - 1
            cdm[ind:ind_] = np.amax(np.abs(amds[i+1:] - amds[i]), axis=-1)
            ind = ind_
    else:
        cdm = pdist(amds, metric=metric, **kwargs)

    return cdm


def PDD_cdist(
        pdds: List[np.ndarray],
        pdds_: List[np.ndarray],
        metric: str = 'chebyshev',
        backend='multiprocessing',
        n_jobs=None,
        verbose=0,
        **kwargs
) -> np.ndarray:
    r"""Compare two sets of PDDs with each other, returning a distance matrix.
    Supports parallel processing via joblib. If using parallelisation, make sure to
    include a if __name__ == '__main__' guard around this function.

    Parameters
    ----------
    pdds : List[numpy.ndarray]
        A list of PDDs.
    pdds\_ : List[numpy.ndarray]
        A list of PDDs.
    metric : str or callable, default 'chebyshev'
        Usually PDD rows are compared with the Chebyshev/l-infinity distance.
        Can take any metric accepted by :func:`scipy.spatial.distance.cdist`.
    n_jobs : int, default None
        Maximum number of concurrent jobs for parallel processing with joblib.
        Set to -1 to use the maximum possible. Note that for small inputs (< 100), 
        using parallel processing may be slower than the default n_jobs=None.
    verbose : int, default 0
        Controls verbosity. If using parallel processing (n_jobs > 1), verbose is
        passed to :class:`joblib.Parallel`, where larger values = more verbosity.
        Otherwise, uses progressbar2 where the progressbar is either on or off.
    backend : str, default 'multiprocessing'
        Specifies the parallelization backend implementation. For a list of
        supported backends, see the backend argument of :class:`joblib.Parallel`.

    Returns
    -------
    numpy.ndarray
        Returns a distance matrix shape ``(len(pdds), len(pdds_))``.
        The :math:`ij` th entry is the distance between ``pdds[i]``
        and ``pdds_[j]`` given by Earth mover's distance.
    """

    if isinstance(pdds, np.ndarray):
        if len(pdds.shape) == 2:
            pdds = [pdds]

    if isinstance(pdds_, np.ndarray):
        if len(pdds_.shape) == 2:
            pdds_ = [pdds_]

    kwargs.pop('return_transport', None)

    if n_jobs is not None and n_jobs > 1:
        # TODO: put results into preallocated empty array in place
        dm = Parallel(backend=backend, n_jobs=n_jobs, verbose=verbose)(
            delayed(partial(EMD, metric=metric, **kwargs))(pdds[i], pdds_[j])
            for i in range(len(pdds)) for j in range(len(pdds_))
        )
        dm = np.array(dm).reshape((len(pdds), len(pdds_)))

    else:
        n, m = len(pdds), len(pdds_)
        dm = np.empty((n, m))
        if verbose:
            bar = ProgressBar(max_value=n * m)
        count = 0
        for i in range(n):
            for j in range(m):
                dm[i, j] = EMD(pdds[i], pdds_[j], metric=metric, **kwargs)
                if verbose:
                    count += 1
                    bar.update(count)
    return dm


def PDD_pdist(
        pdds: List[np.ndarray],
        metric: str = 'chebyshev',
        n_jobs=None,
        verbose=0,
        backend='multiprocessing',
        **kwargs
) -> np.ndarray:
    """Compare a set of PDDs pairwise, returning a condensed distance matrix.
    Supports parallelisation via joblib. If using parallelisation, make sure to
    include a if __name__ == '__main__' guard around this function.

    Parameters
    ----------
    pdds : List[numpy.ndarray]
        A list of PDDs.
    metric : str or callable, default 'chebyshev'
        Usually PDD rows are compared with the Chebyshev/l-infinity distance.
        Can take any metric accepted by :func:`scipy.spatial.distance.pdist`.
    n_jobs : int, default None
        Maximum number of concurrent jobs for parallel processing with joblib.
        Set to -1 to use the maximum possible. Note that for small inputs (< 100), 
        using parallel processing may be slower than the default n_jobs=None.
    verbose : int, default 0
        Controls verbosity. If using parallel processing (n_jobs > 1), verbose is
        passed to :class:`joblib.Parallel`, where larger values = more verbosity.
        Otherwise, uses progressbar2 where the progress bar is either on or off.
    backend : str, default 'multiprocessing'
        Specifies the parallelization backend implementation. For a list of
        supported backends, see the backend argument of :class:`joblib.Parallel`.

    Returns
    -------
    numpy.ndarray
        Returns a condensed distance matrix. Collapses a square
        distance matrix into a vector just keeping the upper half. See
        :func:`scipy.spatial.distance.squareform` to convert to a square 
        distance matrix or for more on condensed distance matrices.
    """

    kwargs.pop('return_transport', None)

    if n_jobs is not None and n_jobs > 1:
        # TODO: put results into preallocated empty array in place
        cdm = Parallel(backend=backend, n_jobs=n_jobs, verbose=verbose)(
            delayed(partial(EMD, metric=metric, **kwargs))(pdds[i], pdds[j])
            for i, j in combinations(range(len(pdds)), 2)
        )
        cdm = np.array(cdm)
    
    else:
        m = len(pdds)
        cdm_len = (m * (m - 1)) // 2
        cdm = np.empty(cdm_len, dtype=np.double)
        inds = ((i, j) for i in range(0, m - 1) for j in range(i + 1, m))
        if verbose:
            bar = ProgressBar(max_value=cdm_len)
        for r, (i, j) in enumerate(inds):
            cdm[r] = EMD(pdds[i], pdds[j], metric=metric, **kwargs)
            if verbose:
                bar.update(r)
    return cdm


def emd(
        pdd: np.ndarray,
        pdd_: np.ndarray,
        metric: Optional[str] = 'chebyshev',
        return_transport: Optional[bool] = False,
        **kwargs):
    """Alias for amd.EMD()."""
    return EMD(pdd, pdd_, metric=metric, return_transport=return_transport, **kwargs)


def _unwrap_periodicset_list(psets_or_str, **reader_kwargs):
    """Valid input for compare (PeriodicSet, path, refcode, lists of such)
    --> 
    list of PeriodicSets"""

    if isinstance(psets_or_str, PeriodicSet):
        return [psets_or_str]
    elif isinstance(psets_or_str, list):
        return [s for item in psets_or_str for s in _extract_periodicsets(item, **reader_kwargs)]
    else:
        return _extract_periodicsets(psets_or_str, **reader_kwargs)


def _extract_periodicsets(item, **reader_kwargs):
    """str (path/refocde), file or PeriodicSet --> list of PeriodicSets."""

    if isinstance(item, PeriodicSet):
        return [item]
    elif isinstance(item, str) and not os.path.isfile(item) and not os.path.isdir(item):
        reader_kwargs.pop('reader', None)
        return list(CSDReader(item, **reader_kwargs))
    else:
        reader_kwargs.pop('families', None)
        reader_kwargs.pop('refcodes', None)
        return list(CifReader(item, **reader_kwargs))
