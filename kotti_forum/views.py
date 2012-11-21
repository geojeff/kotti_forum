import datetime
from dateutil.tz import tzutc

from sqlalchemy import func

import colander
from colander import Invalid

import logging

from deform.widget import CheckboxWidget
from deform.widget import DateTimeInputWidget
from deform.widget import SelectWidget
from deform.widget import RadioChoiceWidget

from kotti.views.form import AddFormView
from kotti.views.form import EditFormView

from kotti.views.edit import DocumentSchema

from kotti_forum import forum_settings
from kotti_forum.resources import Forum
from kotti_forum.resources import Topic
from kotti_forum.resources import Post
from kotti_forum.resources import Vote
from kotti_forum.static import kotti_forum_js
from kotti_forum import _

from kotti.security import has_permission
from kotti.views.util import template_api
from kotti.views.util import nodes_tree

from kotti import DBSession

from plone.batching import Batch

from pyramid.view import view_config
from pyramid.view import view_defaults
from pyramid.renderers import get_renderer

log = logging.getLogger(__name__)


class ForumSchema(DocumentSchema):
    choices = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'))
    sort_order_choice = colander.SchemaNode(colander.String(),
            title=_(u'Sort Order'),
            default='descending',
            widget=RadioChoiceWidget(values=choices),
            validator=colander.OneOf(('ascending', 'descending')))


class TopicSchema(DocumentSchema):
    choices = (
        ('ascending', 'Ascending'),
        ('descending', 'Descending'))
    sort_order_choice = colander.SchemaNode(colander.String(),
            title=_(u'Sort Order'),
            default='descending',
            widget=RadioChoiceWidget(values=choices),
            validator=colander.OneOf(('ascending', 'descending')))

    votable = colander.SchemaNode(
        colander.Boolean(),
        description='Accepts Votes',
        default=False,
        widget=CheckboxWidget(),
        title='Votable')


class PostSchema(DocumentSchema):
    pass


class VoteSchema(DocumentSchema):
    choices = (('', '- Select -'),
               (1, '+1'),
               (0, '0'),
               (-1, '-1'))
    vote = colander.SchemaNode(
        colander.String(),
        default=_(u'0'),
        missing=_(u'0'),
        title=_(u'Vote'),
        widget=SelectWidget(values=choices))


class AddPostFormView(AddFormView):
    item_type = _(u"Post")
    item_class = Post

    def schema_factory(self):

        return PostSchema()

    def add(self, **appstruct):

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            )


class EditPostFormView(EditFormView):

    def schema_factory(self):

        return PostSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']


class AddVoteFormView(AddFormView):
    item_type = _(u"Vote")
    item_class = Vote

    def schema_factory(self):

        return VoteSchema()

    def add(self, **appstruct):

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            vote=appstruct['vote'],
            )


class EditVoteFormView(EditFormView):

    def schema_factory(self):

        return VoteSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']

        if appstruct['vote']:
            self.context.vote = appstruct['vote']


class AddForumFormView(AddFormView):
    item_type = _(u"Forum")
    item_class = Forum

    def schema_factory(self):

        return ForumSchema()

    def add(self, **appstruct):
        sort_order_is_ascending = False

        if appstruct['sort_order_choice'] == 'ascending':
            sort_order_is_ascending = True

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            default_view='folder-view',
            sort_order_is_ascending=sort_order_is_ascending,
            )


class EditForumFormView(EditFormView):

    def schema_factory(self):

        return ForumSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']

        if appstruct['sort_order_choice'] == 'ascending':
            self.context.sort_order_is_ascending = True
        else:
            self.context.sort_order_is_ascending = False


class AddTopicFormView(AddFormView):
    item_type = _(u"Topic")
    item_class = Topic

    def schema_factory(self):

        return TopicSchema()

    def add(self, **appstruct):
        sort_order_is_ascending = False

        if appstruct['sort_order_choice'] == 'ascending':
            sort_order_is_ascending = True

        return self.item_class(
            title=appstruct['title'],
            description=appstruct['description'],
            body=appstruct['body'],
            tags=appstruct['tags'],
            votable=appstruct['votable'],
            sort_order_is_ascending=sort_order_is_ascending,
            )


class EditTopicFormView(EditFormView):

    def schema_factory(self):

        return TopicSchema()

    def edit(self, **appstruct):

        if appstruct['title']:
            self.context.title = appstruct['title']

        if appstruct['description']:
            self.context.description = appstruct['description']

        if appstruct['body']:
            self.context.body = appstruct['body']

        if appstruct['tags']:
            self.context.tags = appstruct['tags']

        if appstruct['votable']:
            self.context.votable = appstruct['votable']

        if appstruct['sort_order_choice'] == 'ascending':
            self.context.sort_order_is_ascending = True
        else:
            self.context.sort_order_is_ascending = False


@view_defaults(permission='view')
class BaseView(object):

    def __init__(self, context, request):

        self.context = context
        self.request = request

        if has_permission("edit", self.context, self.request):
            kotti_forum_js.need()


@view_defaults(context=Post,
               permission='view')
class PostView(BaseView):

    @view_config(renderer='kotti_forum:templates/post-view.pt')
    def view(self):
        if self.context.children:
            tree = nodes_tree(self.request, self.context)
            return {
                'tree': {
                    'children': [tree],
                    },
                }
        else:
            return {}


@view_defaults(context=Vote,
               permission='view')
class VoteView(BaseView):

    @view_config(renderer='kotti_forum:templates/vote-view.pt')
    def view(self):

        return {}


@view_defaults(context=Topic,
               permission='view')
class TopicView(BaseView):

    @view_config(
             renderer="kotti_forum:templates/topic-view.pt")
    def view(self):

        session = DBSession()

        # Posts, if we have them.

        order_by = Post.modification_date
        if self.context.sort_order_is_ascending:
            order_by = Post.modification_date.desc()
        query = (session.query(Post)
                 .filter(Post.parent_id == self.context.id)
                 .order_by(order_by)
                )

        top_level_posts = query.all()

        post_counts_and_trees = []

        for post in top_level_posts:
            if post.children:
                tree = nodes_tree(self.request, post)
                post_count = len(tree.tolist())
            else:
                tree = (post)
                post_count = 1
            post_tree = {
                'tree': {
                    'children': [tree],
                    },
                }

            post_counts_and_trees.append((post_count, post, post_tree))

        # Votes, if we have them.

        votes = None

        vote_data = {}
        vote_data['Sum'] = 0
        vote_data['Count'] = 0
        vote_data['Plus'] = 0
        vote_data['Zero'] = 0
        vote_data['Minus'] = 0

        votes_and_vote_objs = []

        if self.context.votable:

            query = session.query(Vote).filter(
                    Vote.parent_id == self.context.id)

            votes = query.all()

            for vote in votes:

                vote_data['Sum'] += vote.vote
                vote_data['Count'] += 1

                if vote.vote > 0:
                    vote_data['Plus'] += 1
                elif vote.vote == 0:
                    vote_data['Zero'] += 1
                else:
                    vote_data['Minus'] += 1

                votes_and_vote_objs.append((vote.vote, vote, 'vote'))

            if votes_and_vote_objs:
                if self.context.sort_order_is_ascending:
                    votes_and_vote_objs = sorted(votes_and_vote_objs)
                else:
                    votes_and_vote_objs = sorted(votes_and_vote_objs, reverse=True)

        page = self.request.params.get('page', 1)

        settings = forum_settings()

        if settings['use_batching']:
            post_items = Batch.fromPagenumber(post_counts_and_trees,
                          pagesize=settings['pagesize'],
                          pagenumber=int(page))

        return {
            'api': template_api(self.context, self.request),
            'macros': get_renderer('templates/macros.pt').implementation(),
            'vote_items': votes_and_vote_objs,
            'vote_data': vote_data,
            'items': post_items,
            'settings': settings,
            }


@view_defaults(context=Forum,
               permission='view')
class ForumView(BaseView):

    @view_config(
             renderer="kotti_forum:templates/forum-view.pt")
    def view(self):

        session = DBSession()

        query = session.query(Topic).filter(
                Topic.parent_id == self.context.id)

        items = query.all()

        modification_dates_and_items = []
        for item in items:
            if item.children:
                sorted_posts = sorted(item.children, 
                                      key=lambda x: x.modification_date,
                                      reverse=True)
                modification_dates_and_items.append(
                        (sorted_posts[0].modification_date, sorted_posts[0], item))
            else:
                modification_dates_and_items.append(
                        (item.modification_date, item, item))


        if self.context.sort_order_is_ascending:
            items = sorted(modification_dates_and_items)
        else:
            items = sorted(modification_dates_and_items, reverse=True)

        page = self.request.params.get('page', 1)

        settings = forum_settings()

        if settings['use_batching']:
            items = Batch.fromPagenumber(items,
                          pagesize=settings['pagesize'],
                          pagenumber=int(page))

        return {
            'api': template_api(self.context, self.request),
            'macros': get_renderer('templates/macros.pt').implementation(),
            'items': items,
            'settings': settings,
            }


def includeme_edit(config):

    config.add_view(
        EditForumFormView,
        context=Forum,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddForumFormView,
        name=Forum.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        EditTopicFormView,
        context=Topic,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddTopicFormView,
        name=Topic.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        EditPostFormView,
        context=Post,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddPostFormView,
        name=Post.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        EditVoteFormView,
        context=Vote,
        name='edit',
        permission='edit',
        renderer='kotti:templates/edit/node.pt',
        )

    config.add_view(
        AddVoteFormView,
        name=Vote.type_info.add_view,
        permission='add',
        renderer='kotti:templates/edit/node.pt',
        )


def includeme_view(config):

    config.add_static_view('static-kotti_forum', 'kotti_forum:static')


def includeme(config):

    settings = config.get_settings()

    if 'kotti_forum.asset_overrides' in settings:
        asset_overrides = \
                [a.strip()
                 for a in settings['kotti_forum.asset_overrides'].split()
                 if a.strip()]
        for override in asset_overrides:
            config.override_asset(to_override='kotti_forum',
                                  override_with=override)

    config.scan("kotti_forum")

    includeme_edit(config)
    includeme_view(config)
