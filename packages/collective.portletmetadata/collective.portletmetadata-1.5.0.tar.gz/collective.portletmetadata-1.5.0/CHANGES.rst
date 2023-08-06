Changes
=======

1.5.0 (2022-09-08)
------------------

- Make our patches have no effect when the product is not activated.
  Until now, when a portlet was marked as local, it was still invisible elsewhere when the product was deactivated,
  and you could no longer change the setting.
  [maurits]

- Fix uninstall to remove our registry settings.  [maurits]

- Have a different template override for edit manager macros on Plone 6.
  This uses Bootstrap 5 classes.
  [maurits]

- Fix ImportError on Plone 6, for isDefaultPage.
  [maurits]


1.4.1 (2022-03-14)
------------------

- Fix Plone 5.0 support by downgrading the minimum ``plone.app.portlets`` version to be 3.0.0.
  The 3.x series of plone.app.portlets is the version used by Plone 5.0.
  [JeffersonBledsoe]


1.4 (2022-01-05)
----------------

- Fix for Plone 5.2 and Python 3 compatibility.
  Should still work on Plone 5.0 and between as well.
  [maurits]


1.3 (2018-01-17)
----------------

- Fix case in managing groups-and contenttype-portlets when the query-string
  is no longer in the request.
  [kroman0, pbauer]

- Plone 5 compatibility - this release requires plone 5 (p.a.portlets >= 4.0.0)
  [sunew]

- uninstall profile
  [sunew]


1.2 (2014-04-22)
----------------

- Allow ``class|descriptive title`` as format in the control panel.
  When this format is used, we show the title in de portlet metadata
  edit form.  A simple ``class`` is of course still supported.
  [maurits]

- Support the local portlet checkbox for ContentWellPortlets.
  [mauritsvanrees]


1.1 (2014-03-13)
----------------

- Backported local portlets functionality
  [bosim]

- Override Products/ContentWellPortlets/browser/templates/renderer.pt
  [mauritsvanrees]


1.0 (2013-12-29)
----------------

Initial release
