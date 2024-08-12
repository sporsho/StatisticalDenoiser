import numpy as np
from sklearn.neighbors import KDTree

class DSOR(object):

    def clean(self, pcd, k, s, r):
        """

        :param pcd: point colud data in shape n x 3 or nx4, only x, y, z values will be used.
        :param k: minimum number of nearest neighborv
        :param s: multiplicaton factor for standard deviation
        :param r: multiplication factor for range
        :return:
        """
        labels = np.zeros(shape=(pcd.shape[0],), dtype=np.int32) # placeholder for output
        self.tree = KDTree(pcd[:, :3], leaf_size=100) # kd tree for neighbour search

        dist, ind = self.tree.query(pcd[:, :3], k=k) # get all the nearest neighbours and there distance
        dist_sum = np.sum(dist, axis=1)
        mean_dist = dist_sum / (k - 1)
        sq_mean_dist = mean_dist * mean_dist
        sum_mean_dist = np.sum(mean_dist)
        mean_mean_dist = np.mean(mean_dist)
        std_mean_dist = np.std(mean_dist)

        # Global threshold
        Tg = mean_mean_dist + s * std_mean_dist
        sq_dist = np.sum(pcd[:, :3] * pcd[:, :3], axis=1)
        for i in range(pcd.shape[0]):
            Td_sq = Tg * Tg * r * r * sq_dist[i]
            if sq_mean_dist[i] < Td_sq:
                labels[i] = 0
            else:
                labels[i] = 1

        return labels

