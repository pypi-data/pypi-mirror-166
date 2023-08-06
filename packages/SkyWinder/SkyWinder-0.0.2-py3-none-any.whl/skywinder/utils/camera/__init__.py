import warnings as _warnings

try:
    from .pycamera.pycamera import PyCamera
except ImportError:  # pragma: no cover
    _warnings.warn("Could not import PyCamera")  # pragma: no cover