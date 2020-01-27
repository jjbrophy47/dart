"""
Decision tree implementation for binary-class classification and binary-valued attributes.
Adapted from MLFromScratch: https://github.com/eriklindernoren/ML-From-Scratch.

Uses certified removal to improve deletion efficiency.
"""
import numpy as np


class DecisionNode():
    """Class that represents a decision node or leaf in the decision tree

    Parameters:
    -----------
    feature_i: int
        Feature index which we want to use as the threshold measure.
    threshold: float
        The value that we will compare feature values at feature_i against to determine the prediction.
    value: float
        The class prediction if classification tree, or float value if regression tree.
    true_branch: DecisionNode
        Next decision node for samples where features value met the threshold.
    false_branch: DecisionNode
        Next decision node for samples where features value did not meet the threshold.
    """
    def __init__(self, feature_i=None, threshold=None, value=None, left_branch=None, right_branch=None,
                 node_dict=None):
        self.feature_i = feature_i          # Index for the feature that is tested
        self.threshold = threshold          # Threshold value for feature
        self.value = value                  # Value if the node is a leaf in the tree
        self.left_branch = left_branch      # 'Left' subtree
        self.right_branch = right_branch    # 'Right' subtree
        self.node_dict = node_dict          # Attribute split / leaf metadata

    def copy(self):
        left_node = self.left_branch.copy() if self.left_branch is not None else None
        right_node = self.right_branch.copy() if self.right_branch is not None else None
        node_dict = self.node_dict.copy()
        node = DecisionNode(feature_i=self.feature_i, threshold=self.threshold, value=self.value,
                            left_branch=left_node, right_branch=right_node, node_dict=node_dict)
        return node


class Tree(object):
    """
    Decision Tree using Gini index for the splitting criterion.

    Parameters:
    -----------
    epsilon: float (default=0.1)
        Efficiency-utility tradeoff; lower for more deletion efficieny, higher for more utility.
    gamma: float (default=0.1)
        Fraction of data guaranteed for certified removal.
    max_depth: int (default=4)
        The maximum depth of a tree.
    min_samples_split: int (default=2)
        The minimum number of samples needed to make a split when building a tree.
    random_state: int (default=None)
        Random state for reproducibility.
    verbose: int (default=0)
        Verbosity level.
    """
    def __init__(self, epsilon=0.1, gamma=0.1, max_depth=4, min_samples_split=2, verbose=0, random_state=None):
        self.epsilon = epsilon
        self.gamma = gamma
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.random_state = random_state
        self.verbose = verbose

    def __str__(self):
        s = 'Tree:'
        s += '\nepsilon={}'.format(self.epsilon)
        s += '\ngamma={}'.format(self.gamma)
        s += '\nmax_depth={}'.format(self.max_depth)
        s += '\nmin_samples_split={}'.format(self.min_samples_split)
        s += '\nrandom_state={}'.format(self.random_state)
        s += '\nverbose={}'.format(self.verbose)
        return s

    def fit(self, X, y):
        """
        Build decision tree.
        """
        assert X.ndim == 2
        assert y.ndim == 1
        self.n_features_ = X.shape[1]

        # save the data into dicts for easy deletion
        self.X_train_, self.y_train_ = self._numpy_to_dict(X, y)
        keys = np.arange(X.shape[0])

        self.root_ = self._build_tree(X, y, keys)
        return self

    def _remove_elements(self, arr, elements):
        return np.setdiff1d(arr, elements)

    def _numpy_to_dict(self, X, y):
        """
        Converts numpy data into dicts.
        """
        Xd, yd = {}, {}
        for i in range(X.shape[0]):
            Xd[i] = X[i]
            yd[i] = y[i]
        return Xd, yd

    def _get_numpy_data(self, indices):
        """
        Collects the data from the dicts as specified by indices,
        then puts them into numpy arrays.
        """
        n_samples = len(indices)
        X = np.zeros((n_samples, self.n_features_), np.int32)
        y = np.zeros(n_samples, np.int32)
        keys = np.zeros(n_samples, np.int32)

        for i, ndx in enumerate(indices):
            X[i] = self.X_train_[ndx]
            y[i] = self.y_train_[ndx]
            keys[i] = ndx

        return X, y, keys

    def _build_tree(self, X, y, keys, current_depth=0):
        """
        Recursive method which builds out the decision tree and splits X and respective y
        on the feature of X which (based on impurity) best separates the data.
        """

        # additional data structure to maintain attribute split info
        n_samples = len(keys)
        pos_count = np.sum(y)
        neg_count = n_samples - pos_count
        gini_data = round(1 - (pos_count / n_samples)**2 - (neg_count / n_samples)**2, 8)
        node_dict = {'count': n_samples, 'pos_count': pos_count, 'gini_data': gini_data}

        # handle edge cases
        create_leaf = False
        if node_dict['count'] > 0:

            # all instances of the same class
            if node_dict['pos_count'] == 0 or node_dict['pos_count'] == node_dict['count']:

                # the root node contains instances from the same class
                if current_depth == 0:
                    raise ValueError('root node contains only instances from the same class!')

                # create leaf
                else:
                    create_leaf = True

        else:
            raise ValueError('Zero samples in this node!, depth: {}'.format(current_depth))

        # create leaf
        if n_samples < self.min_samples_split or current_depth == self.max_depth or \
                self.n_features_ - current_depth == 0 or create_leaf:
            leaf_value = pos_count / n_samples
            node_dict['count'] = n_samples
            node_dict['pos_count'] = pos_count
            node_dict['leaf_value'] = 0 if node_dict['pos_count'] == 0 else node_dict['pos_count'] / node_dict['count']
            node_dict['indices'] = keys
            return DecisionNode(value=leaf_value, node_dict=node_dict)

        # create a decision node
        else:

            # save gini indexes from each attribute
            gini_indexes = []
            attr_indices = []

            # iterate through each feature
            node_dict['attr'] = {}
            for i in range(self.n_features_):

                # split the binary attribute
                left_indices = np.where(X[:, i] == 1)[0]
                right_indices = np.setdiff1d(np.arange(n_samples), left_indices)

                # debug
                if self.verbose > 1:
                    # if i == 85:
                    print(i, y[left_indices].shape, np.sum(y[right_indices].shape), current_depth)
                    # print(i, y[right_indices].shape[0], np.sum(y[right_indices]), current_depth)
                    # print()

                # make sure there is atleast 1 sample in each branch
                if len(left_indices) > 0 and len(right_indices) > 0:

                    # gather stats about the split to compute the Gini index
                    left_count = len(left_indices)
                    left_pos_count = np.sum(y[left_indices])
                    right_count = n_samples - left_count
                    right_pos_count = np.sum(y[right_indices])

                    # compute the weighted Gini index of this feature
                    left_pos_prob = left_pos_count / left_count
                    left_weight = left_count / n_samples
                    left_index = 1 - (np.square(left_pos_prob) + np.square(1 - left_pos_prob))
                    left_weighted_index = left_weight * left_index

                    right_pos_prob = right_pos_count / right_count
                    right_weight = right_count / n_samples
                    right_index = 1 - (np.square(right_pos_prob) + np.square(1 - right_pos_prob))
                    right_weighted_index = right_weight * right_index

                    # save the metadata for efficient updating
                    node_dict['attr'][i] = {'left': {}, 'right': {}}
                    node_dict['attr'][i]['left']['count'] = left_count
                    node_dict['attr'][i]['left']['pos_count'] = left_pos_count
                    node_dict['attr'][i]['left']['weight'] = left_weight
                    node_dict['attr'][i]['left']['pos_prob'] = left_pos_prob
                    node_dict['attr'][i]['left']['index'] = left_index
                    node_dict['attr'][i]['left']['weighted_index'] = left_weighted_index

                    node_dict['attr'][i]['right']['count'] = right_count
                    node_dict['attr'][i]['right']['pos_count'] = right_pos_count
                    node_dict['attr'][i]['right']['weight'] = right_weight
                    node_dict['attr'][i]['right']['pos_prob'] = right_pos_prob
                    node_dict['attr'][i]['right']['index'] = right_index
                    node_dict['attr'][i]['right']['weighted_index'] = right_weighted_index

                    gini_index = self._compute_gini_index(node_dict['attr'][i])
                    node_dict['attr'][i]['gini_index'] = gini_index

                    # save gini_indexes for later
                    gini_indexes.append(gini_index)
                    attr_indices.append(i)

            # create probability distribution over the attributes
            p = np.exp(-(self.epsilon * np.array(gini_indexes)) / (5 * self.gamma))
            p = p / p.sum()

            # sample from this distribution
            np.random.seed(self.random_state)
            chosen_i = np.random.choice(attr_indices, p=p)

            # retrieve samples for the chosen attribute
            left_indices = np.where(X[:, chosen_i] == 1)[0]
            right_indices = np.setdiff1d(np.arange(n_samples), left_indices)

            # build the node with the best attribute
            left = self._build_tree(X[left_indices], y[left_indices], keys[left_indices], current_depth + 1)
            right = self._build_tree(X[right_indices], y[right_indices], keys[right_indices], current_depth + 1)
            return DecisionNode(feature_i=chosen_i, node_dict=node_dict, left_branch=left, right_branch=right)

    def copy(self):
        """
        Return a deep copy of this object.
        """
        tree = Tree(min_samples_split=self.min_samples_split, min_impurity=self.min_impurity,
                    max_depth=self.max_depth, verbose=self.verbose)
        tree.n_features_ = self.n_features_
        tree.X_train_ = self.X_train_.copy()
        tree.y_train_ = self.y_train_.copy()

        # recursively copy the tree
        tree.root_ = self.root_.copy()

        return tree

    def predict(self, X):
        """
        Classify samples one by one and return the set of labels.
        """
        y_proba = self.predict_proba(X)
        y_pred = np.argmax(y_proba, axis=1)
        return y_pred

    def predict_proba(self, X):
        """
        Classify samples one by one and return the set of labels.
        """
        assert X.ndim == 2
        y_positive = np.array([self._predict_value(sample) for sample in X]).reshape(-1, 1)
        y_proba = np.hstack([1 - y_positive, y_positive])
        return y_proba

    def delete(self, remove_indices):
        """
        Removes instance remove_ndx from the training data and updates the model.
        """
        if isinstance(remove_indices, int):
            remove_indices = np.array([remove_indices], dtype=np.int32)

        X = np.zeros((len(remove_indices), self.n_features_))
        y = np.zeros(len(remove_indices))
        for i, remove_ndx in enumerate(remove_indices):
            X[i] = self.X_train_[remove_ndx]
            y[i] = self.y_train_[remove_ndx]

        self.deletion_types_ = []
        self.root_ = self._delete(X, y, remove_indices)

        # remove the instances from the data
        for remove_ndx in remove_indices:
            del self.X_train_[remove_ndx]
            del self.y_train_[remove_ndx]

        return self.deletion_types_

    # support batch removal
    def _delete(self, X, y, remove_indices, tree=None, current_depth=0):

        # get root node of the tree
        if tree is None:
            tree = self.root_

        # type 1: leaf node, update its metadata
        if tree.value is not None:
            self._update_leaf_node(tree, y, remove_indices)

            if self.verbose > 0:
                print('tree check complete, ended at depth {}'.format(current_depth))

            self.deletion_types_.append('1a')
            return tree

        # decision node, update the high-level metadata
        count = tree.node_dict['count'] - len(y)
        pos_count = tree.node_dict['pos_count'] - np.sum(y)
        neg_count = pos_count - count
        gini_data = round(1 - (pos_count / count)**2 - (neg_count / count)**2, 8)
        tree.node_dict['pos_count'] = pos_count
        tree.node_dict['count'] = count
        tree.node_dict['gini_data'] = gini_data

        left_indices = np.where(X[:, tree.feature_i] == 1)[0]
        right_indices = np.setdiff1d(np.arange(X.shape[0]), left_indices)
        y_left, y_right = y[left_indices], y[right_indices]

        # raise an error if there are only instances from one class are at the root
        if current_depth == 0:
            if tree.node_dict['pos_count'] == 0 or tree.node_dict['pos_count'] == tree.node_dict['count']:
                raise ValueError('Instances in the root node are all from the same class!')

        # edge case: if remaining instances in this node are of the same class, make leaf
        if tree.node_dict['pos_count'] == 0 or tree.node_dict['pos_count'] == tree.node_dict['count']:

            if self.verbose > 0:
                print('check complete, lefotvers in the same class, creating leaf at depth {}'.format(current_depth))

            tree.node_dict['attr'] = None
            tree.node_dict['leaf_value'] = tree.node_dict['pos_count'] / tree.node_dict['count']
            tree.node_dict['indices'] = self.get_indices(tree, current_depth)
            tree.node_dict['indices'] = self._remove_elements(tree.node_dict['indices'], remove_indices)
            tree_branch = DecisionNode(value=tree.node_dict['leaf_value'], node_dict=tree.node_dict)
            self.deletion_types_.append('1b')
            return tree_branch

        # type 2: all instances are removed from the left or right branch, rebuild at this node
        if tree.node_dict['attr'][tree.feature_i]['left']['count'] - len(left_indices) <= 0 or\
           tree.node_dict['attr'][tree.feature_i]['right']['count'] - len(right_indices) <= 0:

            if self.verbose > 0:
                print('hanging branch with >1 instance, rebuilding at depth {}'.format(current_depth))

            indices = self.get_indices(tree, current_depth)
            indices = self._remove_elements(indices, remove_indices)
            Xa, ya, keys = self._get_numpy_data(indices)
            self.deletion_types_.append('2a_{}'.format(current_depth))
            return self._build_tree(Xa, ya, keys, current_depth)

            # # type 2a: both branches contain one example, turn this node into a leaf
            # if tree.node_dict['attr'][tree.feature_i][nabranch]['count'] == 1:
            #     if self.verbose > 0:
            #         print('tree check complete, creating a leaf at depth {}'.format(current_depth))
            #     tree.node_dict['attr'] = None
            #     tree.node_dict['leaf_value'] = tree.node_dict['pos_count'] / tree.node_dict['count']
            #     tree.node_dict['indices'] = self.get_indices(na_branch, current_depth + 1)
            #     tree.node_dict['indices'] = self._remove_element(tree.node_dict['indices'], remove_ndx)
            #     tree_branch = DecisionNode(value=tree.node_dict['leaf_value'], node_dict=tree.node_dict)
            #     self.deletion_type_ = '2a'
            #     return tree_branch

            # if self.verbose > 0:
            #     print('hanging branch with >1 instance, rebuilding at depth {}'.format(current_depth))
            # indices = self.get_indices(tree, current_depth)
            # indices = self._remove_element(indices, remove_ndx)
            # Xa, ya, keys = self._get_numpy_data(indices)
            # self.deletion_type_ = '2b_{}'.format(current_depth)
            # return self._build_tree(Xa, ya, keys, current_depth)

        # udpate gini_index for each attribute in this node
        old_gini_indexes = []
        gini_indexes = []
        invalid_indices = []
        invalid_attr_indices = []

        for i, attr_ndx in enumerate(tree.node_dict['attr']):
            left_status, right_status = True, True

            left_indices = np.where(X[:, attr_ndx] == 1)[0]
            right_indices = np.setdiff1d(np.arange(X.shape[0]), left_indices)
            y_left, y_right = y[left_indices], y[right_indices]

            if len(y_left) > 0:
                left_status = self._update_decision_node(tree.node_dict, attr_ndx, 'left', y_left)

            if len(y_right) > 0:
                right_status = self._update_decision_node(tree.node_dict, attr_ndx, 'right', y_right)

            # this attribute causes a hanging branch, remove it from future tree models
            if left_status is None or right_status is None:
                invalid_attr_indices.append(attr_ndx)
                invalid_indices.append(i)
                old_gini_indexes.append(tree.node_dict['attr'][attr_ndx]['gini_index'])
                gini_indexes.append(0)

            # recompute the gini gain for this attribute
            else:
                attr_dict = tree.node_dict['attr'][attr_ndx]
                gini_index = self._compute_gini_index(attr_dict)
                old_gini_indexes.append(attr_dict['gini_index'])
                gini_indexes.append(gini_index)
                attr_dict['gini_index'] = gini_index

        # remove invalid attributes from the model
        for invalid_attr_ndx in invalid_attr_indices:
            del tree.node_dict['attr'][invalid_attr_ndx]

        # TODO: save old_p when it is first built?
        # recreate old probability distribution over the attributes
        old_p = np.exp(-(self.epsilon * np.array(old_gini_indexes)) / (5 * self.gamma))
        old_p = old_p / old_p.sum()

        # create probability distribution over the updated gini indexes
        p = np.exp(-(self.epsilon * np.array(gini_indexes)) / (5 * self.gamma))
        if len(invalid_attr_indices) > 0:
            p[np.array(invalid_indices)] = 0
        p = p / p.sum()

        # retrain if probability ratio over any attribute differs by more than e^ep or e^-ep
        if np.any(p / old_p > np.exp(self.epsilon)) or np.any(p / old_p < np.exp(-self.epsilon)):

            if self.verbose > 0:
                print('rebuilding at depth {}'.format(current_depth))

            indices = self.get_indices(tree, current_depth)
            indices = self._remove_elements(indices, remove_indices)
            Xa, ya, keys = self._get_numpy_data(indices)

            dtype = '2b' if len(invalid_indices) > 0 else '2c'
            self.deletion_types_.append('{}_{}'.format(dtype, current_depth))

            return self._build_tree(Xa, ya, keys, current_depth)

        # continue checking the tree
        else:

            left_indices = np.where(X[:, tree.feature_i] == 1)[0]
            right_indices = np.setdiff1d(np.arange(X.shape[0]), left_indices)
            y_left, y_right = y[left_indices], y[right_indices]

            if len(left_indices) > 0:

                if self.verbose > 0:
                    print('check complete at depth {}, traversing left'.format(current_depth))

                X_left = X[left_indices]
                left_remove_indices = remove_indices[left_indices]
                left_branch = self._delete(X_left, y_left, left_remove_indices, tree=tree.left_branch,
                                           current_depth=current_depth + 1)
                tree.left_branch = left_branch

            if len(right_indices) > 0:

                if self.verbose > 0:
                    print('check complete at depth {}, traversing right'.format(current_depth))

                X_right = X[right_indices]
                right_remove_indices = remove_indices[right_indices]
                right_branch = self._delete(X_right, y_right, right_remove_indices, tree=tree.right_branch,
                                            current_depth=current_depth + 1)
                tree.right_branch = right_branch

            return tree

    def _update_leaf_node(self, tree, y, remove_indices):
        """
        Update this leaf node to effectively remove the target index.
        """
        node_dict = tree.node_dict
        node_dict['count'] -= len(y)
        node_dict['pos_count'] -= np.sum(y)
        node_dict['leaf_value'] = 0 if node_dict['pos_count'] == 0 else node_dict['pos_count'] / node_dict['count']
        node_dict['indices'] = self._remove_elements(node_dict['indices'], remove_indices)
        tree.value = node_dict['leaf_value']

    def _update_decision_node(self, node_dict, attr_ndx, abranch, y):
        """
        Update the attribute dictionary of the node metadata.
        """

        # access the attriubute metadata
        abranch_dict = node_dict['attr'][attr_ndx][abranch]

        # if attr_ndx == 85:
        #     print()
        #     print(abranch_dict, len(y), np.sum(y))

        # # only the affected instances are in this branch
        if abranch_dict['count'] <= len(y):
            return None

        # update the affected branch
        abranch_dict['count'] -= len(y)
        abranch_dict['pos_count'] -= np.sum(y)
        # if abranch_dict['pos_count'] > abranch_dict['count']:
        #     print(attr_ndx, abranch_dict['count'], abranch_dict['pos_count'], len(y), np.sum(y))
        abranch_dict['weight'] = abranch_dict['count'] / node_dict['count']
        abranch_dict['pos_prob'] = abranch_dict['pos_count'] / abranch_dict['count']
        abranch_dict['index'] = 1 - (np.square(abranch_dict['pos_prob']) + np.square(1 - abranch_dict['pos_prob']))
        abranch_dict['weighted_index'] = abranch_dict['weight'] * abranch_dict['index']

        # # update the non-affected branch
        # nabranch = 'left' if abranch == 'right' else 'right'
        # nabranch_dict = node_dict['attr'][attr_ndx][nabranch]
        # nabranch_dict['weight'] = nabranch_dict['count'] / node_dict['count']
        # nabranch_dict['weighted_index'] = nabranch_dict['weight'] * nabranch_dict['index']

        return True

    def _compute_gini_index(self, attr_dict):
        gini_index = attr_dict['left']['weighted_index'] + attr_dict['right']['weighted_index']
        return round(gini_index, 8)

    def get_indices(self, tree=None, depth=0):
        """
        Recursively retrieve all the indices for this node from the leaves.
        """
        if tree is None:
            tree = self.root_

        # made it to a leaf node, return the indices
        if tree.value is not None:
            return tree.node_dict['indices']

        else:
            left_indices = self.get_indices(tree.left_branch, depth + 1)
            right_indices = self.get_indices(tree.right_branch, depth + 1)
            return np.concatenate([left_indices, right_indices])

    def print_tree(self, tree=None, indent='\t', depth=0):
        """
        Recursively print the decision tree.
        """
        if tree is None:
            tree = self.root_

        indent_str = indent * (depth + 1)

        # If we're at leaf => print the label
        if tree.value is not None:
            if self.verbose > 1:
                y_vals = [self.y_train_[ndx] for ndx in tree.node_dict['indices']]
                print(tree.value, tree.node_dict['indices'], y_vals)
            else:
                print(tree.value, tree.node_dict['indices'])

        # Go deeper down the tree
        else:

            # Print test
            print("X%s? " % (tree.feature_i))

            # Print the left branch
            print("%sT->" % (indent_str), end="")
            self.print_tree(tree.left_branch, depth=depth + 1)

            # Print the right branch
            print("%sF->" % (indent_str), end="")
            self.print_tree(tree.right_branch, depth=depth + 1)

    def equals(self, other=None, this=None):
        """
        Tests if this tree is equal to another tree.
        """

        # initialize tree
        if this is None:
            this = self.root_
            if other is None:
                return 0
            else:
                other = other.root_

        # check to make sure they are both leaf nodes
        if this.value is not None:
            return 1 if this.value == other.value else 0

        # check to make sure they have the same attribute split
        if this.feature_i is not None:
            return 1 if this.feature_i == other.feature_i and \
                self.equals(this.left_branch, other.left_branch) and \
                self.equals(this.right_branch, other.right_branch) else 0

    def _predict_value(self, x, tree=None):
        """
        Do a recursive search down the tree and make a prediction of the data sample by the
        value of the leaf that we end up at.
        """

        if tree is None:
            tree = self.root_

        # If we have a value (i.e we're at a leaf) => return value as the prediction
        if tree.value is not None:
            return tree.value

        # traverse the tree based on the attribute value
        if x[tree.feature_i] == 1:
            branch = tree.left_branch

        else:
            branch = tree.right_branch

        # test subtree
        return self._predict_value(x, branch)
