# Copyright (c) 2011 gocept gmbh & co. kg
# See also LICENSE.txt

import zeit.cms.content.interfaces
import zeit.cms.repository.interfaces
import zeit.edit.interfaces
import zope.container.interfaces
import zope.interface


DAV_NAMESPACE = 'http://namespaces.zeit.de/CMS/newsletter'


class INewsletter(zeit.cms.content.interfaces.IXMLContent,
                  zope.container.interfaces.IReadContainer):
    pass


class IBody(zeit.edit.interfaces.IArea):
    pass


class IGroup(zeit.edit.interfaces.IArea,
             zeit.edit.interfaces.IBlock):

    title = zope.schema.TextLine(title=u'The title of this group')


class ITeaser(zeit.edit.interfaces.IBlock):

    reference = zope.schema.Choice(
        source=zeit.cms.content.contentsource.cmsContentSource)


class INewsletterCategory(zeit.cms.repository.interfaces.IFolder):

    last_created = zope.schema.Datetime(
        title=u'Timestamp when the last newsletter object'
        ' in this category was created')

    def create():
        """Creates a new newsletter object for this category."""


class IBuild(zope.interface.Interface):
    """Builds a newsletter in a way specific to the category."""

    def __call__(content_list):
        """Selects appropriate content objects and populates the newsletter
        with groups and teasers."""
