import handyscikit as hsk
import numpy as np


class ConvectionDiffusionInChannelTest:
    @staticmethod
    def basic():
        solution = hsk.analytical.ConvectionDiffusionInChannel(1, 1, np.array([0.001, 0.001]), 0.02)

        assert solution.calc(np.array([0.2, 0.5])) == -0.01053842453305654

        hsk.cprint("[ConvectionDiffusionInChannel Test] Basic test passed.", color="green")


class GaussianHillTest:
    @staticmethod
    def basic():
        gauss = hsk.analytical.GaussianHill(0.05, np.array([[0.001, 0], [0, 0.001]]))

        assert gauss.calc(np.array([0.1, 0.1]), 0) == 0.018315638888734175
        assert gauss.calc(np.array([0.1, 0.1]), 100) == 0.011750824499050483
        assert gauss.calc(np.array([0.1, 0.1]), 500) == 0.0024690137745113686
        assert gauss.calc(np.array([0.1, 0.1]), 999) == 0.0012434562892379337

        assert gauss.calc_initial_condition(np.array([0, 0, 0])) == 1.0
        assert gauss.calc_initial_condition(np.array([0.05, 0.05, 0])) == 0.3678794411714422

        hsk.cprint("[GaussianHill Test] Basic test passed.", color="green")


class TheisTest:
    @staticmethod
    def basic():
        theis = hsk.analytical.Theis()
        theis.set_initial_head(2000)
        theis.set_flow_rate(-0.01)
        theis.set_coe_storage(1e-6)
        theis.set_coe_conductivity(4e-13)

        error = 1e-6
        assert theis.calc(np.array([36.8176, 52.5568, 0]), 3600) == 2431.2246233501837
        assert theis.calc(np.array([36.8176, 52.5568, 0]), 7200) == 2565.994826527471

        hsk.cprint("[Theis Test] Basic test passed.", color="green")

    @staticmethod
    def aquifer_thick():
        theis = hsk.analytical.Theis(2)
        theis.set_initial_head(2000)
        theis.set_flow_rate(-0.01)
        theis.set_coe_storage(1e-6)
        theis.set_coe_conductivity(4e-13)

        error = 1e-6
        assert theis.calc(np.array([36.8176, 52.5568, 0]), 3600) == 2215.612311675092
        assert theis.calc(np.array([36.8176, 52.5568, 0]), 7200) == 2282.9974132637353

        hsk.cprint("[Theis Test] Aquifer thick test passed.", color="green")


if __name__ == "__main__":
    ConvectionDiffusionInChannelTest.basic()

    TheisTest.basic()
    TheisTest.aquifer_thick()

    GaussianHillTest.basic()