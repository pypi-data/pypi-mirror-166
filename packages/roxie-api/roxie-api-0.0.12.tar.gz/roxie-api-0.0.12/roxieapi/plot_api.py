import operator
from typing import Any

import matplotlib  # type: ignore
import numpy as np
import pandas as pd
import plotly.express as px  # type: ignore
import plotly.graph_objects as go  # type: ignore
import pyvista as pv
import vtk  # type: ignore

from roxieapi.xml_api import X_COORDINATE, Y_COORDINATE

ROXIE_COLOR_MAP_RGB = [
    (17, 0, 181),
    (11, 42, 238),
    (0, 104, 236),
    (0, 154, 235),
    (0, 208, 226),
    (0, 246, 244),
    (0, 255, 0),
    (116, 255, 0),
    (191, 255, 0),
    (252, 255, 0),
    (255, 199, 0),
    (255, 146, 0),
    (255, 86, 0),
    (255, 0, 0),
    (246, 0, 0),
    (232, 0, 0),
    (197, 0, 50),
    (168, 0, 159),
]

ROXIE_COLOR_MAP_RGB_PLOTLY = [
    f"rgb{color_code_rgb}" for color_code_rgb in ROXIE_COLOR_MAP_RGB
]


def rgb_to_hex(rgb):
    return "#%02x%02x%02x" % rgb


ROXIE_COLOR_MAP_HEX = [rgb_to_hex(rgb) for rgb in ROXIE_COLOR_MAP_RGB]
ROXIE_COLOR_MAP_RGB_MATPLOTLIB = matplotlib.colors.ListedColormap(
    ROXIE_COLOR_MAP_HEX, name="ROXIE_COLORMAP"
)


def plotly_results(
    strand_data: pd.DataFrame,
    column: str,
    figsize=(750, 600),
    xlim=(0, 80),
    ylim=(0, 80),
) -> None:
    """Function plotting results with plotly package

    :param strand_data: a dataframe with strand positions and field values
    :param xlim: limits in x-direction
    :param ylim: limits in y-direction
    """

    fig = px.scatter(
        strand_data,
        x="x, [mm]",
        y="y, [mm]",
        color=column,
        hover_data=[column],
        color_continuous_scale=ROXIE_COLOR_MAP_RGB_PLOTLY,
    )
    fig.update_layout(
        autosize=False,
        width=figsize[0],
        height=figsize[1],
        xaxis_range=xlim,
        yaxis_range=ylim,
        plot_bgcolor="rgba(0,0,0,0)",
        images=[
            dict(
                source="https://i.ibb.co/kcc2mbw/ROXIE.png",
                xref="paper",
                yref="paper",
                x=1.16,
                y=-0.05,
                sizex=0.2,
                sizey=0.2,
                xanchor="right",
                yanchor="bottom",
            )
        ],
    )
    fig.show()


def plotly_mesh(
    x_values, y_values, elements, figsize=(750, 750), xlim=(-80, 80), ylim=(-80, 80)
):
    """Method plotting blocks with plotly library

    :param figsize: size of the figure on a display
    :param xlim: limits in x-direction
    :param ylim: limits in y-direction
    """
    go_scatters = _create_plotly_scatters(x_values, y_values, elements)

    fig = go.Figure(go_scatters)
    fig.update_layout(
        autosize=False,
        width=figsize[0],
        height=figsize[1],
        yaxis_range=ylim,
        xaxis_range=xlim,
        showlegend=False,
        plot_bgcolor="rgba(0,0,0,0)",
    )
    fig.add_trace(px.scatter(x=[0], y=[0]).data[0])
    fig.update_xaxes(title=dict(text="x, [mm]"))
    fig.update_yaxes(title=dict(text="y, [mm]"))
    fig.show()


def _create_plotly_scatters(x_values, y_values, elements):
    """Static method creating a list of plotly scatter instances

    :param blocks: list of blocks to convert to plotly scatter
    :return: a list of plotly scatter instances
    """
    go_scatter = []
    index = 1
    for element in elements:
        x = list(operator.itemgetter(*element)(x_values))
        y = list(operator.itemgetter(*element)(y_values))
        x.append(x[0])
        y.append(y[0])

        go_scatter.append(
            go.Scatter(
                x=x,
                y=y,
                fill="toself",
                fillcolor="white",
                marker=dict(size=1),
                name="element" + str(index),
                line=go.scatter.Line(color="blue"),
            )
        )
        index += 1

    return go_scatter


def plot_strand_mesh_data(
    strand_data_df: pd.DataFrame,
    mesh_data_df: pd.DataFrame,
    elements: list,
    field_name_strand: str,
    field_name_mesh: str,
    show_bar_strand=False,
    show_bar_mesh=True,
    point_size_strand=2.5,
) -> None:
    """
    Function plotting mesh data along with strand data
    :param strand_data_df: a dataframe with x y coordinates of strands and at least one column with strand data to plot
    :param  mesh_data_df: a dataframe with x y coordinates of mesh nodes and at least one column with mesh data to plot
    :param elements: a list of lists with mesh elements definition. The outer list goes from 1 to number of mesh
        elements. The inner list goes from 1 to m nodes of a mesh element. The inner loop contains mesh indices
    :param field_name_strand: name of a column with strand data to plot
    :param field_name_mesh: name of a column with mesh data to plot
    :param show_bar_strand: if True a bar legend for mesh data is shown, otherwise hidden
    :param show_bar_mesh: if True a bar legend for mesh data is shown, otherwise hidden
    :param point_size_strand: size of a strand point with data
    """
    vtk_grid_strand = _initialize_vtk_grid_with_points(
        strand_data_df[[X_COORDINATE, Y_COORDINATE]].values
    )
    vtk_grid_mesh = _initialize_vtk_grid_with_points(
        mesh_data_df[[X_COORDINATE, Y_COORDINATE]].values
    )

    for element in elements:
        vtk_grid_mesh.InsertNextCell(vtk.VTK_POLYGON, len(element), element)

    field_mesh = mesh_data_df[field_name_mesh].values
    field_strand = strand_data_df[field_name_strand].values

    pv_grid_strand = _initialize_pyvista_grid_with_vtk_grid_and_point_data(
        vtk_grid_strand, field_strand, field_name=field_name_strand
    )

    pv_grid_mesh = _initialize_pyvista_grid_with_vtk_grid_and_point_data(
        vtk_grid_mesh, field_mesh, field_name=field_name_mesh
    )

    pl = pv.Plotter()
    pl.add_points(
        pv_grid_strand.points,
        scalars=field_strand,
        cmap=ROXIE_COLOR_MAP_RGB_MATPLOTLIB,
        show_scalar_bar=show_bar_strand,
        point_size=point_size_strand,
    )
    pl.add_mesh(
        pv_grid_mesh, cmap=ROXIE_COLOR_MAP_RGB_MATPLOTLIB, show_scalar_bar=show_bar_mesh
    )

    pl.view_xy()
    pl.enable_joystick_style()
    pl.show()


def _initialize_vtk_grid_with_points(xy_points: np.ndarray) -> vtk.vtkUnstructuredGrid:
    vtk_grid = vtk.vtkUnstructuredGrid()
    vtk_points = vtk.vtkPoints()

    for i, (x, y) in enumerate(xy_points):
        vtk_points.InsertPoint(i, x, y, 0.0)

    vtk_grid.SetPoints(vtk_points)

    return vtk_grid


def _initialize_pyvista_grid_with_vtk_grid_and_point_data(
    vtk_grid: vtk.vtkUnstructuredGrid,
    point_data: np.ndarray[float, Any],
    field_name="field",
) -> pv.UnstructuredGrid:
    pv_grid = pv.UnstructuredGrid(vtk_grid)
    pv_grid.point_data[field_name] = point_data

    return pv_grid
