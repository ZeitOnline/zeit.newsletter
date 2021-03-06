from zeit.cms.i18n import MessageFactory as _
from zope.cachedescriptors.property import Lazy as cachedproperty
import os.path
import zeit.cms.browser.view
import zeit.cms.content.interfaces
import zeit.cms.interfaces
import zeit.content.image.interfaces
import zeit.content.video.interfaces
import zeit.edit.browser.form
import zeit.edit.browser.landing
import zeit.edit.browser.view
import zeit.newsletter.interfaces
import zope.formlib.form


class LandingZoneBase(zeit.edit.browser.landing.LandingZone):

    uniqueId = zeit.edit.browser.view.Form('uniqueId')
    block_type = 'teaser'

    def initialize_block(self):
        content = zeit.cms.interfaces.ICMSContent(self.uniqueId)
        self.block.reference = content


class GroupLandingZone(LandingZoneBase):
    """Handler to drop objects to the body's landing zone."""

    order = 0


class TeaserLandingZone(LandingZoneBase):
    """Handler to drop objects after other objects."""

    order = 'after-context'


class Teaser(zeit.cms.browser.view.Base):

    @cachedproperty
    def metadata(self):
        return zeit.cms.content.interfaces.ICommonMetadata(
            self.context.reference, None)

    @cachedproperty
    def image(self):
        # XXX copy&paste&tweak of zeit.content.cp.browser.blocks.teaser.Display
        content = self.context.reference
        if content is None:
            return
        if zeit.content.video.interfaces.IVideoContent.providedBy(content):
            return content.thumbnail
        images = zeit.content.image.interfaces.IImages(content, None)
        if images is None:
            preview = zope.component.queryMultiAdapter(
                (content, self.request), name='preview')
            if preview:
                return self.url(preview)
            return
        if not images.image:
            return
        group = images.image
        for name in group:
            basename, ext = os.path.splitext(name)
            if basename.endswith('148x84'):
                image = group[name]
                return self.url(image, '@@raw')


class Advertisement(zeit.cms.browser.view.Base):

    @cachedproperty
    def image(self):
        if not self.context.image:
            return
        return self.url(self.context.image, '@@raw')


class GroupTitle(zeit.edit.browser.form.InlineForm):

    legend = None
    prefix = 'group'
    undo_description = _('edit group title')

    form_fields = zope.formlib.form.FormFields(
        zeit.newsletter.interfaces.IGroup).select('title')


class Empty(object):

    def render(self):
        return u''
