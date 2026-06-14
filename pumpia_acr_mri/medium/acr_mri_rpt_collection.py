"""
Collection for Medium ACR with repeat images.
"""

from pumpia_acr_mri.bases.acr_mri_rpt_collection import ACRMRIrptCollection
from pumpia_acr_mri.medium.acr_mri_context import MedACRContextManager
from pumpia_acr_mri.medium.modules.sub_snr import MedACRSubSNR
from pumpia_acr_mri.medium.modules.uniformity import MedACRUniformity
from pumpia_acr_mri.medium.modules.ghosting import MedACRGhosting
from pumpia_acr_mri.medium.modules.slice_width import MedACRSliceWidth
from pumpia_acr_mri.medium.modules.slice_pos import MedACRSlicePosition
from pumpia_acr_mri.medium.modules.phantom_width import MedACRPhantomWidth
from pumpia_acr_mri.medium.modules.resolution import MedACRResolution


class MedACRrptCollection(ACRMRIrptCollection):
    """
    Collection for medium ACR phantom with repeated scans.
    """
    context_manager = MedACRContextManager()
    title = "Medium ACR Repeat Collection"

    snr = MedACRSubSNR(verbose_name="SNR")

    uniformity1 = MedACRUniformity(verbose_name="Uniformity")
    uniformity2 = MedACRUniformity(verbose_name="Uniformity")

    ghosting1 = MedACRGhosting(verbose_name="Ghosting")
    ghosting2 = MedACRGhosting(verbose_name="Ghosting")

    phantom_width1 = MedACRPhantomWidth(verbose_name="Phantom Width")
    phantom_width2 = MedACRPhantomWidth(verbose_name="Phantom Width")

    slice_width1 = MedACRSliceWidth(verbose_name="Slice Width")
    slice_width2 = MedACRSliceWidth(verbose_name="Slice Width")

    slice_pos1 = MedACRSlicePosition(verbose_name="Slice Position")
    slice_pos2 = MedACRSlicePosition(verbose_name="Slice Position")

    resolution1 = MedACRResolution(verbose_name="Resolution")
    resolution2 = MedACRResolution(verbose_name="Resolution")
