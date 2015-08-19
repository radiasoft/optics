"""
Implements SRW BeamlineComponent settings.

It is completely up to driver developer to design this object.
The only requirement is that it inherits from AbstractDriverSetting that is initialized with the driver it belongs to.

Although we use only one BeamlineComponent Setting object in this example it is easily possible to use multiple if needed/wished.
One can define a different source setting class for lenses than for apertures. The driver then needs to know if it
processes a lens that its settings object is different from that of an aperature and act accordingly.
"""
from code_drivers.SRW.SRW_driver_setting import SRWDriverSetting


class SRWBeamlineComponentSetting(SRWDriverSetting):
    def __init__(self):
        SRWDriverSetting.__init__(self)

        #***********Wavefront Propagation Parameters:
        #[0]: Auto-Resize (1) or not (0) Before propagation
        #[1]: Auto-Resize (1) or not (0) After propagation
        #[2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
        #[3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
        #[4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
        #[5]: Horizontal Range modification factor at Resizing (1. means no modification)
        #[6]: Horizontal Resolution modification factor at Resizing
        #[7]: Vertical Range modification factor at Resizing
        #[8]: Vertical Resolution modification factor at Resizing
        #[9]: Type of wavefront Shift before Resizing (not yet implemented)
        #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
        #[11]: New Vertical wavefront Center position after Shift (not yet implemented)

        self._auto_resize_before_propagation = True
        self._auto_resize_after_propagation = True
        self._auto_resize_relative_precision = 1.0
        self._allow_semi_analytical_phase_treatment = False
        self._resize_on_ft_side = False
        self._resize_factor_horizontal = 1.0
        self._resize_resolution_horizontal = 1.0
        self._resize_factor_vertical = 1.0
        self._resize_resolution_vertical = 1.0

        self.set_drift_space_settings(None)

    def set_auto_resize_before_propagation(self, auto_resize_before_propagation):
        self._auto_resize_before_propagation = auto_resize_before_propagation

    def set_auto_resize_after_propagation(self, auto_resize_after_propagation):
        self._auto_resize_after_propagation = auto_resize_after_propagation

    def set_auto_resize_relative_precision(self, auto_resize_relative_precision):
        self._auto_resize_relative_precision = auto_resize_relative_precision

    def set_allow_semi_analytical_phase_treatment(self, allow_semi_analytical_phase_treatment):
        self._allow_semi_analytical_phase_treatment = allow_semi_analytical_phase_treatment

    def set_resize_on_ft_side(self, resize_on_ft_side):
        self._resize_on_ft_side = resize_on_ft_side

    def set_resize_factor_horizontal(self, resize_factor_horizontal):
        self._resize_factor_horizontal = resize_factor_horizontal

    def set_resize_resolution_horizontal(self, resize_resolution_horizontal):
        self._resize_resolution_horizontal = resize_resolution_horizontal

    def set_resize_factor_vertical(self, resize_factor_vertical):
        self._resize_factor_vertical = resize_factor_vertical

    def set_resize_resolution_vertical(self, resize_resolution_vertical):
        self._resize_resolution_vertical = resize_resolution_vertical

    def from_list(self, srw_parameter):
        self.set_auto_resize_before_propagation(srw_parameter[0])
        self.set_auto_resize_after_propagation(srw_parameter[1])
        self.set_auto_resize_relative_precision(srw_parameter[2])
        self.set_allow_semi_analytical_phase_treatment(srw_parameter[3])
        self.set_resize_on_ft_side(srw_parameter[4])
        self.set_resize_factor_horizontal(srw_parameter[5])
        self.set_resize_resolution_horizontal(srw_parameter[6])
        self.set_resize_factor_vertical(srw_parameter[7])
        self.set_resize_resolution_vertical(srw_parameter[8])

    def to_list(self):
        srw_parameter = list()

        #[0]: Auto-Resize (1) or not (0) Before propagation
        srw_parameter.append(int(self._auto_resize_before_propagation))
        #[1]: Auto-Resize (1) or not (0) After propagation
        srw_parameter.append(int(self._auto_resize_after_propagation))
        #[2]: Relative Precision for propagation with Auto-Resizing (1. is nominal)
        srw_parameter.append(self._auto_resize_relative_precision)
        #[3]: Allow (1) or not (0) for semi-analytical treatment of the quadratic (leading) phase terms at the propagation
        srw_parameter.append(int(self._allow_semi_analytical_phase_treatment))
        #[4]: Do any Resizing on Fourier side, using FFT, (1) or not (0)
        srw_parameter.append(int(self._resize_on_ft_side))
        #[5]: Horizontal Range modification factor at Resizing (1. means no modification)
        srw_parameter.append(self._resize_factor_horizontal)
        #[6]: Horizontal Resolution modification factor at Resizing
        srw_parameter.append(self._resize_resolution_horizontal)
        #[7]: Vertical Range modification factor at Resizing
        srw_parameter.append(self._resize_factor_vertical)
        #[8]: Vertical Resolution modification factor at Resizing
        srw_parameter.append(self._resize_resolution_vertical)

        #[9]: Type of wavefront Shift before Resizing (not yet implemented)
        srw_parameter.append(0)
        #[10]: New Horizontal wavefront Center position after Shift (not yet implemented)
        srw_parameter.append(0)
        #[11]: New Vertical wavefront Center position after Shift (not yet implemented)
        srw_parameter.append(0)

        return srw_parameter

    def set_drift_space_settings(self, drift_space_settings):
        self._drift_space_settings = drift_space_settings

    def has_drift_space_settings(self):
        has_drift_space_settings = self._drift_space_settings is not None
        return has_drift_space_settings
