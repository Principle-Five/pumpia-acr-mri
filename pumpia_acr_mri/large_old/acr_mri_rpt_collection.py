"""
Collection for Large ACR with repeat images.
"""

from pumpia.module_handling.collections import ModuleGroup
from pumpia.module_handling.fields.windows import FieldWindow
from pumpia.module_handling.fields.groups import FieldGroup
from pumpia.module_handling.fields.viewer_fields import MonochromeDicomViewerField

from pumpia_acr_mri.bases.acr_mri_rpt_collection import ACRMRIrptCollection
from pumpia_acr_mri.large_old.acr_mri_context import LargeACRContextManager
from pumpia_acr_mri.large_old.modules.sub_snr import LargeACRSubSNR
from pumpia_acr_mri.large_old.modules.uniformity import LargeACRUniformity
from pumpia_acr_mri.large_old.modules.ghosting import LargeACRGhosting
from pumpia_acr_mri.large_old.modules.slice_width import LargeACRSliceWidth
from pumpia_acr_mri.large_old.modules.slice_pos import LargeACRSlicePosition
from pumpia_acr_mri.large_old.modules.phantom_width import LargeACRPhantomWidth
from pumpia_acr_mri.large_old.modules.resolution import LargeACRResolution


class LargeACRrptCollection(ACRMRIrptCollection):
    """
    Collection for large ACR phantom with repeated scans.
    """
    context_manager = LargeACRContextManager()
    title = "Large ACR Repeat Collection"

    viewer1 = MonochromeDicomViewerField(row=0, column=0)
    viewer2 = MonochromeDicomViewerField(row=0, column=1)

    snr = LargeACRSubSNR(verbose_name="SNR")

    uniformity1 = LargeACRUniformity(verbose_name="Uniformity")
    uniformity2 = LargeACRUniformity(verbose_name="Uniformity")

    ghosting1 = LargeACRGhosting(verbose_name="Ghosting")
    ghosting2 = LargeACRGhosting(verbose_name="Ghosting")

    phantom_width1 = LargeACRPhantomWidth(verbose_name="Phantom Width")
    phantom_width2 = LargeACRPhantomWidth(verbose_name="Phantom Width")

    slice_width1 = LargeACRSliceWidth(verbose_name="Slice Width")
    slice_width2 = LargeACRSliceWidth(verbose_name="Slice Width")

    slice_pos1 = LargeACRSlicePosition(verbose_name="Slice Position")
    slice_pos2 = LargeACRSlicePosition(verbose_name="Slice Position")

    resolution1 = LargeACRResolution(verbose_name="Resolution")
    resolution2 = LargeACRResolution(verbose_name="Resolution")

    snr_output = FieldWindow(snr.fields.signal,
                             snr.fields.noise,
                             snr.fields.snr,
                             snr.fields.cor_snr,
                             verbose_name="SNR Output")
    image1_output = FieldWindow(uniformity1.fields.uniformity,
                                ghosting1.fields.ghosting,
                                slice_width1.fields.slice_width,
                                slice_pos1.fields.slice_1_pos,
                                slice_pos1.fields.slice_11_pos,
                                phantom_width1.fields.linearity,
                                phantom_width1.fields.distortion,
                                resolution1.fields.total_contrast,
                                verbose_name="Image 1 Results")
    image2_output = FieldWindow(uniformity2.fields.uniformity,
                                ghosting2.fields.ghosting,
                                slice_width2.fields.slice_width,
                                slice_pos2.fields.slice_1_pos,
                                slice_pos2.fields.slice_11_pos,
                                phantom_width2.fields.linearity,
                                phantom_width2.fields.distortion,
                                resolution2.fields.total_contrast,
                                verbose_name="Image 2 Results")

    uniformity_size_group = FieldGroup(uniformity1.fields.size,
                                       uniformity2.fields.size)
    uniformity_kernel_group = FieldGroup(uniformity1.fields.kernel_bool,
                                         uniformity2.fields.kernel_bool)
    ghosting_size_group = FieldGroup(ghosting1.fields.size,
                                     ghosting2.fields.size)
    slice_width_tan_theta_group = FieldGroup(slice_width1.fields.tan_theta,
                                             slice_width2.fields.tan_theta)
    slice_width_max_perc_group = FieldGroup(slice_width1.fields.max_perc,
                                            slice_width2.fields.max_perc)
    slice_width_type_group = FieldGroup(slice_width1.fields.fit_type,
                                        slice_width2.fields.fit_type)
    phantom_width_max_perc_group = FieldGroup(phantom_width1.fields.max_perc,
                                              phantom_width2.fields.max_perc)
    phantom_width_inc_vert_group = FieldGroup(phantom_width1.fields.bool_vertical,
                                              phantom_width2.fields.bool_vertical)
    phantom_width_inc_hor_group = FieldGroup(phantom_width1.fields.bool_horizontal,
                                             phantom_width2.fields.bool_horizontal)
    phantom_width_inc_up_group = FieldGroup(phantom_width1.fields.bool_up_slope,
                                            phantom_width2.fields.bool_up_slope)
    phantom_width_inc_down_group = FieldGroup(phantom_width1.fields.bool_down_slope,
                                              phantom_width2.fields.bool_down_slope)
    res_perc_group = FieldGroup(resolution1.fields.resolution_percentage,
                                resolution2.fields.resolution_percentage)
    res_auto_pos_group = FieldGroup(resolution1.fields.auto_position_lines,
                                    resolution2.fields.auto_position_lines)
    res_type_group = FieldGroup(resolution1.fields.resolution_type,
                                resolution2.fields.resolution_type)

    uniformity_window = ModuleGroup(uniformity1, uniformity2,
                                    verbose_name="Uniformity")
    ghosting_window = ModuleGroup(ghosting1, ghosting2,
                                  verbose_name="Ghosting")
    slice_width_window = ModuleGroup(slice_width1, slice_width2,
                                     verbose_name="Slice Width")
    slice_pos_window = ModuleGroup(slice_pos1, slice_pos2,
                                   verbose_name="Slice Position")
    phantom_width_window = ModuleGroup(phantom_width1, phantom_width2,
                                       verbose_name="Phantom Width")
    resolution_window = ModuleGroup(resolution1, resolution2,
                                    verbose_name="Resolution")
