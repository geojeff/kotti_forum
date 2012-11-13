from fanstatic import (
    Library,
    Resource,
    Group,
    )
from pyramid.i18n import TranslationStringFactory
from kotti.fanstatic import view_needed
from kotti.util import extract_from_settings
from js.jquery_infinite_ajax_scroll import (
    jquery_infinite_ajax_scroll,
    jquery_infinite_ajax_scroll_css,
)

_ = TranslationStringFactory('kotti_forum')

library = Library("kotti_forum", "static")
kotti_forum_css = Resource(library,
                           "style.css",
                           depends=[jquery_infinite_ajax_scroll_css, ],
                           bottom=True)
kotti_forum_js = Resource(library,
                          "kotti_forum.js",
                          depends=[jquery_infinite_ajax_scroll, ],
                          bottom=True)
view_needed.add(Group([kotti_forum_css, kotti_forum_js, ]))


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_forum.views'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Forum'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Topic'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Post'


def check_true(value):
    if value == u'true':
        return True
    return False


FORUM_DEFAULTS = {
    'use_batching': 'true',
    'pagesize': '5',
    'use_auto_batching': 'true',
    'link_headline_overview': 'true',
    }


def forum_settings(name=''):
    prefix = 'kotti_forum.forum_settings.'
    if name:
        prefix += name + '.'  # pragma: no cover
    settings = FORUM_DEFAULTS.copy()
    settings.update(extract_from_settings(prefix))
    settings['use_batching'] = check_true(settings['use_batching'])
    try:
        settings['pagesize'] = int(settings['pagesize'])
    except ValueError:
        settings['pagesize'] = 5
    settings['use_auto_batching'] = check_true(settings['use_auto_batching'])
    settings['link_headline_overview'] = \
            check_true(settings['link_headline_overview'])
    return settings
