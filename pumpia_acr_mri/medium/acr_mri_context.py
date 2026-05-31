from pumpia_acr_mri.bases.acr_mri_context import ACRMRIContextManager


class MedACRContextManager(ACRMRIContextManager):
    """
    Context Manager for Medium ACR Phantom.
    """
    FIVE_BOX_OFFSET = 28
    MIN_SLICE = 4
