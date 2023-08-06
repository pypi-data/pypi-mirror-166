import vtkmodules.all as vtk


class VtkWindow:
    def __init__(self):
        self._render_window = vtk.vtkRenderWindow()
        self._render_window.SetSize(800, 800)

        self._interactor = vtk.vtkRenderWindowInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self._interactor.SetRenderWindow(self._render_window)

        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground((1, 1, 1))
        self._render_window.AddRenderer(self._renderer)



class Contour(VtkWindow):
    def __init__(self, mesh, solutions, show_mesh=False):
        """

        :param mesh:
        """
        VtkWindow.__init__(self)

        self._color_table = vtk.vtkLookupTable()
        self._color_table.SetRange(0, 1)
        self._color_table.SetHueRange(0.6804, 0)
        self._color_table.SetNumberOfColors(100)

        self._scalar_bar_actor = vtk.vtkScalarBarActor()
        self._scalar_bar_actor.UnconstrainedFontSizeOn()
        self._scalar_bar_actor.GetLabelTextProperty().SetColor(0, 0, 0)
        self._scalar_bar_actor.GetLabelTextProperty().SetColor(124 / 255, 124 / 255, 124 / 255)
        self._scalar_bar_actor.GetLabelTextProperty().SetFontSize(13)
        self._scalar_bar_actor.GetLabelTextProperty().SetBold(False)
        self._scalar_bar_actor.GetLabelTextProperty().SetShadow(False)
        self._scalar_bar_actor.SetTitle("")
        self._scalar_bar_actor.SetWidth(0.05)
        self._scalar_bar_actor.SetHeight(0.6)
        self._scalar_bar_actor.SetNumberOfLabels(8)
        self._scalar_bar_actor.SetOrientationToVertical()
        self._scalar_bar_actor.GetPositionCoordinate().SetValue(0.9, 0.2)

        self._unstructured_grid = None

        self.__make(mesh, solutions, show_mesh)

    def __make(self, mesh, solutions, show_mesh):
        points = vtk.vtkPoints()
        points.Allocate(mesh.node_num)
        for node in mesh.nodes:
            points.InsertNextPoint(node[0], node[1], node[2])

        self._unstructured_grid = vtk.vtkUnstructuredGrid()
        self._unstructured_grid.Allocate(mesh.cell_num)
        self._unstructured_grid.SetPoints(points)
        for cell in mesh.cells:
            # Element type 9 means polygon.
            self._unstructured_grid.InsertNextCell(9, mesh.node_per_cell, cell)

        scalars = vtk.vtkDoubleArray()
        for solution in solutions:
            scalars.InsertNextTuple1(solution)
        self._unstructured_grid.GetPointData().SetScalars(scalars)

        scalar_range = (solutions.min(), solutions.max())

        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(self._unstructured_grid)
        mapper.SetScalarRange(scalar_range[0], scalar_range[1])
        mapper.SetLookupTable(self._color_table)

        contour_actor = vtk.vtkActor()
        contour_actor.SetMapper(mapper)
        if show_mesh:
            contour_actor.GetProperty().EdgeVisibilityOn()
        else:
            contour_actor.GetProperty().EdgeVisibilityOff()

        self._renderer.AddActor(contour_actor)
        self._scalar_bar_actor.SetLookupTable(mapper.GetLookupTable())
        self._renderer.AddActor(self._scalar_bar_actor)

    def show(self):
        self._interactor.Start()