import numpy as np
from sklearn.neighbors import KDTree


class DROR(object):
    def clean(self, pcd, k_min, alpha, beta, sr_min):
        """

        :param pcd: point colud data in shape n x 3 or nx4, only x, y, z values will be used.
        :param k_min: Minimum number of nearest neighbor to consider
        :param alpha: horizontal angular resolution of the lidar
        :param beta: multiplication factor
        :param sr_min: minimum search radius
        :return:
        """
        labels = np.zeros(shape=(pcd.shape[0],), dtype=np.int32) # placeholder to store output
        self.tree = KDTree(pcd[:, :3], leaf_size=100) # kd tree for doing neighbor search
        RPs = np.sum(pcd[:, :3] * pcd[:, :3], axis=1) # Range from points squared
        RP = np.sqrt(RPs) # Range from points

        for i in range(pcd.shape[0]):
            rp = RP[i]
            if rp < sr_min:
                sr_p = sr_min
            else:
                sr_p = beta * rp * alpha * 3.14 / 180.0 # alpha is an angle, which needs to be in radians

            k = self.tree.query_radius(pcd[i, :3].reshape(-1,3), sr_p, count_only=True)
            if k < k_min:
                labels[i] = 1
        return labels