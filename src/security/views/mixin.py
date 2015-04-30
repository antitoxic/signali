class SecuredViewMixin(object):
    def extract_permission_args(self, request, pk):
        """Returns tuple of arguments for the permission checking"""
        raise NotImplemented('Permission args extraction must be implemented before the view can be secured')
