from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer

from zope.interface import implements

from kotti.resources import IDocument
from kotti.resources import IDefaultWorkflow
from kotti.resources import Document
from kotti.resources import TypeInfo

from kotti.security import view_permitted

from pprint import pformat

from kotti_forum import _


class Forum(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)
    sort_order_is_ascending = Column('sort_order_is_ascending', Boolean())

    type_info = Document.type_info.copy(
        name=u'Forum',
        title=_(u'Forum'),
        add_view=u'add_forum',
        addable_to=[u'Document'],
        )

    def __init__(self,
                 sort_order_is_ascending=False,
                 **kwargs):
        super(Forum, self).__init__(**kwargs)

        self.sort_order_is_ascending = sort_order_is_ascending


class Topic(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column('id', Integer, ForeignKey('documents.id'), primary_key=True)
    votable = Column('votable', Boolean())
    sort_order_is_ascending = Column('sort_order_is_ascending', Boolean())

    type_info = Document.type_info.copy(
        name=u'Topic',
        title=_(u'Topic'),
        add_view=u'add_topic',
        addable_to=[u'Forum'],
        )

    def __init__(self,
                 votable=False,
                 sort_order_is_ascending=False,
                 **kwargs):
        super(Topic, self).__init__(**kwargs)
        self.votable = votable
        self.sort_order_is_ascending = sort_order_is_ascending


class Post(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)

    type_info = Document.type_info.copy(
        name=u'Post',
        title=_(u'Post'),
        add_view=u'add_post',
        addable_to=[u'Topic', u'Post'],
        )

    def __init__(self, thread_parent_id=None, **kwargs):
        super(Post, self).__init__(**kwargs)
        self.thread_parent_id = thread_parent_id 


class VoteTypeInfo(TypeInfo):

    def addable(self, context, request):
        """Return True if
            - the type described in 'self' may be added."""

        if view_permitted(context, request, self.add_view):
            addable = context.type_info.name in self.addable_to
            if context.type_info.name == 'Topic':
                vote_is_addable = True if context.votable else False
                return addable and vote_is_addable
            return False
        else:  # pragma: no cover (this already tested in Kotti itself)
            return False

    def copy(self, **kwargs):

        d = self.__dict__.copy()
        d.update(kwargs)
        return VoteTypeInfo(**d)

    def __repr__(self):  # pragma: no cover

        return pformat(self.__dict__)


vote_type_info = VoteTypeInfo(
        name=u'Vote',
        title=_(u'Vote'),
        add_view=u'add_vote',
        addable_to=[u'Topic'],
        )


class Vote(Document):
    implements(IDocument, IDefaultWorkflow)

    id = Column(Integer, ForeignKey('documents.id'), primary_key=True)
    vote = Column('vote', Integer())

    type_info = vote_type_info.copy()

    def __init__(self, vote="0", **kwargs):
        super(Vote, self).__init__(**kwargs)

        self.vote = vote
