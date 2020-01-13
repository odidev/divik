import gc
from functools import partial
from typing import Optional

import numpy as np
from sklearn import clone

from divik.core import Data, DivikResult
from ._report import DivikReporter


def _recursive_selection(current_selection: np.ndarray, partition: np.ndarray,
                         cluster_number: int) -> np.ndarray:
    selection = np.zeros(shape=current_selection.shape, dtype=bool)
    selection[current_selection] = partition == cluster_number
    return selection


StatSelector = 'divik.feature_selection.StatSelectorMixin'
GAPSearch = 'divik.cluster._kmeans._gap.GAPSearch'


# @gmrukwa: I could not find more readable solution than recursion for now.
def divik(data: Data, selection: np.ndarray,
          kmeans: GAPSearch,
          feature_selector: StatSelector,
          minimal_size: int, rejection_size: int, report: DivikReporter) \
        -> Optional[DivikResult]:
    subset = data[selection]

    if subset.shape[0] <= max(kmeans.max_clusters, minimal_size):
        report.finished_for(subset.shape[0])
        return None

    report.filter(subset)
    feature_selector = clone(feature_selector)
    filtered_data = feature_selector.fit_transform(subset)
    report.filtered(filtered_data)

    report.processing(filtered_data)
    report.stop_check()
    kmeans_ = clone(kmeans).fit(filtered_data)
    if not kmeans_.fitted_ or kmeans_.n_clusters_ == 1:
        report.finished_for(subset.shape[0])
        return None

    partition = kmeans_.labels_
    _, counts = np.unique(partition, return_counts=True)

    if any(counts <= rejection_size):
        report.rejected(subset.shape[0])
        return None

    report.recurring(len(counts))
    recurse = partial(
        divik, data=data,
        kmeans=kmeans, feature_selector=feature_selector,
        minimal_size=minimal_size, rejection_size=rejection_size,
        report=report)
    del subset
    del filtered_data
    gc.collect()
    subregions = [
        recurse(selection=_recursive_selection(selection, partition, cluster))
        for cluster in np.unique(partition)
    ]

    report.assemble()
    return DivikResult(clustering=kmeans_, feature_selector=feature_selector,
                       merged=partition, subregions=subregions)
