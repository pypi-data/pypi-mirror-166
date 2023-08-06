from Acquisition import aq_inner
from Acquisition import aq_parent
from plone.app.portlets.interfaces import IColumn
from plone.app.portlets.manager import (
    ColumnPortletManagerRenderer as BaseColumnPortletManagerRenderer,
)
from Products.CMFPlone.defaultpage import check_default_page_via_view
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import adapter
from zope.interface import Interface
from zope.publisher.interfaces.browser import IBrowserView
from zope.publisher.interfaces.browser import IDefaultBrowserLayer


@adapter(Interface, IDefaultBrowserLayer, IBrowserView, IColumn)
class ColumnPortletManagerRenderer(BaseColumnPortletManagerRenderer):

    template = ViewPageTemplateFile("column.pt")

    def available(self, info):
        """Only make available on definition context

        Our _lazyLoadPortlets patch makes sure the portlet info has a 'settings'
        attribute, but only if the product has been activated.
        """
        if info.get("settings", {}).get("is_local", False):
            compare_context = self.context
            if check_default_page_via_view(self.context, self.request):
                compare_context = aq_parent(aq_inner(self.context))
            if "/".join(compare_context.getPhysicalPath()) != info["key"]:
                return False

        return True
