__author__ = 'labx'

import copy, numpy

import Shadow
from optics.driver.abstract_driver_result import AbstractDriverResult

class ShadowOEHistoryItem(object):

    def __init__(self, oe_number=0, shadow_source_start=None, shadow_source_end=None, shadow_oe_start=None, shadow_oe_end=None):
        self._oe_number = oe_number
        self._shadow_source_start = shadow_source_start
        self._shadow_source_end = shadow_source_end
        self._shadow_oe_start = shadow_oe_start
        self._shadow_oe_end = shadow_oe_end

    def duplicate(self):
        return ShadowOEHistoryItem(oe_number=self._oe_number,
                                   shadow_source_start=self._shadow_source_start,
                                   shadow_source_end=self._shadow_source_end,
                                   shadow_oe_start=self._shadow_oe_start,
                                   shadow_oe_end=self._shadow_oe_end)

class ShadowBeam(AbstractDriverResult):
    def __init__(self, oe_number=0, beam=None, number_of_rays=0):
        AbstractDriverResult.__init__(self)

        self._oe_number = oe_number

        if (beam is None):
            if number_of_rays > 0:
                self._beam = Shadow.Beam(number_of_rays)
            else:
                self._beam = Shadow.Beam()
        else:
            self._beam = beam

        self.history = []

    def duplicate(self, copy_rays=True, history=True):
        beam = Shadow.Beam()

        if copy_rays: beam.rays = copy.deepcopy(self._beam.rays)

        new_shadow_beam = ShadowBeam(self._oe_number, beam)

        if history:
            for historyItem in self.history:
                new_shadow_beam.history.append(historyItem)

        return new_shadow_beam

    @classmethod
    def mergeBeams(cls, beam_1, beam_2):
        if beam_1 and beam_2:
            rays_1 = None
            rays_2 = None

            if len(getattr(beam_1._beam, "rays", numpy.zeros(0))) > 0:
                rays_1 = copy.deepcopy(beam_1._beam.rays)
            if len(getattr(beam_2._beam, "rays", numpy.zeros(0))) > 0:
                rays_2 = copy.deepcopy(beam_2._beam.rays)

            merged_beam = beam_1.duplicate(copy_rays=False, history=True)

            if not rays_1 is None and not rays_2 is None:
                merged_beam._oe_number = beam_2._oe_number
                merged_beam._beam.rays = numpy.append(rays_1, rays_2, axis=0)
            elif not rays_1 is None:
                merged_beam._beam.rays = rays_1
                merged_beam._oe_number = beam_2._oe_number
            elif not rays_2 is None:
                merged_beam._beam.rays = rays_2
                merged_beam._oe_number = beam_2._oe_number

            return merged_beam

    @classmethod
    def traceFromSource(cls, shadow_src):
        shadow_beam = ShadowBeam(beam=Shadow.Beam())

        shadow_source_start = shadow_src.duplicate()
        shadow_beam._beam.genSource(shadow_src.toNativeShadowSource())
        shadow_source_end = shadow_src.duplicate()

        shadow_beam.history.append(ShadowOEHistoryItem(shadow_source_start=shadow_source_start, shadow_source_end=shadow_source_end))

        return shadow_beam

    @classmethod
    def traceFromOE(cls, shadow_oe, input_beam):
        shadow_beam = cls.initializeFromPreviousBeam(input_beam)

        history_shadow_oe_start = shadow_oe.duplicate()
        shadow_beam._beam.traceOE(shadow_oe.toNativeShadowOE(), shadow_beam._oe_number)
        history_shadow_oe_end = shadow_oe.duplicate()

        #N.B. history[0] = Source
        if not shadow_beam._oe_number == 0:
            if len(shadow_beam.history) - 1 < shadow_beam._oe_number:
                shadow_beam.history.append(ShadowOEHistoryItem(oe_number=shadow_beam._oe_number,
                                                        shadow_oe_start=history_shadow_oe_start,
                                                        shadow_oe_end=history_shadow_oe_end))
            else:
                shadow_beam.history[shadow_beam._oe_number]=ShadowOEHistoryItem(oe_number=shadow_beam._oe_number,
                                                                  shadow_oe_start=history_shadow_oe_start,
                                                                  shadow_oe_end=history_shadow_oe_end)

        return shadow_beam

    @classmethod
    def initializeFromPreviousBeam(cls, input_beam):
        shadow_beam = input_beam.duplicate()
        shadow_beam._oe_number = input_beam._oe_number + 1

        return shadow_beam

    @classmethod
    def traceFromOENoHistory(cls, input_beam, shadow_oe):
        shadow_beam = cls.initializeFromPreviousBeam(input_beam)
        shadow_beam._beam.traceOE(shadow_oe.toNativeShadowOE(), shadow_beam._oe_number)

        return shadow_beam

    def getOEHistory(self, oe_number=None):
        if oe_number is None:
            return self.history
        else:
            return self.history[oe_number-1]
