import os
from examples.shadow.test.main import run_shadow

def test_shadow():
    shadow_beam = run_shadow()
    rays = shadow_beam._beam.rays

    # Remove shadow files
    os.remove("SRANG")
    os.remove("SRDISTR")
    os.remove("SRSPEC")

    # The rays are random thats why test for ray shape.
    shape_rays = rays.shape
    assert shape_rays == (50000, 18), \
        'Quick test rays shape'
