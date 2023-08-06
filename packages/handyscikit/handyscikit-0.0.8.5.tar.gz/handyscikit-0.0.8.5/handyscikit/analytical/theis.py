import math
import numpy as np

class Theis:
    def __init__(self, thick=1):
        """
        :param thick: <float> Aquifer thick.
        """
        self._coe_storage = None
        self._coe_conductivity = None
        self._g = 9.8
        self._flow_rate = None
        self._initial_head = None
        self._thick = thick
        self._water_rho = 1000
        self._water_miu = 1.01e-3

        self.__a = [-0.57721566, 0.99999193, -0.24991055, 0.05519968, -0.00976004, 0.00107857]
        self.__b = [0.2677737343, 8.6347608925, 18.059016973, 8.5733287401]
        self.__c = [3.9584969228, 21.0996530827, 25.6329561486, 9.5733223454]

    def set_coe_conductivity(self, perimeability):
        self._coe_conductivity = (perimeability*self._water_rho*self._g/self._water_miu)*self._thick

    def set_coe_storage(self, storage):
        self._coe_storage = storage*self._thick

    def set_flow_rate(self, flow_rate):
        self._flow_rate = flow_rate

    def set_initial_head(self, initial_head):
        self._initial_head = initial_head

    def calc(self, coordinate, time):
        """
        :param coordinate: <np.ndarray> Calculation location coordinate, well must be set at (0, 0, 0).
        :param time: <float> Time.
        :return:
        """
        radius = np.linalg.norm(coordinate)
        u = radius**2*self._coe_storage / (4*self._coe_conductivity*time)
        return self._initial_head - self._flow_rate*self.__series_num(u)/(4*math.pi*self._coe_conductivity)

    def __series_num(self, u):
        if u < 1:
            tmp = self.__a[0] + u*(self.__a[1] + u*(self.__a[2] + u*(self.__a[3] + u*(self.__a[4] + u*self.__a[5]))))
            return -1*math.log(u) + tmp
        else:
            tmp1 = 1/(u*(math.e**u))
            tmp2 = self.__b[0] + u*(self.__b[1] + u*(self.__b[2] + u*(self.__b[3] + u)))
            tmp3 = self.__c[0] + u*(self.__c[1] + u*(self.__c[2] + u*(self.__c[3] + u)))
            return tmp1*tmp2/tmp3


