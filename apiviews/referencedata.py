from django.contrib.auth.models     import Group
from django.views                   import View
from .base                          import cors_json_response, group_access
from .activity                      import Activity_Get_V1
from ..                             import models

class ReferenceData_V1( View ):

    @group_access( 'KCT-Creator' )
    def get( self, request, *args, **kwargs ):
        return cors_json_response( request, {
            'activities':                   Activity_Get_V1().getlist_data( request, order='-modified' ),
            'ageGroups':                    self.get_model_data( models.AgeGroup ),
            'cannedFeedbacks':              self.get_model_data( models.CannedFeedback ),
            'cities':                       self.get_model_data( models.City ),
            'contexts':                     self.get_model_data( models.Context ),
            'costs':                        self.get_model_data( models.Cost ),
            'durations':                    self.get_model_data( models.Duration ),
            'executions':                   self.get_model_data( models.Execution ),
            'jobs':                         self.get_model_data( models.Job ),
            'learningOutcomeCategories':    models.LEARNING_OUTCOME_CATEGORIES,
            'locations':                    self.get_model_data( models.Location ),
            'situations':                   self.get_model_data( models.Situation ),
            'skills':                       self.get_model_data( models.Skill ),
            'subjects':                     self.get_model_data( models.Subject ),
            'userGroups':                   self.get_user_groups( request ),
            'validationTypes':              self.get_model_data( models.ValidationType ),
            'verbs':                        self.get_model_data( models.LearningOutcomeVerb ),
        })

    def get_model_data( self, model ):
        return list( model.objects.all().values() )

    def get_user_groups( self, request ):
        data = []
        queryset = request.user.groups.all().prefetch_related( 'user_set' )
        values   = queryset.values()
        for group, group_data in zip( queryset, values ):
            group_data ['users'] = [
                {
                    "username": user.username,
                    "fullname": user.get_full_name(),
                }
                for user in group.user_set.all()
            ]
            data.append( group_data )
        return data
