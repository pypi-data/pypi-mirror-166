from collective.portletmetadata.interfaces import IPortletMetadata
from plone.app.portlets.browser import formhelper
from plone.portlets.interfaces import IPortletAssignment
from plone.portlets.interfaces import IPortletAssignmentSettings
from zope.component import adapter
from zope.interface import implementer


@adapter(IPortletAssignment)
@implementer(IPortletMetadata)
class PortletMetadataAdapter(object):
    def __init__(self, context):
        # avoid recursion
        self.__dict__["context"] = context

    def __setattr__(self, attr, value):
        settings = IPortletAssignmentSettings(self.context)
        settings[attr] = value

    def __getattr__(self, attr):
        settings = IPortletAssignmentSettings(self.context)
        return settings.get(attr, None)


class PortletMetadataEditForm(formhelper.EditForm):
    label = u"Edit portlet settings"
    schema = IPortletMetadata

    def getContent(self):
        return IPortletMetadata(self.context)
