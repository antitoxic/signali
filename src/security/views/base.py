from abc import ABCMeta, abstractmethod

class SecuredView(metaclass=ABCMeta):
    @abstractmethod
    def extract_permission_target(self, request, *args, **kwargs):
        """Returns a target object for the permission checking"""
        pass

    @classmethod
    def __subclasshook__(cls, C):
        if cls is SecuredView:
            if any("extract_permission_target" in B.__dict__ for B in C.__mro__):
                return True
        return NotImplemented