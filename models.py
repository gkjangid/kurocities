from django.db                      import models
from django.core.exceptions         import ValidationError
from django.contrib.auth.models     import User
from django.contrib.postgres.fields import JSONField
from django.utils                   import timezone

import datetime
import itertools


# Choices

FEEDBACK_TYPES = [
    ( 'positive', 'Positive' ),
    ( 'negative', 'Negative' ),
]

LEARNING_OUTCOME_CATEGORIES = (
    ( 'Comprehend',   'Comprehend'   ),
    ( 'Apply',        'Apply'        ),
    ( 'Analyze',      'Analyze'      ),
    ( 'Synthesize',   'Synthesize'   ),
    ( 'Evaluate',     'Evaluate'     ),
    ( 'Emotionalize', 'Emotionalize' ),
)

TODO_STATUSES = (
    ( 'in-progress', 'In Progress' ),
    ( 'completed',   'Completed'   ),
    ( 'cancelled',   'Cancelled'   ),
)

YES_NO_CHOICES = (
    ( True, 'Yes' ),
    ( False, 'No' )
)

# Base models

class BaseModel( models.Model ):
    created     = models.DateTimeField ( auto_now_add=True )
    modified    = models.DateTimeField ( auto_now=True     )

    class Meta:
        abstract = True


class ReferenceDataModelManager( models.Manager ):

    def get_by_natural_key( self, name ):
        return self.get( name=name )

class ReferenceDataModel( BaseModel ):
    objects = ReferenceDataModelManager()
    name    = models.CharField( max_length=255, unique=True )
    order   = models.IntegerField( blank=True, default=999 )

    def __str__( self ):
        return self.name

    def natural_key( self ):
        return ( self.name, )

    class Meta:
        abstract = True
        ordering = [ 'order', 'name' ]

#####
#####

class ActivityManager( models.Manager ):
    def get_by_natural_key( self, title ):
        return self.get( title=title )

    def questions( self, *, questionType=None, logicalType=None, mathType=None ):
        data = []
        for activity in self.all():
            for i, question in enumerate( activity.data.get( 'questions', [] )):
                if questionType and question['questionType']    != questionType:  continue
                if logicalType  and question.get('logicalType') != logicalType:   continue
                if mathType     and question.get('mathType')    != mathType:      continue
                question['activity']    = activity.data['title']
                question['question_no'] = i
                data.append( question )
        return data

class Activity( BaseModel ):
    objects                 = ActivityManager()

    title                   = models.CharField ( max_length=255, unique=True )
    data                    = JSONField( default=dict )
    learning_journal        = models.ForeignKey( 'LearningJournal', on_delete=models.PROTECT, blank=True, null=True )
    checker                 = models.ForeignKey( User, on_delete=models.PROTECT, related_name='checker_set', blank=True, null=True )
    created_by              = models.ForeignKey( User, on_delete=models.PROTECT, related_name='+' )
    modified_by             = models.ForeignKey( User, on_delete=models.PROTECT, related_name='+' )

    def __str__( self ):
        return self.title

    def natural_key( self ):
        return ( self.title, )

    @property
    def name( self ):
        return self.title

    @classmethod
    def needs_checker( cls, question ):
        return question ['questionType'] == 'noAutoCorrection' and question.get( 'needsChecker' )

    def questions( self, questionType=None ):
        questions = self.data.get( 'questions' ) or []
        if questionType:
            questions = [ question
                for question in questions
                if question.get( 'questionType' ) == questionType
            ]
        return questions

    class Meta:
        verbose_name_plural = 'Activities'
        ordering = [ 'title' ]

# -----

class ActivityStatus( ReferenceDataModel ):
    class Meta( ReferenceDataModel.Meta ):
        verbose_name_plural = 'Activity statuses'
        ordering            = [ 'order', 'id' ]

# -----

class AgeGroup( ReferenceDataModel ):
    class Meta( ReferenceDataModel.Meta ):
        ordering = [ 'order', 'id' ]

# -----

class AnswerScoreManager( models.Manager ):

    def get_by_natural_key( self, answer_score_type, attempt_no ):
        return self.get( answer_score_type=answer_score_type, attempt_no=attempt_no )

class AnswerScore( BaseModel ):
    objects = AnswerScoreManager()

    answer_score_type   = models.ForeignKey( 'AnswerScoreType', on_delete=models.PROTECT )
    attempt_no          = models.IntegerField()
    score               = models.IntegerField()

    def __str__( self ):
        return '{self.answer_score_type}::{self.attempt_no}::{self.score}'.format ( self=self )

    def natural_key( self ):
        return ( self.answer_score_type, self.attempt_no )

    class Meta:
        ordering        = [ 'answer_score_type', 'attempt_no' ]
        unique_together = ( 'answer_score_type', 'attempt_no' )

# -----

class AnswerScoreType( ReferenceDataModel ):
    pass

# -----

class AppFeatureManager( models.Manager ):

    def get_by_natural_key( self, name ):
        return self.get( name=name )

    def chk_feature( self, name ):
        try:
            obj = self.get( name=name )
        except self.DoesNotExist:
            obj, _ = self.get_or_create( name=name )
        return obj.enabled

    class Meta:
        ordering = [ 'name' ]

class AppFeature( BaseModel ):
    objects = AppFeatureManager()

    name        = models.CharField( max_length=32, unique=True )
    enabled     = models.BooleanField( blank=True, default=True )

    def __str__( self ):
        return self.name

    def natural_key( self ):
        return ( self.name, )

# -----
# -----

class CannedFeedbackManager( models.Manager ):

    def get_by_natural_key( self, feedback_type, feedback ):
        return self.get( feedback_type=feedback_type, feedback=feedback )

class CannedFeedback( BaseModel ):
    objects = CannedFeedbackManager()

    feedback_type = models.CharField( max_length=32, choices=FEEDBACK_TYPES )
    feedback      = models.CharField( max_length=255 )
    order         = models.IntegerField( blank=True, default=999 )

    def __str__( self ):
        return '{self.feedback_type}::{self.feedback}'.format ( self=self )

    def natural_key( self ):
        return ( self.feedback_type, self.feedback )

    class Meta:
        ordering        = [ 'feedback_type', 'order', 'feedback' ]
        unique_together = ( 'feedback_type', 'feedback' )

# -----

class CategoryManager( models.Manager ):

    def get_by_natural_key( self, parent, name ):
        return self.get( parent=parent, name=name )

class Category( BaseModel ):
    objects = CategoryManager()

    parent          = models.ForeignKey( 'self', on_delete=models.PROTECT, null=True, blank=True )
    name            = models.CharField( max_length=256 )
    score           = models.IntegerField( default=0 , blank=True )
    is_correct      = models.BooleanField( blank=True, default=True )
    action_category = models.BooleanField( blank=True, default=False )

    def __str__( self ):
        parent = self.parent or ''
        return '{parent}::{self.name}'.format ( self=self, parent=parent )

    def natural_key( self ):
        return ( self.parent, self.name )

    @property
    def level( self ):

        def get_parent( obj, i ):
            if not obj.parent:
                return i
            return get_parent( obj.parent, i + 1 )

        return get_parent( self, 0 )

    @property
    def total_scores( self ):
        return sum( item.score for item in self.category_set.all() )

    class Meta:
        verbose_name_plural = 'Categories'
        ordering        = ( 'parent__name', 'name' )
        unique_together = ( 'parent', 'name' )

# -----

class ChatMessageManager( models.Manager ):

    def get_by_natural_key( self, invitation, user, time ):
        return self.get( invitation=invitation, user=user, time=time )

class ChatMessage( BaseModel ):
    objects = ChatMessageManager()

    invitation  = models.ForeignKey( 'Invitation', on_delete=models.PROTECT )
    user        = models.ForeignKey( User, on_delete=models.PROTECT )
    team        = models.CharField( max_length=32, default='' )
    message     = models.TextField()
    time        = models.DateTimeField()

    def __str__( self ):
        return '{self.invitation}::{self.user}::{self.time}'.format ( self=self )

    def natural_key( self ):
        return ( self.invitation, self.user, self.time )

    class Meta:
        ordering        = ( 'invitation', 'time', 'user' )
        unique_together = ( 'invitation', 'user', 'time' )

# -----

class CheckerScoreType( ReferenceDataModel ):
    min_score = models.IntegerField()
    max_score = models.IntegerField()

# -----

class City( ReferenceDataModel ):
    class Meta( ReferenceDataModel.Meta ):
        verbose_name_plural = 'Cities'

# -----

class Context( ReferenceDataModel ):
    pass

# -----

class Curriculum( ReferenceDataModel ):
    class Meta( ReferenceDataModel.Meta ):
        verbose_name_plural = 'Curricula'

# -----

class Cost( ReferenceDataModel ):
    class Meta( ReferenceDataModel.Meta ):
        ordering = [ 'order', 'id' ]

# -----

class Duration( ReferenceDataModel ):
    class Meta( ReferenceDataModel.Meta ):
        ordering = [ 'order', 'id' ]

# -----

class Execution( ReferenceDataModel ):
    pass

# -----

class FeedbackManager( models.Manager ):

    def get_by_natural_key( self, user, created ):
        return self.get( user=user, created=created )

class Feedback( BaseModel ):
    objects     = FeedbackManager()
    user        = models.ForeignKey( User, on_delete=models.PROTECT )
    feedback    = models.TextField()

    def __str__( self ):
        return '{self.user.username}::{self.created}'.format ( self=self )

    def natural_key( self ):
        return ( self.user, self.created )

    class Meta:
        ordering = [ '-created' ]

# -----

class InvitationManager( models.Manager ):

    def get_by_natural_key( self, inviter, title, created ):
        return self.get( inviter__username=inviter, activity__title=title, created=created )

    def get_check_incomplete( self ):
        return self.filter(
            date_checked__isnull=True,
            activity__checker__isnull=False,
        ).order_by(
            'inviter',
            'deadline',
            'activity__checker',
            'created',
        )

    def get_expired( self ):
        now   = datetime.datetime.now()
        now   = now.combine( now, datetime.time( 0, 0 ) )
        today = timezone.make_aware( now )
        return self.filter(
            date_completed__isnull=True,
            deadline__lt = today,
        ).order_by(
            'inviter',
            'deadline',
            'created',
        )

class Invitation( BaseModel ):
    objects         = InvitationManager()

    inviter         = models.ForeignKey ( User,     on_delete=models.PROTECT )
    activity        = models.ForeignKey ( Activity, on_delete=models.PROTECT )
    start_date      = models.DateTimeField( blank=True, null=True )
    deadline        = models.DateTimeField( blank=True, null=True )
    invitees        = JSONField( default=dict )
    date_completed  = models.DateTimeField( blank=True, null=True )
    date_checked    = models.DateTimeField( blank=True, null=True )

    def __str__( self ):
        return '{self.inviter}::{self.activity}::{self.created}'.format ( self=self )

    def natural_key( self ):
        return ( self.inviter.username, self.activity.title, self.created )

    class Meta:
        ordering        = [ 'inviter', 'created', 'activity' ]
        unique_together = ( 'created', 'inviter', 'activity' )

    def checked( self ):
        users = self.invitees.get( 'checked', {} )
        if not len( users.keys() ):
            return false
        return all( users.values() )

    def completed( self ):
        users = self.invitees.get( 'completed', {} )
        if not len( users.keys() ):
            return false
        return all( users.values() )

# -----

class Job( ReferenceDataModel ):
    pass

# -----

class LearningJournalManager( models.Manager ):

    def get_by_natural_key( self, user_id, created, title ):
        return self.get( user_id=user_id, created=created, title=title )

class LearningJournal( BaseModel ):
    objects     = LearningJournalManager()
    user        = models.ForeignKey( User, on_delete=models.PROTECT )
    title       = models.CharField( max_length=500 )
    text        = models.TextField()
    questions   = JSONField( default=list, blank=True )

    def __str__( self ):
        return '{self.user.username}::{self.created}::{self.title}'.format ( self=self )

    def natural_key( self ):
        return ( self.user_id, self.created, self.title )

    class Meta:
        ordering = [ '-created' ]

# -----

class LearningObjective( ReferenceDataModel ):
    pass

# -----

class LearningOutcomeVerbManager( models.Manager ):

    def get_by_natural_key( self, category, verb ):
        return self.get( category=category, verb=verb )

class LearningOutcomeVerb( BaseModel ):
    objects     = LearningOutcomeVerbManager()

    category    = models.CharField( max_length=32, choices=LEARNING_OUTCOME_CATEGORIES )
    verb        = models.CharField( max_length=255 )
    order       = models.IntegerField( blank=True, default=999 )

    def __str__( self ):
        return '{self.category}::{self.verb}'.format ( self=self )

    def natural_key( self ):
        return ( self.category, self.verb )

    class Meta:
        ordering        = [ 'category', 'order', 'verb' ]
        unique_together = ( 'category', 'verb' )

# -----

class LocationManager( models.Manager ):

    def get_by_natural_key( self, city, name ):
        return self.get( city=city, name=name )

class Location( BaseModel ):
    objects             = LocationManager()

    name                = models.CharField      ( max_length=255 )
    order               = models.IntegerField   ( blank=True, default=999 )
    city                = models.ForeignKey     ( 'City', on_delete=models.PROTECT )
    address             = models.TextField      ( blank=True, null=True )
    tel_no              = models.CharField      ( max_length=255, default='' )
    website             = models.URLField       ( blank=True, null=True )
    latitude            = models.FloatField     ( blank=True, null=True )
    longitude           = models.FloatField     ( blank=True, null=True )
    contact_name        = models.CharField      ( max_length=255, blank=True, default='' )
    contact_email       = models.EmailField     ( blank=True, default='' )
    contact_cell_no     = models.CharField      ( max_length=255, blank=True, default='' )
    comments            = models.TextField      ( blank=True, default='' )
    interactions_log    = models.TextField      ( blank=True, default='' )
    next_steps          = models.TextField      ( blank=True, default='' )


    def __str__( self ):
        return '{self.city}::{self.name}'.format ( self=self )

    def natural_key( self ):
        return ( self.city, self.name )

    class Meta:
        ordering        = [ 'city', 'order', 'name' ]
        unique_together = ( 'name', 'city' )

# -----

class QuestionTypeManager( models.Manager ):
    def get_by_natural_key( self, validation_type, name ):
        return self.get( validation_type=validation_type, name=name )

class QuestionType( BaseModel ):
    objects         = QuestionTypeManager()

    name            = models.CharField( max_length=255 )
    order           = models.IntegerField( blank=True, default=999 )
    validation_type = models.ForeignKey ( 'ValidationType', on_delete=models.PROTECT )

    def __str__( self ):
        return '%s (%s)' % ( self.name, self.validation_type.name )

    def natural_key( self ):
        return ( self.validation_type, self.name )

    class Meta:
        ordering        = ( 'validation_type', 'order', 'name' )
        unique_together = ( 'validation_type', 'name' )

# -----

class SequenceType( ReferenceDataModel ):
    pass

# -----

class Situation( ReferenceDataModel ):
    pass

# -----

class Skill( ReferenceDataModel ):
    pass

# -----

class Subject( ReferenceDataModel ):
    pass

# -----

class ValidationType( ReferenceDataModel ):
    pass

# -----

def default_UserActivityState():
    return UserActivityState.get_or_create_enrolled().id

class UserActivityBase( BaseModel ):

    user                = models.ForeignKey ( User,                on_delete=models.PROTECT )
    activity            = models.ForeignKey ( 'Activity',          on_delete=models.PROTECT )
    state               = models.ForeignKey ( 'UserActivityState', on_delete=models.PROTECT, default=default_UserActivityState )
    invitation          = models.ForeignKey ( 'Invitation',        on_delete=models.PROTECT, blank=True, null=True, default=None )
    started             = models.DateTimeField( blank=True, null=True )
    completed           = models.DateTimeField( blank=True, null=True, verbose_name='Date completed' )
    date_checked        = models.DateTimeField( blank=True, null=True )
    completed_question  = models.IntegerField ( blank=True, default=-1 )
    comment             = models.TextField    ( blank=True, null=True )
    date_commented      = models.DateTimeField( blank=True, null=True )
    team                = models.CharField    ( max_length=30, blank=True, null=True )
    answers             = JSONField( default=dict, blank=True )
    answer_attempts     = JSONField( default=dict, blank=True )
    uploads             = JSONField( default=dict, blank=True )
    actions             = JSONField( default=dict, blank=True )
    scores              = JSONField( default=dict, blank=True )

    def __str__( self ):
        return '{self.user}::{self.activity}'.format( self=self )

    class Meta:
        abstract = True


class UserActivityManager( models.Manager ):
    def get_natural_key( self, username, activity_title ):
        return self.get( user__username=username, activity__title=activity_title )


class UserActivity( UserActivityBase ):
    objects = UserActivityManager()

    def natural_key( self ):
        return ( self.user.username, self.activity.title )

    class Meta:
        verbose_name_plural = 'User activities'
        unique_together     = ( 'user', 'activity' )
        ordering            = ( 'user', 'activity' )


class UserActivityArchive( UserActivityBase ):
    archive_date = models.DateTimeField ( auto_now_add=True )

# -----

class UserActivityJournalManager( models.Manager ):
    def get_natural_key( self, user_activity_id ):
        return self.get( user_activity_id=user_activity_id )

class UserActivityJournal( BaseModel ):
    objects       = UserActivityJournalManager()
    user_activity = models.OneToOneField( UserActivity, on_delete=models.PROTECT )
    text          = models.TextField()

    def __str__( self ):
        return str( self.user_activity )

    def natural_key( self ):
        return self.user_activity.id

    class Meta:
        ordering = ( 'user_activity', )

# -----

class UserActivityState( ReferenceDataModel ):

    @classmethod
    def get_or_create_completed( cls ):
        return cls.objects.get_or_create( name = 'Completed' )[0]

    @classmethod
    def get_or_create_enrolled( cls ):
        return cls.objects.get_or_create( name = 'Enrolled' )[0]

    @classmethod
    def get_or_create_started( cls ):
        return cls.objects.get_or_create( name = 'Started' )[0]

# -----

class UserActivityToDoManager( models.Manager ):

    def get_by_natural_key( self, user_activity_id, question_no ):
        return self.get( user_activity_id=user_activity_id, question_no=question_no )

class UserActivityToDo( BaseModel ):
    objects = UserActivityToDoManager()

    user_activity   = models.ForeignKey( 'UserActivity',on_delete=models.PROTECT, null=True, blank=True )
    question_no     = models.IntegerField( null=True, blank=True )
    description     = models.TextField()
    deadline        = models.DateTimeField()
    status          = models.CharField( max_length=30, choices=TODO_STATUSES, default='in-progress' )
    category        = models.ForeignKey( 'Category',on_delete=models.PROTECT, null=True, blank=True )
    notes           = models.TextField( null=True, blank=True )
    user            = models.ForeignKey( User, on_delete=models.PROTECT )

    def __str__( self ):
        return '{self.user}::{self.description}'.format ( self=self )

    def natural_key( self ):
        return ( self.user_activity.id, self.question_no )

    class Meta:
        ordering        = ( 'deadline', 'user_activity', 'question_no' )
        unique_together = ( 'user_activity', 'question_no' )

# -----

class UserProfileManager( models.Manager ):
    def get_natural_key( self, username ):
        return self.get( user__username=username )

class UserProfile( BaseModel ):
    objects             = UserProfileManager()

    user                = models.OneToOneField( User, on_delete=models.CASCADE )
    change_password     = models.BooleanField( blank=False, default=False )
    scores              = JSONField( default=dict, blank=True )

    def __str__( self ):
        return '{self.user}'.format( self=self )

    def natural_key( self ):
        return ( self.user.username )

