import numpy as np
cimport numpy as np

from ._manager cimport _DataManager
from ._splitter cimport SplitRecord
from ._tree cimport Node
from ._tree cimport _Tree
from ._tree cimport _TreeBuilder
from ._utils cimport DTYPE_t
from ._utils cimport SIZE_t
from ._utils cimport INT32_t
from ._utils cimport UINT32_t

cdef class _Remover:
    """
    Recursively removes data from a _Tree built using _TreeBuilder;
    retrains a node / subtree when a better feature / threshold is optimal.
    """

    # Inner structures
    cdef _DataManager manager                # Database manager
    cdef _TreeBuilder tree_builder           # Tree Builder
    cdef bint         use_gini               # Controls splitting criterion
    cdef SIZE_t       min_samples_leaf       # Minimum number of samples for a leafs
    cdef SIZE_t       min_samples_split      # Minimum number of samples for a split
    cdef SIZE_t       k                      # Number of thresholds to sample

    # Metric structures
    cdef SIZE_t  capacity                    # Number of removal allocations for space
    cdef SIZE_t  remove_count                # Number of removals
    cdef SIZE_t* remove_types                # Removal type
    cdef SIZE_t* remove_depths               # Depth of leaf or node needing retraining
    cdef SIZE_t  retrain_sample_count        # Number of samples used for retraining

    # Python API
    cpdef int remove(self, _Tree tree, np.ndarray remove_indices)
    cpdef void clear_remove_metrics(self)

    # C API
    cdef void _remove(self, Node** node_ptr,
                      double** X, int* y,
                      int* samples, int n_samples) nogil

    cdef int _check_node(self, Node* node, double** X, int* y,
                          int* samples, int n_samples, int pos_count,
                          SplitRecord *split) nogil

    cdef int _update_splits(self, Node** node_ptr, double** X, int* y,
                            int* samples, int n_samples, int pos_count) nogil

    cdef void _update_leaf(self, Node** node_ptr, int* y, int* samples,
                           int n_samples, int pos_count) nogil

    cdef void _convert_to_leaf(self, Node** node_ptr, int* samples, int n_samples,
                               SplitRecord *split) nogil

    cdef void _retrain(self, Node*** node_ptr, double** X, int* y, int* samples,
                       int n_samples) nogil

    cdef void _get_leaf_samples(self, Node* node, int* remove_samples,
                                int n_remove_samples, int** leaf_samples_ptr,
                                int* leaf_samples_count_ptr) nogil

    cdef void _update_decision_node(self, Node** node_ptr, SplitRecord *split) nogil

    cdef void _add_removal_type(self, int remove_type, int remove_depth) nogil
    cdef np.ndarray _get_int_ndarray(self, int *data, int n_elem)
