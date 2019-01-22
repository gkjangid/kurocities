from django.contrib     import admin
from kuriocities.models import *

import logging


admin.site.site_header = 'KurioCities DB administration'
admin.site.site_title  = 'KurioCities DB admin'


class WithUserModelAdmin( admin.ModelAdmin ):

    def save_model( self, request, obj, form, change ):
        if not change:
            obj.created_by = request.user
        obj.modified_by = request.user
        super( WithUserModelAdmin, self).save_model( request, obj, form, change )



class ActivityAdmin( admin.ModelAdmin ):
    list_display = ( 'title', 'id', 'created_by', 'status', 'modified' )
    list_filter  = ( 'created_by', )

    def status( self, obj ):
        return obj.data['status']


class AnswerScoreAdminInline( admin.TabularInline ):
    model   = AnswerScore

class AnswerScoreTypeAdmin( admin.ModelAdmin ):
    inlines = [ AnswerScoreAdminInline ]


class AppFeatureAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'enabled' )


class CategoryAdminInline( admin.TabularInline ):
    model   = Category

class CategoryAdmin( admin.ModelAdmin ):
    inlines = [ CategoryAdminInline ]
    list_display  = ( 'name', 'level', 'parent' )
    search_fields = ( 'name', )


class ChatMessageAdmin( admin.ModelAdmin ):
    list_display = ( 'invitation', 'team', 'time' )
    list_filter  = ( 'invitation__inviter', 'team', 'invitation__activity' )


class InvitationAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'inviter', 'activity', 'created', 'start_date', 'deadline', 'date_completed', 'date_checked' )
    list_filter  = ( 'inviter', 'activity' )


class LearningOutcomeVerbAdmin( admin.ModelAdmin ):
    list_display = ( 'category', 'verb' )
    list_filter  = ( 'category', )


class LocationAdmin( admin.ModelAdmin ):
    list_display = ( 'name', 'city', 'address', 'website', 'tel_no', 'contact_name', 'contact_cell_no' )
    list_filter  = ( 'city', )


class QuestionTypeAdmin( admin.ModelAdmin ):
    list_display = ( 'validation_type', 'name' )

class UserActivityAdmin( admin.ModelAdmin ):
    list_display = ( 'id', 'activity', 'user', 'inviter', 'state', 'started', 'completed' )
    list_filter  = ( 'user', 'state' )

    def inviter( self, obj ):
        return obj.invitation.inviter if obj.invitation else ''


admin.site.register( Activity,              ActivityAdmin )
admin.site.register( AnswerScoreType,       AnswerScoreTypeAdmin )
admin.site.register( AgeGroup               )
admin.site.register( AppFeature,            AppFeatureAdmin )
admin.site.register( CannedFeedback         )
admin.site.register( Category,              CategoryAdmin )
admin.site.register( ChatMessage,           ChatMessageAdmin )
admin.site.register( CheckerScoreType       )
admin.site.register( City                   )
admin.site.register( Context                )
admin.site.register( Curriculum             )
admin.site.register( Cost                   )
admin.site.register( Duration               )
admin.site.register( Execution              )
admin.site.register( Feedback               )
admin.site.register( Invitation,            InvitationAdmin )
admin.site.register( Job                    )
admin.site.register( LearningJournal        )
admin.site.register( LearningObjective      )
admin.site.register( LearningOutcomeVerb,   LearningOutcomeVerbAdmin )
admin.site.register( Location,              LocationAdmin     )
admin.site.register( QuestionType,          QuestionTypeAdmin )
admin.site.register( SequenceType           )
admin.site.register( Situation              )
admin.site.register( Skill                  )
admin.site.register( Subject                )
admin.site.register( ValidationType         )
admin.site.register( UserActivity,          UserActivityAdmin )
admin.site.register( UserActivityArchive,   UserActivityAdmin )
admin.site.register( UserActivityJournal )
admin.site.register( UserActivityState      )
admin.site.register( UserActivityToDo       )
admin.site.register( UserProfile )
