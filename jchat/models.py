from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType, ContentTypeManager
from django.contrib.contenttypes import generic
from django.utils import timezone
from django.utils.timezone import make_aware
import datetime
import random, string

from monopoly.models import Player

def my_random_key():
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(10))

class RoomManager(models.Manager):
    '''Custom model manager for rooms, this is used for "table-level" operations.
    All methods defined here can be invoked through the Room.objects class.
    @see: http://docs.djangoproject.com/en/1.0/topics/db/managers/#topics-db-managers
    Also see GenericTypes from the contenttypes django app!
    @see: http://docs.djangoproject.com/en/1.0/ref/contrib/contenttypes/'''

    def create(self, object):
        '''Creates a new chat room and registers it to the calling object'''
        r = self.model(content_object=object)
        r.save()
        return r

    def get_for_object(self, object):
        '''Try to get a room related to the object passed.'''
        return self.get(content_type=ContentType.objects.get_for_model(object), object_id=object.pk)

    def get_or_create(self, object):
        '''Save us from the hassle of validating the return value of get_for_object and create a room if none exists'''
        try:
            return self.get_for_object(object)
        except Room.DoesNotExist:
            return self.create(object)

class Room(models.Model):
    '''Representation of a generic chat room'''
    id = models.AutoField(primary_key=True)
    content_type = models.ForeignKey(ContentType) # to what kind of object is this related
    object_id = models.PositiveIntegerField() # to which instace of the aforementioned object is this related
    content_object = generic.GenericForeignKey('content_type','object_id') # use both up, USE THIS WHEN INSTANCING THE MODEL
    created = models.DateTimeField(default=datetime.datetime.now())
    comment = models.TextField(blank=True, null=True)
    objects = RoomManager() # custom manager

    def __add_message(self, type, sender, message=None):
        '''Generic function for adding a message to the chat room'''
        m = Message(room=self, type=type, author=sender, message=message)
        m.save()
        return m

    def say(self, sender, message):
        '''Say something in to the chat room'''
        return self.__add_message('m', sender, message)
    def join(self, user):
        '''A user has joined'''
        return self.__add_message('j', user)

    def leave(self, user):
        '''A user has leaved'''
        return self.__add_message('l', user)

    def messages(self, after_pk=None, after_date=None):
        '''List messages, after the given id or date'''
        m = Message.objects.filter(room=self)
        if after_pk:
            m = m.filter(pk__gt=after_pk)
        if after_date:
            m = m.filter(timestamp__gte=after_date)
        return m.order_by('pk')

    def last_message_id(self):
        '''Return last message sent to room'''
        m = Message.objects.filter(room=self).order_by('-pk')
        if m:
            return m[0].id
        else:
            return 0

    def __unicode__(self):
        return 'Chat for %s %d' % (self.content_type, self.object_id)

MESSAGE_TYPE_CHOICES = (
    ('s','system'),
    ('a','action'),
    ('m', 'message'),
    ('j','join'),
    ('l','leave'),
    ('n','notification')
)
class Spy_code(models.Model):
    spy_hash = models.CharField(max_length=10, default=my_random_key, unique=True)
    linked_room = models.ForeignKey(Room, null=True, blank=True)
    first_used = models.DateTimeField(null=True, blank=True)
    used_by = models.ForeignKey(Player, null=True, blank=True)
    def is_active(self):
        if(self.first_used is None):
             self.first_used =  timezone.now() #datetime.datetime.now()
             self.save()
             return True
        else:
            if (self.first_used + datetime.timedelta(hours=12) >=  timezone.now()):
                return True
            else:
                return False
    def is_set(self):
        try:
            if self.linked_room:
                return True
        except NameError:
            return False
    def is_allowed(self, user):
        if (self.used_by is None):
            self.used_by = user
            self.save()
            return True
        elif (self.used_by == user):
            return True
        else:
            return False

class Message(models.Model):
    '''A message that belongs to a chat room'''
    room = models.ForeignKey(Room)
    type = models.CharField(max_length=1, choices=MESSAGE_TYPE_CHOICES)
    #sender = models.CharField(max_length=50, blank=True)
    author = models.ForeignKey(User, related_name='author', blank=True, null=True)
    message = models.CharField(max_length=255, blank=True, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        '''Each message type has a special representation, return that representation.
        This will also be translator AKA i18l friendly.'''
        if self.type == 's':
            return u'SYSTEM: %s' % self.message
        if self.type == 'n':
            return u'NOTIFICATION: %s' % self.message
        elif self.type == 'j':
            return 'JOIN: %s' % self.author
        elif self.type == 'l':
            return 'LEAVE: %s' % self.author
        elif self.type == 'a':
            return 'ACTION: %s > %s' % (self.author, self.message)
        return self.message