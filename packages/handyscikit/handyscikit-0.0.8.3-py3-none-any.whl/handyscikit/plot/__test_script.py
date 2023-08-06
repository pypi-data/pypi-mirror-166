import handyscikit as hsk
import handyscikit.plot
import numpy as np


class ContourTest:
    @staticmethod
    def square_mesh():
        mesh = hsk.mesh.SquareCase(1)
        mesh.generate_structured([2, 2], show_mesh=False)

        result_node = np.array([0.0, 0.0, 2.0, 2.0, 0.0, 1.0, 2.0, 1.0, 1.0], dtype=np.float64)

        contour = hsk.plot.Contour(mesh, result_node)
        contour.show()

        hsk.cprint("[Contour Test] Square mesh test passed.", color="green")

    @staticmethod
    def triangle_mesh():
        mesh = hsk.mesh.SquareCase(1)
        mesh.generate_unstructured([1, 1, 1, 1], show_mesh=False)

        result_node = np.array([0.0, 0.0, 0.0, 0.0, 1.0], dtype=np.float64)

        contour = hsk.plot.Contour(mesh, result_node)
        contour.show()

        hsk.cprint("[Contour Test] Triangle mesh test passed.", color="green")


if __name__ == "__main__":
    # ContourTest.square_mesh()
    ContourTest.triangle_mesh()


"""Line plot"""
# figure = Figure()
# figure.set_title("3xn vs nx3 (mesh number 200)")
# figure.set_x_label("案例")
# figure.set_y_label("run time(s)")
# base_data = np.array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9])
# figure.set_base_data(base_data)
# data_1 = np.array([0.124038, 0.12445, 0.122516, 0.120756, 0.122971, 0.122542, 0.122296, 0.122151, 0.12097, 0.122452])
# figure.add_line_data(data_1, legend="data1")
# data_2 = np.array([0.138069, 0.121229, 0.128158, 0.12646, 0.12979, 0.127898, 0.12959, 0.127754, 0.128288, 0.128105])
# figure.add_line_data(data_2, legend="data2")
# figure.set_y_limit([0.12, 0.14])
# figure.add_legend()
# # figure.show()
# figure.save("1")

"""Line point plot"""
# figure_1 = Figure()
# base_data = np.array([0, 1, 2, 3, 4, 5])
# figure_1.set_base_data(base_data)
# figure_1.add_point_data(np.array([1, 2, 3, 4, 5, 6]))
# figure_1.add_line_data(np.array([0, 3, 2, 1, 4, 5]))
# figure_1.set_title("字体设置")
# figure_1.set_x_label("x轴")
# figure_1.set_y_label("y轴")
# figure_1.set_y_limit([0, 6])
# # figure_1.show()
# figure.save("2")
