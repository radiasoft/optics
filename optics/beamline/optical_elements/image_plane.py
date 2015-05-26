__author__ = 'labx'


from optics.beamline.beamline_component import BeamlineComponent


class ImagePlane(BeamlineComponent):
    def __init__(self, name):
        BeamlineComponent.__init__(self, name=name)
