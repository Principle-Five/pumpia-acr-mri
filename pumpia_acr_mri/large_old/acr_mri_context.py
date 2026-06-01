from pumpia_acr_mri.bases.acr_mri_context import ACRMRIContextManager


class LargeACRContextManager(ACRMRIContextManager):
    """
    Context Manager for Large ACR Phantom.
    """
    FIVE_BOX_OFFSET = 33
    MIN_SLICE = 0
