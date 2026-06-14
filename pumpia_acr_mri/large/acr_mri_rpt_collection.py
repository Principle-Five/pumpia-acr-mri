"""
Collection for Large ACR with repeat images.
"""

from pumpia_acr_mri.bases.acr_mri_rpt_collection import ACRMRIrptCollection
from pumpia_acr_mri.large.acr_mri_context import LargeACRContextManager
from pumpia_acr_mri.large.modules.sub_snr import LargeACRSubSNR
from pumpia_acr_mri.large.modules.uniformity import LargeACRUniformity
from pumpia_acr_mri.large.modules.ghosting import LargeACRGhosting
from pumpia_acr_mri.large.modules.slice_width import LargeACRSliceWidth
from pumpia_acr_mri.large.modules.slice_pos import LargeACRSlicePosition
from pumpia_acr_mri.large.modules.phantom_width import LargeACRPhantomWidth
from pumpia_acr_mri.large.modules.resolution import LargeACRResolution


class LargeACRrptCollection(ACRMRIrptCollection):
    """
    Collection for large ACR phantom with repeated scans.
    """
    context_manager = LargeACRContextManager()
    title = "Large ACR Repeat Collection"

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
