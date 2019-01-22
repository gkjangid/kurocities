from django.http                    import Http404
from django.shortcuts               import get_object_or_404, render
from django.views                   import View

from .                              import models
from .apiviews.base                 import group_access

from datetime                       import datetime
from pdb                            import set_trace as st


class Data( View ):

    @group_access([ 'KCT-Activity-Data' ])
    def get( self, request, resource_type, resource_id, *args, **kwargs ):
        try:
            handler = getattr( self, resource_type )
        except AttributeError:
            raise Http404
        return handler( request, resource_id )


    def invitation( self, request, resource_id ):

        def row_get( data, index, default='' ):
            try:
                return data [index]
            except IndexError:
                return default

        invitation          = get_object_or_404( models.Invitation, pk=resource_id )
        activity            = invitation.activity
        activity_questions  = activity.data ['questions']
        user_activities     = ( models.UserActivity.objects
            .filter( invitation=invitation )
            .order_by( 'team', 'user__username' )
        )
        questions = []

        for index, question in enumerate( activity_questions ):
            index   = str( index )
            answers = []

            for user_activity in user_activities:

                answer = user_activity.answers.get( index, '' )
                if question ['questionType'] == 'table':
                    table_answers = []
                    for row_no, row_info in enumerate( question ['table'] ['rows'] ):
                        row_data = [ row_info ['label'] ]
                        row_data.extend( row_get( answer, row_no, [] ) )
                        table_answers.append( row_data )
                    answer = table_answers

                elif question ['questionType'] == 'multipleChoice':
                    try:
                        choice = question ['choices'] [ int(answer) ]
                        answer = choice.get( 'choice', '' )
                    except ValueError:
                        answer = ''

                answers.append({
                    'user':     user_activity.user.username,
                    'team':     user_activity.team,
                    'answer':   answer,
                    'upload':   user_activity.uploads.get( index ),
                })

            questions.append({
                 'question':    question ['question'],
                 'answers':     answers,
                 'data':        question,
            })

        response = render( request, 'data/invitation.html', locals() )
        title    = activity.title.replace( ' ', '_' )
        time     = datetime.now().strftime( '%Y%m%d-%H%M' )
        response ['Content-Disposition'] = 'attachment; filename="%s-%s.html"' % ( title, time )
        return response


class Image( View ):

    def get( self, request ):
        image = request.GET ['i']
        return render( request, 'image.html', locals() )
