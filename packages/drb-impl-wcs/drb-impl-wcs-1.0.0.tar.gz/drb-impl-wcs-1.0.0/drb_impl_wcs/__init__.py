from . import _version
from .wcs_nodes import WcsServiceNode, WcsNodeOperationGetCoverage, \
    WcsNodeOperationDescribeCoverage, WcsGetCoveragePredicate, \
    WcsDescribeCoveragePredicate

__version__ = _version.get_versions()['version']
__all__ = [
    'WcsServiceNode',
    'WcsNodeOperationGetCoverage',
    'WcsNodeOperationDescribeCoverage',
    'WcsGetCoveragePredicate',
    'WcsDescribeCoveragePredicate']
