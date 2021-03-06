from pyramid.i18n import TranslationStringFactory
from kotti.util import extract_from_settings

_ = TranslationStringFactory('kotti_forum')


def kotti_configure(settings):
    settings['pyramid.includes'] += ' kotti_forum.views'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Forum'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Topic'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Post'
    settings['kotti.available_types'] += \
            ' kotti_forum.resources.Vote'
    settings['kotti.alembic_dirs'] += ' kotti_forum:alembic'


def check_true(value):
    if value == u'true':
        return True
    return False


FORUM_DEFAULTS = {
    'use_batching': 'true',
    'pagesize': '10',
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
        settings['pagesize'] = 10
    settings['use_auto_batching'] = check_true(settings['use_auto_batching'])
    settings['link_headline_overview'] = \
            check_true(settings['link_headline_overview'])
    return settings
