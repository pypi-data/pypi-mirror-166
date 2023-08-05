from ..common.print_related import cprint
from .core.mesh_2d import Mesh2D
from .core.mesh_base import meshing_timer
import gmsh
import numpy as np


# todo: gmsh 有getBaryCenter的接口。（闲着没事的时候再升级）
# todo: 有哪些边界条件没指定的检测，这里做一个Warn的提示，不作为红色的bug，不然会给调试带来困难。(闲着没事的时候再升级)
class SquareCase(Mesh2D):
    def __init__(self, size, coordinate=[0, 0]):
        Mesh2D.__init__(self)

        gmsh.model.occ.addRectangle(coordinate[0], coordinate[1], 0, size, size)
        gmsh.model.occ.synchronize()

        self._dim = 2
        self._node_per_face = 2
        self._size = size
        self._structured_num = None

    @meshing_timer
    def generate_structured(self, mesh_number, show_mesh=False):
        self._structured_num = mesh_number
        self._gmsh_element_type = 3  # 3 means quadrilateral.
        self._face_per_cell = 4
        self._node_per_cell = 4

        gmsh.model.mesh.set_transfinite_curve(1, mesh_number[0] + 1)  # down
        gmsh.model.mesh.set_transfinite_curve(2, mesh_number[1] + 1)  # right
        gmsh.model.mesh.set_transfinite_curve(3, mesh_number[0] + 1)  # up
        gmsh.model.mesh.set_transfinite_curve(4, mesh_number[1] + 1)  # left
        gmsh.model.mesh.set_transfinite_surface(1, "Left")
        gmsh.model.mesh.generate(2)
        gmsh.model.mesh.recombine()
        if show_mesh: gmsh.fltk.run()

        self._generate_topology()

    @meshing_timer
    def generate_unstructured(self, size_list=None, show_mesh=False):
        self._gmsh_element_type = 2  # 2 means triangle.
        self._face_per_cell = 3
        self._node_per_cell = 3

        if size_list is not None:
            gmsh.model.mesh.set_size([(0, 1)], size_list[0])
            gmsh.model.mesh.set_size([(0, 2)], size_list[1])
            gmsh.model.mesh.set_size([(0, 3)], size_list[2])
            gmsh.model.mesh.set_size([(0, 4)], size_list[3])
        gmsh.model.mesh.generate(2)
        if show_mesh: gmsh.fltk.run()

        self._generate_topology()

    @property
    def boundary_down(self):
        return 1

    @property
    def boundary_right(self):
        return 2

    @property
    def boundary_up(self):
        return 3

    @property
    def boundary_left(self):
        return 4

    @property
    def square_area(self):
        return 1

    @property
    def size(self):
        return self._size

    @property
    def structured_num(self):
        return self._structured_num
