"""
Subtraction SNR module for ACR MRI phantom
"""
from pumpia.module_handling.fields.roi_fields import EllipseROIField
from pumpia.module_handling.fields.viewer_fields import MonochromeDicomViewerField
from pumpia.module_handling.fields.simple import (PercField,
                                                  FloatField,
                                                  BoolField,
                                                  IntField)

from pumpia_acr_mri.bases.modules.sub_snr import ACRMRISubSNR

from pumpia_acr_mri.large.acr_mri_context import LargeACRContextManager


class LargeACRSubSNR(ACRMRISubSNR):
    """
    Module for subtraction method SNR on ACR MRI phantom.
    """
    context_manager = LargeACRContextManager()

    viewer1 = MonochromeDicomViewerField(row=0, column=0)
    viewer2 = MonochromeDicomViewerField(row=0, column=1, allow_changing_rois=False)

    size = PercField(70, verbose_name="Size (%)")
    ref_bandwidth = FloatField(1, verbose_name="Reference Bandwidth (Hz/px)")
    bw_cor_bool = BoolField(verbose_name="Bandwidth Correction")
    pix_size_bool = BoolField(verbose_name="Pixel Size Correction")
    avg_cor_bool = BoolField(verbose_name="Averages Correction")
    pe_cor_bool = BoolField(verbose_name="Phase Encode Correction")

    slice_used = IntField(read_only=True)
    im_bw = FloatField(verbose_name="Image Bandwidth (Hz/px)",
                       reset_on_analysis=True,
                       read_only=True)
    pixel_size_cor = FloatField(verbose_name="Pixel Size Correction",
                                reset_on_analysis=True,
                                read_only=True)
    pe_cor = FloatField(verbose_name="Phase Encode Correction",
                        reset_on_analysis=True,
                        read_only=True)
    avg_cor = FloatField(verbose_name="Averages Correction",
                         reset_on_analysis=True,
                         read_only=True)
    signal = FloatField(reset_on_analysis=True,
                        read_only=True)
    noise = FloatField(reset_on_analysis=True,
                       read_only=True)
    snr = FloatField(verbose_name="SNR",
                     reset_on_analysis=True,
                     read_only=True)
    cor_snr = FloatField(verbose_name="Corrected SNR",
                         reset_on_analysis=True,
                         read_only=True)

    signal_roi1 = EllipseROIField("SNR ROI1")
    signal_roi2 = EllipseROIField("SNR ROI2", allow_manual_draw=False)
