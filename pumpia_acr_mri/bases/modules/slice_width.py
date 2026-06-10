"""
Slice width for Medium ACR Phantom
"""
import math
from collections.abc import Callable
import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

from pumpia.module_handling.modules import PhantomModule
from pumpia.module_handling.fields.roi_fields import RectangleROIField
from pumpia.module_handling.fields.viewer_fields import MonochromeDicomViewerField
from pumpia.module_handling.fields.simple import (PercField,
                                                  FloatField,
                                                  StringField,
                                                  OptionField,
                                                  BoolField)
from pumpia.image_handling.roi_structures import RectangleROI
from pumpia.file_handling.dicom_structures import Series, Instance
from pumpia.utilities.array_utils import nth_max_widest_peak
from pumpia.utilities.feature_utils import flat_top_gauss, split_gauss

from pumpia_acr_mri.bases.acr_mri_context import ACRMRIContextManager, ACRMRIContext

# ROI sizes in mm
ROI_HEIGHT = 2
ROI_WIDTH = 150
BOTTOM_OFFSET = 1
TOP_OFFSET = -3.5
BOTTOM_UNI_OFFSET = 8.5
TOP_UNI_OFFSET = -10

fit_options: dict[str, Callable] = {"Flat Top Gaussian": flat_top_gauss,
                                    "Split Gaussian": split_gauss}


class ACRMRISliceWidth(PhantomModule):
    """
    Calculates slice width for the ACR MRI phantom by fitting to a flat top gaussian.

    Overall slice width is calculated by taking the geometric mean
    of the top and bottom ramp widths.
    """
    context_manager: ACRMRIContextManager
    show_draw_rois_button = True
    show_analyse_button = True
    title = "Slice Width"

    viewer = MonochromeDicomViewerField(row=0, column=0)

    tan_theta = FloatField(0.1, verbose_name="Tan of ramp angle")
    max_perc = PercField(50, verbose_name="Height for peak finding (% of max)")
    width_def = PercField(50, verbose_name="Result width position (% of max)")
    fit_type = OptionField(fit_options, "Flat Top Gaussian")
    uniformity_correct = BoolField()

    ramp_dir = StringField(verbose_name="Ramp Direction", read_only=True)

    expected_width = FloatField(verbose_name="Expected Width (mm)",
                                reset_on_analysis=True,
                                read_only=True)
    top_ramp_width = FloatField(verbose_name="Top Ramp Width (mm)",
                                reset_on_analysis=True,
                                read_only=True)
    bottom_ramp_width = FloatField(verbose_name="Bottom Ramp Width (mm)",
                                   reset_on_analysis=True,
                                   read_only=True)
    slice_width = FloatField(verbose_name="Slice Width (mm)",
                             reset_on_analysis=True,
                             read_only=True)

    top_ramp = RectangleROIField()
    bottom_ramp = RectangleROIField()
    top_uniformity = RectangleROIField()
    bottom_uniformity = RectangleROIField()

    def draw_rois(self, context: ACRMRIContext, batch: bool = False) -> None:

        if isinstance(self.viewer.image, Instance):
            image = self.viewer.image
        elif isinstance(self.viewer.image, Series):
            if context.inserts_slice == 10:
                image = self.viewer.image.instances[10]
            else:
                image = self.viewer.image.instances[0]
        else:
            return

        pixel_size = image.pixel_spacing
        if pixel_size is None:
            return
        pixel_height = pixel_size[0]
        pixel_width = pixel_size[1]

        slice_thickness = self.viewer.image.slice_thickness
        if slice_thickness is None:
            return
        self.expected_width = slice_thickness

        if context.res_insert_side == "bottom" or context.res_insert_side == "top":
            self.ramp_dir = "Horizontal"
            box_height = ROI_HEIGHT / pixel_height
            box_width = ROI_WIDTH / pixel_width
            top_pix_offset = TOP_OFFSET / pixel_height
            bottom_pix_offset = BOTTOM_OFFSET / pixel_height
            top_uni_pix_offset = TOP_UNI_OFFSET / pixel_height
            bottom_uni_pix_offset = BOTTOM_UNI_OFFSET / pixel_height

            top_xmin = bottom_xmin = round(context.xcent - box_width / 2)
            top_xmax = bottom_xmax = round(context.xcent + box_width / 2)
            top_uni_xmin = bottom_uni_xmin = round(context.xcent - box_width / 2)
            top_uni_xmax = bottom_uni_xmax = round(context.xcent + box_width / 2)

            if context.res_insert_side == "bottom":
                top_ymin = round(context.ycent + top_pix_offset)
                top_ymax = round(context.ycent + top_pix_offset + box_height)
                bottom_ymin = round(context.ycent + bottom_pix_offset)
                bottom_ymax = round(context.ycent + bottom_pix_offset + box_height)
                top_uni_ymin = round(context.ycent + top_uni_pix_offset)
                top_uni_ymax = round(context.ycent + top_uni_pix_offset + box_height)
                bottom_uni_ymin = round(context.ycent + bottom_uni_pix_offset)
                bottom_uni_ymax = round(context.ycent + bottom_uni_pix_offset + box_height)
            else:
                top_ymin = round(context.ycent - top_pix_offset - box_height)
                top_ymax = round(context.ycent - top_pix_offset)
                bottom_ymin = round(context.ycent - bottom_pix_offset - box_height)
                bottom_ymax = round(context.ycent - bottom_pix_offset)
                top_uni_ymin = round(context.ycent - top_uni_pix_offset - box_height)
                top_uni_ymax = round(context.ycent - top_uni_pix_offset)
                bottom_uni_ymin = round(context.ycent - bottom_uni_pix_offset - box_height)
                bottom_uni_ymax = round(context.ycent - bottom_uni_pix_offset)
        else:
            self.ramp_dir = "Vertical"
            box_height = ROI_HEIGHT / pixel_width
            box_width = ROI_WIDTH / pixel_height
            top_pix_offset = TOP_OFFSET / pixel_width
            bottom_pix_offset = BOTTOM_OFFSET / pixel_width
            top_uni_pix_offset = TOP_UNI_OFFSET / pixel_width
            bottom_uni_pix_offset = BOTTOM_UNI_OFFSET / pixel_width

            top_ymin = bottom_ymin = round(context.ycent - box_width / 2)
            top_ymax = bottom_ymax = round(context.ycent + box_width / 2)
            top_uni_ymin = bottom_uni_ymin = round(context.ycent - box_width / 2)
            top_uni_ymax = bottom_uni_ymax = round(context.ycent + box_width / 2)

            if context.res_insert_side == "right":
                top_xmin = round(context.xcent + top_pix_offset)
                top_xmax = round(context.xcent + top_pix_offset + box_height)
                bottom_xmin = round(context.xcent + bottom_pix_offset)
                bottom_xmax = round(context.xcent + bottom_pix_offset + box_height)
                top_uni_xmin = round(context.xcent + top_uni_pix_offset)
                top_uni_xmax = round(context.xcent + top_uni_pix_offset + box_height)
                bottom_uni_xmin = round(context.xcent + bottom_uni_pix_offset)
                bottom_uni_xmax = round(context.xcent + bottom_uni_pix_offset + box_height)
            else:
                top_xmin = round(context.xcent - top_pix_offset - box_height)
                top_xmax = round(context.xcent - top_pix_offset)
                bottom_xmin = round(context.xcent - bottom_pix_offset - box_height)
                bottom_xmax = round(context.xcent - bottom_pix_offset)
                top_uni_xmin = round(context.xcent - top_uni_pix_offset - box_height)
                top_uni_xmax = round(context.xcent - top_uni_pix_offset)
                bottom_uni_xmin = round(context.xcent - bottom_uni_pix_offset - box_height)
                bottom_uni_xmax = round(context.xcent - bottom_uni_pix_offset)

        top_roi = RectangleROI(image,
                               top_xmin,
                               top_ymin,
                               top_xmax - top_xmin,
                               top_ymax - top_ymin,
                               slice_num=image.current_slice,
                               replace=True)
        self.top_ramp.register_roi(top_roi)

        bottom_roi = RectangleROI(image,
                                  bottom_xmin,
                                  bottom_ymin,
                                  bottom_xmax - bottom_xmin,
                                  bottom_ymax - bottom_ymin,
                                  slice_num=image.current_slice,
                                  replace=True)
        self.bottom_ramp.register_roi(bottom_roi)

        top_uni_roi = RectangleROI(image,
                                   top_uni_xmin,
                                   top_uni_ymin,
                                   top_uni_xmax - top_uni_xmin,
                                   top_uni_ymax - top_uni_ymin,
                                   slice_num=image.current_slice,
                                   replace=True)
        self.top_uniformity.register_roi(top_uni_roi)

        bottom_uni_roi = RectangleROI(image,
                                      bottom_uni_xmin,
                                      bottom_uni_ymin,
                                      bottom_uni_xmax - bottom_uni_xmin,
                                      bottom_uni_ymax - bottom_uni_ymin,
                                      slice_num=image.current_slice,
                                      replace=True)
        self.bottom_uniformity.register_roi(bottom_uni_roi)

    def post_roi_register(self, roi_input: RectangleROIField):
        if (roi_input.roi is not None
            and self.manager is not None
                and (roi_input is self.top_ramp
                     or roi_input is self.bottom_ramp
                     or roi_input is self.bottom_uniformity
                     or roi_input is self.top_uniformity)):
            self.manager.add_roi(roi_input.roi)

    def analyse(self, batch: bool = False):
        if (self.top_ramp.roi is not None
            and self.bottom_ramp.roi is not None
            and self.bottom_uniformity.roi is not None
            and self.top_uniformity.roi is not None
                and self.viewer.image is not None):
            pixel_spacing = self.viewer.image.pixel_spacing
            if pixel_spacing is None:
                return
            if self.ramp_dir[0].lower() == "v":
                top_prof = self.top_ramp.roi.v_profile
                bottom_prof = self.bottom_ramp.roi.v_profile
                top_uni_prof = self.top_uniformity.roi.v_profile
                bottom_uni_prof = self.bottom_uniformity.roi.v_profile
                pix_size = pixel_spacing[0]
            else:
                top_prof = self.top_ramp.roi.h_profile
                bottom_prof = self.bottom_ramp.roi.h_profile
                top_uni_prof = self.top_uniformity.roi.h_profile
                bottom_uni_prof = self.bottom_uniformity.roi.h_profile
                pix_size = pixel_spacing[1]

            if self.uniformity_correct:
                top_uni_prof = top_uni_prof / np.max(top_uni_prof)
                bottom_uni_prof = bottom_uni_prof / np.max(bottom_uni_prof)
                # avg_uni_prof = (top_uni_prof + bottom_uni_prof) / 2
                top_prof = top_prof / top_uni_prof
                bottom_prof = bottom_prof / bottom_uni_prof

            slice_thickness = self.viewer.image.slice_thickness
            if slice_thickness is None:
                return
            self.expected_width = slice_thickness

            if self.fit_type is split_gauss:
                # reciprocal would require a negative in c_coeff
                divisor = 100 / self.max_perc
                width_divisor = 100 / self.width_def
                c_coeff = math.sqrt(2 * math.log(width_divisor))

                top_fwhm_peak = nth_max_widest_peak(top_prof, divisor)
                bottom_fwhm_peak = nth_max_widest_peak(bottom_prof, divisor)
                bounds = ([0, 0, 0, -np.inf, -np.inf],
                          [np.inf, np.inf, np.inf, np.inf, np.inf])

                top_init = (top_fwhm_peak.minimum,
                            top_fwhm_peak.maximum,
                            (top_fwhm_peak.maximum - top_fwhm_peak.minimum) / 4,
                            np.max(top_prof) - np.min(top_prof),
                            np.min(top_prof))
                top_indeces = np.indices(top_prof.shape)[0]
                top_fit, _ = curve_fit(split_gauss,
                                       top_indeces,
                                       top_prof,
                                       top_init,
                                       bounds=bounds)
                top_fwhm = abs(top_fit[1] - top_fit[0]) + (2 * c_coeff * top_fit[2])

                bottom_init = (bottom_fwhm_peak.minimum,
                               bottom_fwhm_peak.maximum,
                               (bottom_fwhm_peak.maximum - bottom_fwhm_peak.minimum) / 4,
                               np.max(bottom_prof) - np.min(bottom_prof),
                               np.min(bottom_prof))
                bottom_indeces = np.indices(bottom_prof.shape)[0]
                bottom_fit, _ = curve_fit(split_gauss,
                                          bottom_indeces,
                                          bottom_prof,
                                          bottom_init,
                                          bounds=bounds)
                bottom_fwhm = abs(bottom_fit[1] - bottom_fit[0]) + (2 * c_coeff * bottom_fit[2])

                tan_theta = self.tan_theta

                top_width = top_fwhm * tan_theta * pix_size
                bottom_width = bottom_fwhm * tan_theta * pix_size

                self.top_ramp_width = top_width
                self.bottom_ramp_width = bottom_width

                self.slice_width = math.sqrt(top_width * bottom_width)

            else:
                # reciprocal would require a negative in coeffs
                divisor = 100 / self.max_perc
                width_divisor = 100 / self.width_def

                top_fwhm_peak = nth_max_widest_peak(top_prof, divisor)
                bottom_fwhm_peak = nth_max_widest_peak(bottom_prof, divisor)
                bounds = ([0, 0, -np.inf, 0, -np.inf],
                          [np.inf, np.inf, np.inf, np.inf, np.inf])

                top_init = ((top_fwhm_peak.maximum + top_fwhm_peak.minimum) / 2,
                            (top_fwhm_peak.maximum - top_fwhm_peak.minimum) / 2,
                            np.max(top_prof) - np.min(top_prof),
                            1,
                            np.min(top_prof))
                top_indeces = np.indices(top_prof.shape)[0]
                top_fit, _ = curve_fit(flat_top_gauss,
                                       top_indeces,
                                       top_prof,
                                       top_init,
                                       bounds=bounds)
                top_coeff = math.sqrt(2 * math.pow(math.log(width_divisor), 1 / top_fit[3]))
                top_fwhm = 2 * top_coeff * top_fit[1]

                bottom_init = ((bottom_fwhm_peak.maximum + bottom_fwhm_peak.minimum) / 2,
                               (bottom_fwhm_peak.maximum - bottom_fwhm_peak.minimum) / 2,
                               np.max(bottom_prof) - np.min(bottom_prof),
                               1,
                               np.min(bottom_prof))
                bottom_indeces = np.indices(bottom_prof.shape)[0]
                bottom_fit, _ = curve_fit(flat_top_gauss,
                                          bottom_indeces,
                                          bottom_prof,
                                          bottom_init,
                                          bounds=bounds)
                bottom_coeff = math.sqrt(2 * math.pow(math.log(width_divisor), 1 / bottom_fit[3]))
                bottom_fwhm = 2 * bottom_coeff * bottom_fit[1]

                tan_theta = self.tan_theta

                top_width = abs(top_fwhm * tan_theta * pix_size)
                bottom_width = abs(bottom_fwhm * tan_theta * pix_size)

                self.top_ramp_width = top_width
                self.bottom_ramp_width = bottom_width

                self.slice_width = math.sqrt(top_width * bottom_width)

    def load_commands(self):
        self.register_command("Show Profiles", self.show_profiles)

    def show_profiles(self):
        """
        Shows the ROI profiles
        """
        if (self.top_ramp.roi is not None
            and self.bottom_ramp.roi is not None
            and self.bottom_uniformity.roi is not None
            and self.top_uniformity.roi is not None
                and self.viewer.image is not None):
            pixel_spacing = self.viewer.image.pixel_spacing
            if pixel_spacing is None:
                return
            if self.ramp_dir[0].lower() == "v":
                top_prof = self.top_ramp.roi.v_profile
                bottom_prof = self.bottom_ramp.roi.v_profile
                top_uni_prof = self.top_uniformity.roi.v_profile
                bottom_uni_prof = self.bottom_uniformity.roi.v_profile
                pix_size = pixel_spacing[0]
            else:
                top_prof = self.top_ramp.roi.h_profile
                bottom_prof = self.bottom_ramp.roi.h_profile
                top_uni_prof = self.top_uniformity.roi.h_profile
                bottom_uni_prof = self.bottom_uniformity.roi.h_profile
                pix_size = pixel_spacing[1]

            if self.uniformity_correct:
                top_uni_prof = top_uni_prof / np.max(top_uni_prof)
                bottom_uni_prof = bottom_uni_prof / np.max(bottom_uni_prof)
                # avg_uni_prof = (top_uni_prof + bottom_uni_prof) / 2
                top_prof = top_prof / top_uni_prof
                bottom_prof = bottom_prof / bottom_uni_prof

            tan_theta = self.tan_theta

            divisor = 100 / self.max_perc

            top_indeces = np.indices(top_prof.shape)[0]
            bottom_indeces = np.indices(bottom_prof.shape)[0]
            top_x_locs = top_indeces * tan_theta * pix_size
            bottom_x_locs = bottom_indeces * tan_theta * pix_size

            plt.clf()

            if self.fit_type is split_gauss:
                plt.plot(top_x_locs, top_prof, label="Top Profile")

                bounds = ([0, 0, 0, -np.inf, -np.inf],
                          [np.inf, np.inf, np.inf, np.inf, np.inf])

                try:
                    top_fwhm_peak = nth_max_widest_peak(top_prof, divisor)
                    top_init = (top_fwhm_peak.minimum,
                                top_fwhm_peak.maximum,
                                (top_fwhm_peak.maximum - top_fwhm_peak.minimum) / 4,
                                np.max(top_prof) - np.min(top_prof),
                                np.min(top_prof))

                    top_fit, _ = curve_fit(split_gauss,
                                           top_indeces,
                                           top_prof,
                                           top_init,
                                           bounds=bounds)

                    top_fitted = split_gauss(top_indeces, *top_fit)
                    plt.plot(top_x_locs, top_fitted,
                             label="Top Fit")

                except RuntimeError:
                    pass

                plt.plot(bottom_x_locs, bottom_prof, label="Bottom Profile")

                try:
                    bottom_fwhm_peak = nth_max_widest_peak(bottom_prof, divisor)
                    bottom_init = (bottom_fwhm_peak.minimum,
                                   bottom_fwhm_peak.maximum,
                                   (bottom_fwhm_peak.maximum - bottom_fwhm_peak.minimum) / 4,
                                   np.max(bottom_prof) - np.min(bottom_prof),
                                   np.min(bottom_prof))

                    bottom_fit, _ = curve_fit(split_gauss,
                                              bottom_indeces,
                                              bottom_prof,
                                              bottom_init,
                                              bounds=bounds)
                    bottom_fitted = split_gauss(bottom_indeces, *bottom_fit)
                    plt.plot(bottom_x_locs, bottom_fitted,
                             label="Bottom Fit")
                except RuntimeError:
                    pass

            else:
                plt.plot(top_x_locs, top_prof, label="Top Profile")

                bounds = ([0, 0, -np.inf, 0, -np.inf],
                          [np.inf, np.inf, np.inf, np.inf, np.inf])

                try:
                    top_fwhm_peak = nth_max_widest_peak(top_prof, divisor)
                    bottom_fwhm_peak = nth_max_widest_peak(bottom_prof, divisor)

                    top_init = ((top_fwhm_peak.maximum + top_fwhm_peak.minimum) / 2,
                                (top_fwhm_peak.maximum - top_fwhm_peak.minimum) / 2,
                                np.max(top_prof) - np.min(top_prof),
                                1,
                                np.min(top_prof))
                    top_indeces = np.indices(top_prof.shape)[0]
                    top_fit, _ = curve_fit(flat_top_gauss,
                                           top_indeces,
                                           top_prof,
                                           top_init,
                                           bounds=bounds)
                    top_fitted = flat_top_gauss(top_indeces, *top_fit)
                    plt.plot(top_x_locs, top_fitted,
                             label="Top Fit")
                except RuntimeError:
                    pass

                plt.plot(bottom_x_locs, bottom_prof, label="Bottom Profile")

                try:
                    bottom_init = ((bottom_fwhm_peak.maximum + bottom_fwhm_peak.minimum) / 2,
                                   (bottom_fwhm_peak.maximum - bottom_fwhm_peak.minimum) / 2,
                                   np.max(bottom_prof) - np.min(bottom_prof),
                                   1,
                                   np.min(bottom_prof))
                    bottom_indeces = np.indices(bottom_prof.shape)[0]
                    bottom_fit, _ = curve_fit(flat_top_gauss,
                                              bottom_indeces,
                                              bottom_prof,
                                              bottom_init,
                                              bounds=bounds)
                    bottom_fitted = flat_top_gauss(bottom_indeces, *bottom_fit)
                    plt.plot(bottom_x_locs, bottom_fitted,
                             label="Bottom Fit")
                except RuntimeError:
                    pass

            plt.legend()
            plt.xlabel("Position (Pixels)")
            plt.ylabel("Value")
            plt.title("ROI Profiles")
            plt.show()
