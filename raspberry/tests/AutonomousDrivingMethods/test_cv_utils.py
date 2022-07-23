import pytest
from AutonomousDrivingMethods.cv_utils import get_steer_value_from_image_center


@pytest.mark.parametrize(("position", "image_width", "expected_value"),
    [
        (0, 320, 0),
        (-80, 320, -64),
        (-160, 320, -128),
        (80, 320, 64),
        (160, 320, 128),
        (-180, 320, -128),
        (180, 320, 128)
    ])
def test_get_steer_value_from_image_center(position, image_width, expected_value):
    assert get_steer_value_from_image_center(position, image_width) == expected_value
