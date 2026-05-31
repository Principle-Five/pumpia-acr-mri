"""
Collection for Medium ACR with repeat images.
"""

from pumpia.module_handling.collections import ModuleGroup, BaseCollection
from pumpia.module_handling.fields.windows import FieldWindow
from pumpia.module_handling.fields.groups import FieldGroup
from pumpia.module_handling.fields.viewer_fields import MonochromeDicomViewerField
from pumpia.widgets.viewers import MonochromeDicomViewer

from pumpia_acr_mri.bases.acr_mri_context import ACRMRIContextManager
from pumpia_acr_mri.bases.modules.sub_snr import ACRMRISubSNR
from pumpia_acr_mri.bases.modules.uniformity import ACRMRIUniformity
from pumpia_acr_mri.bases.modules.ghosting import ACRMRIGhosting
from pumpia_acr_mri.bases.modules.slice_width import ACRMRISliceWidth
from pumpia_acr_mri.bases.modules.slice_pos import ACRMRISlicePosition
from pumpia_acr_mri.bases.modules.phantom_width import ACRMRIPhantomWidth
from pumpia_acr_mri.bases.modules.resolution import ACRMRIResolution


class ACRMRIrptCollection(BaseCollection):
    """
    Collection for ACR MRI phantom with repeated scans.
    """
    context_manager: ACRMRIContextManager
    title = "ACR MRI Repeat Collection"

    viewer1: MonochromeDicomViewerField
    viewer2: MonochromeDicomViewerField

    snr: ACRMRISubSNR

    uniformity1: ACRMRIUniformity
    uniformity2: ACRMRIUniformity

    ghosting1: ACRMRIGhosting
    ghosting2: ACRMRIGhosting

    phantom_width1: ACRMRIPhantomWidth
    phantom_width2: ACRMRIPhantomWidth

    slice_width1: ACRMRISliceWidth
    slice_width2: ACRMRISliceWidth

    slice_pos1: ACRMRISlicePosition
    slice_pos2: ACRMRISlicePosition

    resolution1: ACRMRIResolution
    resolution2: ACRMRIResolution

    snr_output: FieldWindow
    image1_output: FieldWindow
    image2_output: FieldWindow

    uniformity_size_group: FieldGroup
    uniformity_kernel_group: FieldGroup
    ghosting_size_group: FieldGroup
    slice_width_tan_theta_group: FieldGroup
    slice_width_max_perc_group: FieldGroup
    slice_width_type_group: FieldGroup
    phantom_width_max_perc_group: FieldGroup
    phantom_width_inc_vert_group: FieldGroup
    phantom_width_inc_hor_group: FieldGroup
    phantom_width_inc_up_group: FieldGroup
    phantom_width_inc_down_group: FieldGroup
    res_perc_group: FieldGroup
    res_auto_pos_group: FieldGroup
    res_type_group: FieldGroup

    uniformity_window: ModuleGroup
    ghosting_window: ModuleGroup
    slice_width_window: ModuleGroup
    slice_pos_window: ModuleGroup
    phantom_width_window: ModuleGroup
    resolution_window: ModuleGroup

    def on_image_load(self, viewer: MonochromeDicomViewer) -> None:
        if viewer is self.viewer1:
            if self.viewer1.image is not None:
                image = self.viewer1.image
                self.snr.viewer1.load_image(image)
                self.uniformity1.viewer.load_image(image)
                self.ghosting1.viewer.load_image(image)
                self.slice_width1.viewer.load_image(image)
                self.slice_pos1.viewer1.load_image(image)
                self.phantom_width1.viewer.load_image(image)
                self.resolution1.viewer.load_image(image)
        elif viewer is self.viewer2:
            if self.viewer2.image is not None:
                image = self.viewer2.image
                self.snr.viewer2.load_image(image)
                self.uniformity2.viewer.load_image(image)
                self.ghosting2.viewer.load_image(image)
                self.slice_width2.viewer.load_image(image)
                self.slice_pos2.viewer1.load_image(image)
                self.phantom_width2.viewer.load_image(image)
                self.resolution2.viewer.load_image(image)
