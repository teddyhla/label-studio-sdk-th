import math
import os
import shutil
import tempfile

import numpy as np
import pytest

from label_studio_sdk.converter import Converter
from label_studio_sdk.converter.utils import (
    convert_annotation_to_yolo,
    convert_annotation_to_yolo_obb,
    convert_yolo_obb_to_annotation,
)
from .utils import almost_equal_1d, almost_equal_2d, get_os_walk, check_equal_list_of_strings

BASE_DIR = os.path.dirname(__file__)
TEST_DATA_PATH = os.path.join(BASE_DIR, "data", "test_export_yolo")
INPUT_JSON_PATH = os.path.join(BASE_DIR, TEST_DATA_PATH, "data.json")
INPUT_JSON_OBB_PATH = os.path.join(BASE_DIR, TEST_DATA_PATH, "data_obb.json")
LABEL_CONFIG_PATH = os.path.join(BASE_DIR, TEST_DATA_PATH, "label_config.xml")
LABEL_CONFIG_OBB_PATH = os.path.join(BASE_DIR, TEST_DATA_PATH, "label_config_obb.xml")
INPUT_JSON_PATH_POLYGONS = os.path.join(BASE_DIR, TEST_DATA_PATH, "data_polygons.json")
LABEL_CONFIG_PATH_POLYGONS = os.path.join(
    BASE_DIR, TEST_DATA_PATH, "label_config_polygons.xml"
)


@pytest.fixture
def create_temp_folder():
    # Create a temporary folder
    temp_dir = tempfile.mkdtemp()

    # Yield the temporary folder
    yield temp_dir

    # Remove the temporary folder after the test
    shutil.rmtree(temp_dir)


def test_convert_to_yolo(create_temp_folder):
    """Check converstion label_studio json exported file to yolo with multiple labelers"""

    # Generates a temporary folder and return the absolute path
    # The temporary folder contains all the data generate by the following function
    # For debugging replace create_temp_folder with "./tmp"
    tmp_folder = create_temp_folder

    output_dir = tmp_folder
    output_image_dir = os.path.join(output_dir, "tmp_image")
    output_label_dir = os.path.join(output_dir, "tmp_label")
    project_dir = "."

    converter = Converter(LABEL_CONFIG_PATH, project_dir)
    converter.convert_to_yolo(
        INPUT_JSON_PATH,
        output_dir,
        output_image_dir=output_image_dir,
        output_label_dir=output_label_dir,
        is_dir=False,
        split_labelers=True,
    )

    abs_path_label_dir = os.path.abspath(output_label_dir)
    expected_paths = [
        os.path.join(abs_path_label_dir, "1", "image1.txt"),
        os.path.join(abs_path_label_dir, "1", "image2.txt"),
        os.path.join(abs_path_label_dir, "2", "image1.txt"),
    ]
    generated_paths = get_os_walk(abs_path_label_dir)
    # Check all files and subfolders have been generated.
    assert check_equal_list_of_strings(
        expected_paths, generated_paths
    ), f"Generated file: \n  {generated_paths} \n does not match expected ones: \n {expected_paths}"
    # Check all the annotations have been converted to yolo
    for file in expected_paths:
        with open(file) as f:
            lines = f.readlines()
            assert (
                len(lines) == 2
            ), f"Expect different number of annotations in file {file}."


def test_convert_to_yolo_obb(create_temp_folder):
    """Check conversion label_studio json exported file to a yolo obb compatible format"""

    # Generates a temporary folder and return the absolute path
    # The temporary folder contains all the data generate by the following function
    # For debugging replace create_temp_folder with "./tmp"
    tmp_folder = create_temp_folder

    output_dir = tmp_folder
    output_image_dir = os.path.join(output_dir, "tmp_image")
    output_label_dir = os.path.join(output_dir, "tmp_label")
    project_dir = "."

    converter = Converter(LABEL_CONFIG_OBB_PATH, project_dir)
    converter.convert_to_yolo(
        INPUT_JSON_OBB_PATH,
        output_dir,
        output_image_dir=output_image_dir,
        output_label_dir=output_label_dir,
        is_dir=False,
        split_labelers=False,
        is_obb=True,
    )

    abs_path_label_dir = os.path.abspath(output_label_dir)
    expected_paths = [
        os.path.join(abs_path_label_dir, "image1.txt"),
        os.path.join(abs_path_label_dir, "image2.txt"),
        os.path.join(abs_path_label_dir, "image3.txt"),
    ]
    generated_paths = get_os_walk(abs_path_label_dir)
    # Check all files and subfolders have been generated.
    assert check_equal_list_of_strings(
        expected_paths, generated_paths
    ), f"Generated file: \n  {generated_paths} \n does not match expected ones: \n {expected_paths}"

    # Check all the annotations have been converted to yolo
    expected_annotations = [23, 1, 1]
    for fidx, file in enumerate(expected_paths):
        with open(file) as f:
            lines = f.readlines()
            assert (
                len(lines) == expected_annotations[fidx]
            ), f"Expect different number of annotations in file {file}."
            for idx, line in enumerate(lines):
                parameters = line.split(" ")
                total_parameters = len(parameters)
                assert (
                    total_parameters == 9
                ), f"Expected 9 parameters but got {total_parameters} in line {idx}"


def test_convert_polygons_to_yolo(create_temp_folder):
    """Check conversion label_studio json exported file to yolo with polygons"""

    # Generates a temporary folder and return the absolute path
    # The temporary folder contains all the data generate by the following function
    # For debugging replace create_temp_folder with "./tmp"
    tmp_folder = create_temp_folder

    output_dir = tmp_folder
    output_image_dir = os.path.join(output_dir, "tmp_image")
    output_label_dir = os.path.join(output_dir, "tmp_label")
    project_dir = "."

    converter = Converter(LABEL_CONFIG_PATH_POLYGONS, project_dir)
    converter.convert_to_yolo(
        INPUT_JSON_PATH_POLYGONS,
        output_dir,
        output_image_dir=output_image_dir,
        output_label_dir=output_label_dir,
        is_dir=False,
        split_labelers=False,
    )

    abs_path_label_dir = os.path.abspath(output_label_dir)
    expected_paths = [os.path.join(abs_path_label_dir, "image2.txt")]
    generated_paths = get_os_walk(abs_path_label_dir)
    # Check all files and subfolders have been generated.
    assert check_equal_list_of_strings(
        expected_paths, generated_paths
    ), f"Generated file: \n  {generated_paths} \n does not match expected ones: \n {expected_paths}"
    # Check all the annotations have been converted to yolo
    for file in expected_paths:
        with open(file) as f:
            lines = f.readlines()
            assert (
                len(lines) == 1
            ), f"Expect different number of annotations in file {file}."


def test_convert_annotation_to_yolo_format():
    """
    Verify conversion from LS annotation to normalized Yolo format.

    This test case evaluates the conversion of LS (Label Studio) annotations to normalized
    Yolo format. It iterates over a list of LS annotations and compares the result of the
    conversion to expected values.

    Test Procedure:
    1. Define LS annotations and their corresponding expected Yolo representations.
    2. Iterate over each LS annotation and perform the conversion.
    3. Compare the result to the expected Yolo format.
    """

    annotations = [
        {
            "x": 37.15846994535519,
            "y": 70.67395264116576,
            "width": 4.189435336976321,
            "height": 4.735883424408015,
        },
        {
            "x": 57.79102500413977,
            "y": 62.87464812054977,
            "width": 3.808577579069383,
            "height": 4.636529226693169,
        },
        {
            "x": 37.88706739526412,
            "y": 71.76684881602914,
            "width": 3.8251366120218573,
            "height": 4.553734061930784,
        },
    ]

    expectations = [
        (
            0.39253187613843354,
            0.7304189435336975,
            0.04189435336976321,
            0.04735883424408015,
        ),
        (
            0.5969531379367445,
            0.6519291273389635,
            0.03808577579069383,
            0.04636529226693169,
        ),
        (
            0.39799635701275043,
            0.7404371584699453,
            0.03825136612021857,
            0.04553734061930784,
        ),
    ]

    for idx, annotation in enumerate(annotations):
        result = convert_annotation_to_yolo(annotation)
        assert almost_equal_1d(
            result, expectations[idx]
        ), f"Converted LS annotation to normalized Yolo format does not match expected result at index {idx}"


def test_convert_invalid_annotation_to_yolo_format():
    """
    Verify conversion of incomplete or empty annotations to Yolo format.

    This test case evaluates the conversion of incomplete or empty annotations to Yolo format.
    It iterates over a list of annotations with missing keys or an empty dictionary and checks
    whether the function `convert_annotation_to_yolo` returns None for each invalid annotation.

    Test Procedure:
    1. Define a list of incomplete or empty annotations.
    2. Iterate over each annotation and call the conversion function.
    3. Verify that the function returns None for each invalid annotation.
    """
    annotations = [
        {
            "y": 70.67395264116576,
            "width": 4.189435336976321,
            "height": 4.735883424408015,
        },
        {
            "x": 57.79102500413977,
            "width": 3.808577579069383,
            "height": 4.636529226693169,
        },
        {"x": 37.88706739526412, "y": 71.76684881602914, "height": 4.553734061930784},
        {
            "x": 37.88706739526412,
            "y": 71.76684881602914,
            "width": 3.8251366120218573,
        },
        {
            # empty dict
        },
    ]

    for idx, annotation in enumerate(annotations):
        result = convert_annotation_to_yolo(annotation)
        assert result is None, f"Expected annotation at index {idx} to be invalid"


def test_convert_annotation_to_yolo_obb_format():
    """
    Verify conversion from LS annotation to normalized Yolo OBB format.

    This test case evaluates the conversion of LS (Label Studio) annotations to normalized
    Yolo Oriented Bounding Box (OBB) format. It iterates over a list of LS annotations and
    compares the result of the conversion to expected values.

    Test Procedure:
    1. Define LS annotations and their corresponding expected Yolo OBB representations.
    2. Iterate over each LS annotation and perform the conversion.
    3. Compare the result to the expected Yolo OBB format.
    """

    annotations = [
        {
            "original_width": 597,
            "original_height": 768,
            "x": 11.552474514692952,
            "y": 80.83731446979957,
            "width": 19.0454700246567,
            "height": 6.629026203797071,
            "rotation": 328.33240366032836,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "x": 32.94000909818857,
            "y": 77.3890916826675,
            "width": 8.108689897439085,
            "height": 7.490685233798283,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "x": 16.814074232397514,
            "y": 57.43596079245723,
            "width": 18.218991060518677,
            "height": 6.298347014251024,
            "rotation": 43.67748910099408,
        },
    ]

    expectations = [
        [
            (0.11552474514692952, 0.8083731446979957),  # top left
            (0.27762229351938456, 0.7306489626734597),  # top right
            (0.3223923846720476, 0.7870691452334665),  # bottom right
            (0.16029483629959254, 0.8647933272580025),  # bottom left
        ],
        [
            (0.32940009098188566, 0.7738909168266751),  # top left
            (0.4078648636432219, 0.7579911558782483),  # top right
            (0.43217208011269465, 0.830475727539231),  # bottom right
            (0.35370730745135837, 0.8463754884876579),  # bottom left
        ],
        [
            (0.16814074232397513, 0.5743596079245723),  # top left
            (0.29990750552628187, 0.6721650332758418),  # top right
            (0.24395249444460837, 0.7177171056620688),  # bottom right
            (0.11218573124230163, 0.6199116803107994),  # bottom left
        ],
    ]

    for idx, annotation in enumerate(annotations):
        result = convert_annotation_to_yolo_obb(annotation)
        print("result = ", result)
        assert almost_equal_2d(
            result, expectations[idx]
        ), f"Converted LS annotation to normalized Yolo OBB-format does not match expected result at index {idx}"


def test_convert_invalid_annotation_to_yolo_obb_format():
    """
    Verify conversion of incomplete or empty annotations.

    This test iterates over incomplete or empty annotations to simulate invalid input scenarios.
    It checks if `convert_annotation_to_yolo_obb` returns None for each invalid annotation.

    Annotations include cases with missing keys and an empty annotation.

    Test Procedure:
    1. Define incomplete or empty annotations.
    2. Iterate over each annotation and call the conversion function.
    3. Verify the function returns None for each invalid annotation.
    """

    # Annotations with missing keys to simulate invalid annotations...
    annotations = [
        {
            "original_height": 768,
            "x": 16.814074232397514,
            "y": 57.43596079245723,
            "width": 18.218991060518677,
            "height": 6.298347014251024,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "x": 16.814074232397514,
            "y": 57.43596079245723,
            "width": 18.218991060518677,
            "height": 6.298347014251024,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "y": 57.43596079245723,
            "width": 18.218991060518677,
            "height": 6.298347014251024,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "x": 16.814074232397514,
            "width": 18.218991060518677,
            "height": 6.298347014251024,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "x": 16.814074232397514,
            "y": 57.43596079245723,
            "height": 6.298347014251024,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "x": 16.814074232397514,
            "y": 57.43596079245723,
            "width": 18.218991060518677,
            "rotation": 345.3894551068102,
        },
        {
            "original_width": 597,
            "original_height": 768,
            "x": 16.814074232397514,
            "y": 57.43596079245723,
            "width": 18.218991060518677,
            "height": 6.298347014251024,
        },
        {
            # empty annotation
        },
    ]

    for idx, annotation in enumerate(annotations):
        result = convert_annotation_to_yolo_obb(annotation)
        assert (
            result is None
        ), f"Expected annotation for OBB at index {idx} to be invalid"


def test_annotation_to_yolo_obb_and_back():
    label_data = {
        "original_width": 1024,
        "original_height": 768,
        "x": 40.0,
        "y": 30.0,
        "width": 20.0,
        "height": 10.0,
        "rotation": 45.0,
    }

    yolo_obb = convert_annotation_to_yolo_obb(label_data, normalize=False)

    label_converted_back = convert_yolo_obb_to_annotation(
        [coord for point in yolo_obb for coord in point],
        label_data["original_width"],
        label_data["original_height"],
    )

    return (
        math.isclose(label_data["x"], label_converted_back["x"], rel_tol=1e-5),
        math.isclose(label_data["y"], label_converted_back["y"], rel_tol=1e-5),
        math.isclose(label_data["width"], label_converted_back["width"], rel_tol=1e-5),
        math.isclose(
            label_data["height"], label_converted_back["height"], rel_tol=1e-5
        ),
        math.isclose(
            label_data["rotation"], label_converted_back["rotation"], rel_tol=1e-5
        ),
    )


def test_yolo_obb_to_annotation_to_yolo():
    inv_data = [
        10,
        20,
        39.54423259036624,
        26.511806662509885,
        33.98749090502447,
        65.9041167829982,
        4.443258314658229,
        59.39231012048832,
    ]
    original_width = 10
    original_height = 10

    annotation_data = convert_yolo_obb_to_annotation(
        inv_data, original_width, original_height
    )
    yolo_data = convert_annotation_to_yolo_obb(annotation_data, normalize=False)

    assert np.allclose(
        yolo_data, np.array(inv_data).reshape((4, 2)), rtol=1, atol=1  # 1 pixel tolerance
    ), f"Test failed: {yolo_data} != {inv_data}"
