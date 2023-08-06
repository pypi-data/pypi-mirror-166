from ..common import cprint
import vtkmodules.all as vtk


class VtkVisualizeBase:
    def __init__(self):
        # Actor property.
        self._actor_prop_geom = vtk.vtkProperty()
        self._actor_prop_geom.SetColor((0.91, 0.87, 0.67))
        self._actor_prop_geom.SetOpacity(0.3)
        self._actor_prop_geom.SetDiffuse(0)
        self._actor_prop_geom.SetAmbient(1)
        self._actor_prop_geom.SetLineWidth(1)
        self._actor_prop_mesh = vtk.vtkProperty()
        self._actor_prop_mesh.SetColor((0, 0, 0))
        self._actor_prop_mesh.SetOpacity(1)
        self._actor_prop_mesh.SetDiffuse(0)
        self._actor_prop_mesh.SetAmbient(1)
        self._actor_prop_mesh.SetLineWidth(1)
        # Color table.
        self._color_table = vtk.vtkLookupTable()
        self._color_table.SetRange(0, 1)
        self._color_table.SetHueRange(0.6804, 0)
        self._color_table.SetNumberOfColors(100)
        # Interactor.
        self._interactor = vtk.vtkRenderWindowInteractor()
        self._interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        # Render window.
        self._render_window = vtk.vtkRenderWindow()
        self._render_window.SetSize(800, 800)
        # Interactor.
        self._interactor.SetRenderWindow(self._render_window)
        # Renderer.
        self._renderer = vtk.vtkRenderer()
        self._renderer.SetBackground((1, 1, 1))
        self._render_window.AddRenderer(self._renderer)
        # Scalarbar actor.
        self._scalarBarActor = vtk.vtkScalarBarActor()
        self._scalarBarActor.UnconstrainedFontSizeOn()
        self._scalarBarActor.GetLabelTextProperty().SetColor(0, 0, 0)
        self._scalarBarActor.GetLabelTextProperty().SetColor(124 / 255, 124 / 255, 124 / 255)
        self._scalarBarActor.GetLabelTextProperty().SetFontSize(13)
        self._scalarBarActor.GetLabelTextProperty().SetBold(False)
        self._scalarBarActor.GetLabelTextProperty().SetShadow(False)
        self._scalarBarActor.SetTitle("")
        self._scalarBarActor.SetWidth(0.05)
        self._scalarBarActor.SetHeight(0.6)
        self._scalarBarActor.SetNumberOfLabels(8)
        self._scalarBarActor.SetOrientationToVertical()
        self._scalarBarActor.GetPositionCoordinate().SetValue(0.9, 0.2)
        # Unstructured grid.
        self._uGrid = None
        self._uGrid_reader = None
        self._uGrid_scalar_range = (0, 1)


class VtkVisualize(VtkVisualizeBase):
    def __init__(self):
        VtkVisualizeBase.__init__(self)

        cprint("This is deprecated, please use contour class.", color="yellow")

    def load_uGrid_data(self, mesh, result=None):
        # Make topology points.
        points = vtk.vtkPoints()
        points.Allocate(mesh.node_num)
        for node in mesh.nodes:
            points.InsertNextPoint(node[0], node[1], 0)

        # Make unstructured grid.
        self._uGrid = vtk.vtkUnstructuredGrid()
        self._uGrid.Allocate(mesh.cell_num)
        self._uGrid.SetPoints(points)
        for cell in mesh.cells:
            self._uGrid.InsertNextCell(9, 4, (cell[0], cell[1], cell[2], cell[3]))

        # Scalars.
        if result is not None:
            # Make scalars.
            scalars = vtk.vtkDoubleArray()
            for num in result:
                scalars.InsertNextTuple1(num)
            self._uGrid.GetPointData().SetScalars(scalars)

            # Set look up table range.
            self._uGrid_scalar_range = (result.min(), result.max())
            self._color_table.SetRange(self._uGrid_scalar_range[0], self._uGrid_scalar_range[1])

    def load_uGrid_file(self, filename):
        # Make unstructured grid.
        self._uGrid_reader = vtk.vtkUnstructuredGridReader()
        self._uGrid_reader.SetFileName(filename)
        self._uGrid_reader.Update()

    def set_geometry_property(self, color, opacity=1, diffuse=0, ambient=1, line_width=1):
        """
        Change geometry actor porperty.
        :param color: Tuple | (R, G, B).
        :param opacity: Float | [0, 1] | 0 is transparent and 1 is solid.
        :param diffuse: Float | [0, 1]
        :param ambient: Float | [0, 1]
        :param line_width: Float
        :return:
        """
        self._actor_prop_geom.SetColor(color)
        self._actor_prop_geom.SetOpacity(opacity)
        self._actor_prop_geom.SetDiffuse(diffuse)
        self._actor_prop_geom.SetAmbient(ambient)
        self._actor_prop_geom.SetLineWidth(line_width)

    def set_mesh_property(self, color, opacity=1, diffuse=0, ambient=1, line_width=1):
        """
        Change mesh actor porperty.
        :param color: Tuple | (R, G, B) | (0, 0, 0) is black and (1, 1, 1) is white.
        :param opacity: Float | [0, 1] | 0 is transparent and 1 is solid.
        :param diffuse: Float | [0, 1]
        :param ambient: Float | [0, 1]
        :param line_width: Float
        :return:
        """
        self._actor_prop_mesh.SetColor(color)
        self._actor_prop_mesh.SetOpacity(opacity)
        self._actor_prop_mesh.SetDiffuse(diffuse)
        self._actor_prop_mesh.SetAmbient(ambient)
        self._actor_prop_mesh.SetLineWidth(line_width)

    def show_mesh(self):
        # Make geometry filter.
        geometryFileter = vtk.vtkGeometryFilter()
        geometryFileter.SetInputConnection(self._uGrid_reader.GetOutputPort())
        # Make polydata mapper.
        geometryMapper = vtk.vtkPolyDataMapper()
        geometryMapper.SetInputConnection(geometryFileter.GetOutputPort())
        # Extract edge.
        edges = vtk.vtkExtractEdges()
        edges.SetInputConnection(geometryFileter.GetOutputPort())
        # Edge mapper.
        edgeMapper = vtk.vtkPolyDataMapper()
        edgeMapper.SetInputConnection(edges.GetOutputPort())
        # Make geometry actor.
        geometry_actor = vtk.vtkActor()
        geometry_actor.SetMapper(geometryMapper)
        geometry_actor.SetProperty(self._actor_prop_geom)
        self._renderer.AddActor(geometry_actor)
        # Make edges actor.
        edge_actor = vtk.vtkActor()
        edge_actor.SetMapper(edgeMapper)
        edge_actor.SetProperty(self._actor_prop_mesh)
        self._renderer.AddActor(edge_actor)
        # Show render window and start interact.
        self._interactor.Start()

    def show_contour(self, mesh=False):
        """

        :param mesh:
        :param result: Note that this result must be node value.
        :return:
        """
        mapper = vtk.vtkDataSetMapper()
        mapper.SetInputData(self._uGrid)
        mapper.SetScalarRange(self._uGrid_scalar_range[0], self._uGrid_scalar_range[1])
        mapper.SetLookupTable(self._color_table)
        # Make contour actor.
        contour_actor = vtk.vtkActor()
        contour_actor.SetMapper(mapper)
        if mesh:
            contour_actor.GetProperty().EdgeVisibilityOn()
        else:
            contour_actor.GetProperty().EdgeVisibilityOff()
        self._renderer.AddActor(contour_actor)
        # Make scalar bar.
        self._scalarBarActor.SetLookupTable(mapper.GetLookupTable())
        self._renderer.AddActor(self._scalarBarActor)
        # Show render window and start interact.
        self._interactor.Start()






