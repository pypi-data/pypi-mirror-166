from drb import DrbNode
from drb.factory import DrbFactory
from drb_impl_http import DrbHttpNode
from drb.exceptions import DrbFactoryException

from .wcs_nodes import WcsServiceNode


class WcsFactory(DrbFactory):
    def _create(self, node: DrbNode) -> DrbNode:
        if isinstance(node, DrbHttpNode):
            node_wcs_service = WcsServiceNode(
                url=node.path.original_path,
                auth=node.auth)
        else:
            node_wcs_service = WcsServiceNode(
                url=node.path.original_path)
        try:
            node_wcs_service.children
        except err:
            final_url = node.path.name.replace('+wcs', '')
            raise DrbFactoryException(f'Unsupported Wcs service: {final_url}')
        return node_wcs_service
