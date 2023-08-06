import os
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
from pymbse.commons import text_file  # type: ignore

Y_COORDINATE = "y, [mm]"

X_COORDINATE = "x, [mm]"


def correct_xml_file(input_xml_path: str, output_xml_path: str) -> None:
    """Static method for correcting an XML file by removing the first empty line and a first space in the second
    line. The corrected XML file is valid and can be automatically parsed.

    :param input_xml_path: path of an input XML file
    :param output_xml_path: path of an output, corrected XML file
    """
    xml_lines = text_file.read(input_xml_path)

    # get rid of an extra first line and a starting empty space in the second line
    if xml_lines[:2] == "\n ":
        xml_lines = xml_lines[2:]

    text_file.write(output_xml_path, xml_lines)


def parse_xml_element(element: ET.Element) -> list:
    data_str = str(element.text).replace(";", "").split("\n")
    data = []
    for data_el in data_str:
        if "," in data_el:
            data.append(float(data_el.split(",")[1]))
    return data


def read_index_to_variable_xml_output(
    index_to_variable_xml_output_path: str,
) -> dict:
    path = Path(os.path.dirname(__file__))
    full_path = os.path.join(path, index_to_variable_xml_output_path)
    index_to_variable_xml_output_df = pd.read_csv(full_path, index_col=0)

    return {
        index: row["variable"]
        for index, row in index_to_variable_xml_output_df.iterrows()
    }


def parse_roxie_xml(file_path: str) -> pd.DataFrame:
    """Function parsing a ROXIE XML file and returning a dataframe with strand positions and field values given by id

    :param file_path: a path to a file
    :return: output dataframe with strand positions and field values
    """
    mytree = ET.parse(file_path)
    mytree.getroot().get("x")

    x_values, y_values = _read_x_y_values_from_xml(
        mytree, xml_tree_location="loop/step/loop/step/loop/coilGeom/strands/p"
    )

    x_strands = []
    y_strands = []
    for i in range(0, len(x_values), 4):
        x_strands.append(np.mean(x_values[i : i + 4]))
        y_strands.append(np.mean(y_values[i : i + 4]))

    if not mytree.getroot().findall("loop/step/loop/step/loop/step/coilData"):
        raise IndexError(
            "The XML file does not contain coilData with results. "
            "Please enable plotting in the ROXIE data file"
        )

    data_dct = {X_COORDINATE: x_strands, Y_COORDINATE: y_strands}
    index_to_variable = read_index_to_variable_xml_output(
        "index_to_variable_xml_output.csv"
    )
    for data_element in mytree.getroot().findall(
        "loop/step/loop/step/loop/step/coilData"
    ):
        data = parse_xml_element(data_element)
        index = int(data_element.attrib["id"])
        data_dct[index_to_variable[index]] = data

    return pd.DataFrame(data_dct)


def _read_x_y_values_from_xml(mytree, xml_tree_location=""):
    x_values = []
    y_values = []

    for type_tag in mytree.getroot().findall(xml_tree_location):
        x_value = float(str(type_tag.get("x")))
        y_value = float(str(type_tag.get("y")))
        x_values.append(x_value)
        y_values.append(y_value)

    return x_values, y_values


def read_graph_dfs(
    xml_file_path: str, graph_table_df: pd.DataFrame
) -> List[pd.DataFrame]:
    graphs = read_graphs_as_xy_from_xml(xml_file_path)

    graph_dfs = []
    for index, graph in enumerate(graphs):
        xy = convert_graph_from_text_to_float(graph)
        index_name = concat_name(graph_table_df, index, ["xvalue", "s1x", "s2x"])
        col_name = concat_name(graph_table_df, index, ["yvalue", "s1y", "s2y"])
        graph_df = pd.DataFrame(
            index=pd.Index([xy_el[0] for xy_el in xy], name=index_name),
            data=[xy_el[1] for xy_el in xy],
            columns=[col_name],
        )
        graph_dfs.append(graph_df)

    return graph_dfs


def read_graphs_as_xy_from_xml(file_path):
    mytree = ET.parse(file_path)
    mytree.getroot().get("x")

    return mytree.getroot().findall("loop/step/loop/step/loop/step/graph")


def convert_graph_from_text_to_float(graph):
    xy_lines = graph.text.split(";\n")
    xy_str = [xy_line.strip().split(",") for xy_line in xy_lines[:-1]]
    return [(float(x), float(y)) for x, y in xy_str]


def concat_name(df, index, columns):
    name_segments = df.loc[index, columns].values
    return "_".join([str(name_segment) for name_segment in name_segments])


def read_mesh_data_and_elements(roxie_data_xml_path: str) -> tuple:
    mytree = ET.parse(roxie_data_xml_path)
    mytree.getroot().get("x")

    x_values, y_values = _read_x_y_values_from_xml(
        mytree, "loop/step/loop/step/loop/meshGeom/nodes/p"
    )
    elements = _read_mesh_elements_from_xml(
        mytree, "loop/step/loop/step/loop/meshGeom/elements/fe"
    )
    mesh_data = _read_mesh_data(mytree)

    return (
        pd.concat(
            [pd.DataFrame({X_COORDINATE: x_values, Y_COORDINATE: y_values}), mesh_data],
            axis=1,
        ),
        elements,
    )


def _read_mesh_elements_from_xml(mytree, xml_tree_location):
    elements = []

    for type_tag in mytree.getroot().findall(xml_tree_location):
        element = [int(item[1]) - 1 for item in type_tag.items()]
        elements.append(element)

    return elements


def _read_mesh_data(mytree) -> pd.DataFrame:
    mesh_plot_infos = mytree.getroot().findall("loop/step/loop/step/loop/meshPlotInfo")
    mesh_plot_label_to_id = {
        mesh_plot_info.attrib["id"]: mesh_plot_info.attrib["label"]
        for mesh_plot_info in mesh_plot_infos
    }

    data_values_dct = {}
    for data_element in mytree.getroot().findall(
        "loop/step/loop/step/loop/step/meshData"
    ):
        data_id = data_element.get("id")
        data_values = [float(value.attrib["v"]) for value in data_element.findall("d")]
        data_values_dct[mesh_plot_label_to_id[data_id]] = data_values

    return pd.DataFrame(data_values_dct)
