from    django.core.mail    import EmailMessage
from    django.db           import transaction
from    django.http         import Http404, HttpResponse
from    django.views        import View
from    django.utils        import timezone

from    project             import settings
from    .base               import calculate_total_scores, cors_json_response, get_post_data, update_user_profile
from    ..                  import models

from    datetime            import datetime
import  json
import  logging
import  os

class UserActivityAction_V1( View ):

    def create_todo( self, request, user_activity ):
        todos = []
        for idx, question in enumerate( user_activity.activity.data ['questions'] ):
            if not question ['questionType'] == 'action': continue
            answers = user_activity.answers
            answer = user_activity.answers [str(idx)]
            todos.append( models.UserActivityToDo(
                user_activity = user_activity,
                question_no   = idx,
                description   = answer ['answer'],
                deadline      = datetime.strptime( answer ['deadline'], '%Y-%m-%d' )
            ))
        models.UserActivityToDo.objects.bulk_create( todos )


    def get_activity_scores( self, request, activity, user_activity ):

        def get_answer_score_table( question, answer_score_table_cache ):
            score_type = question.get( 'answerScoreType', 'Default' )
            if score_type in answer_score_table_cache:
                return answer_score_table_cache [score_type], answer_score_table_cache

            answer_score_type, created = models.AnswerScoreType.objects.get_or_create( name = score_type )
            answer_score_table = {
                item[ 'attempt_no' ]: item[ 'score' ]
                for item in answer_score_type.answerscore_set.order_by( 'attempt_no' ).values()
            }
            if not len( answer_score_table ) and score_type == 'Default':
                answer_score_table = { 1: 10 }
            answer_score_table_cache [score_type] = answer_score_table
            return answer_score_table, answer_score_table_cache


        def get_question_score( questionIdx, question, user_activity, answer_score_table_cache ):
            answer_score_table, answer_score_table_cache = get_answer_score_table( question, answer_score_table_cache )
            attempt_no = user_activity.answer_attempts.get( str( questionIdx ) )

            if question ['questionType'] == 'upload':
                return [ 0, 0 ]

            if question ['questionType'] == 'noAutoCorrection':
                if question.get( 'needsChecker' ):
                    scores = user_activity.scores.get( 'questions', {} )
                    return scores.get( str( questionIdx ), [ 0, 10 ] )
                else:
                    return [ 0, 0 ]

            score     = answer_score_table.get( attempt_no, 0 )
            max_score = answer_score_table.get( 1, 0 )
            return [ score, max_score ]

        # -----

        answer_score_table_cache = {}
        questions = activity.data['questions']
        scores = {
            "questions": {},
        }

        for i, question in enumerate( questions ):
            question_score = get_question_score( i, question, user_activity, answer_score_table_cache )
            scores ['questions'] [str( i )] = question_score

        scores = calculate_total_scores( questions, scores )
        return scores


    def get_answer( self, activity, user_activity, questionIdx, data ):
        answer = data.get( 'answer', '' )
        if activity.data ['questions'] [questionIdx] ['questionType'] == 'table':
            answer = answer or '[]'
        return json.loads( answer )


    def get_answer_attempts( self, attempts, data ):
        if not isinstance( attempts, int ):
            attempts = 0
        isCorrect = json.loads( data.get( 'isCorrect', 'null' ) )
        if isCorrect is None: # isCorrect == None if no validation
            pass
        elif attempts <= 0: # negative attempts == incorrect attempts
            if isCorrect:
                return abs( attempts ) + 1
            else:
                return attempts - 1
        return attempts


    def get_upload( self, activity, user_activity, questionIdx, files ):
        if 'upload' not in files:
            return ''
        path = os.path.join(
            'UserActivity',
            str( user_activity.pk ),
            str( questionIdx ),
        )
        dir_path = os.path.join( settings.MEDIA_ROOT, path )
        os.makedirs( dir_path, exist_ok=True )
        filename = os.path.join( dir_path, 'uploadedFile' )
        with open( filename, 'wb' ) as f:
            for chunk in files['upload'].chunks():
                f.write( chunk )
        url = '%s%s/%s' % ( settings.MEDIA_URL, path, 'uploadedFile' )
        return url


    def get_steps( self, user_activity, action, question, answer, upload, now, data ):
        steps = user_activity.actions.get( 'steps', [] )
        step = {
            "action"    : action,
            "question"  : question,
            "answer"    : answer,
            "upload"    : upload,
            "datetime"  : now.isoformat(),
            "status"    : data.get( 'status' ),
        }
        steps.append( step )
        return steps


    def question_completed( self, request, user_activity, activity, questionIdx, date_time, answer, upload, data ):
        question_no = str( questionIdx )
        user_activity.answers        [ question_no ] = answer
        user_activity.uploads        [ question_no ] = upload
        user_activity.answer_attempts[ question_no ] = self.get_answer_attempts(
            user_activity.answer_attempts.get( question_no, 0 ),
            data,
        )
        if questionIdx > user_activity.completed_question:
            user_activity.completed_question = questionIdx

        if not user_activity.completed:
            if questionIdx == len( activity.data['questions'] ) - 1:
                user_activity.completed = date_time
                user_activity.state = models.UserActivityState.get_or_create_completed()
                self.update_invitation( request, user_activity, date_time )
                self.create_todo( request, user_activity )
        return user_activity


    def question_started( self, user_activity, activity, questionIdx, date_time ):
        if not user_activity.started:
            user_activity.started  = date_time
            user_activity.state = models.UserActivityState.get_or_create_started()
        return user_activity


    @transaction.atomic
    def post( self, request, resource_id, **kwargs ):
        data            = get_post_data( request )
        now             = timezone.now()
        activity        = models.Activity.objects.get( pk=resource_id )
        try:
            user_activity = models.UserActivity.objects.get(
                user     = request.user,
                activity = activity,
            )
        except models.UserActivity.DoesNotExist:
            raise Http404

        if user_activity.invitation:
            if user_activity.invitation.start_date:
                if user_activity.invitation.start_date > timezone.now():
                    return HttpResponse( 'Too early', status=403 )

        action      = data[ 'action' ]
        question_no = int( data[ 'question' ] )
        answer      = self.get_answer( activity, user_activity, question_no, data )
        upload      = self.get_upload( activity, user_activity, question_no, request.FILES )
        steps       = user_activity.actions[ 'steps' ] = (
            self.get_steps( user_activity, action, question_no, answer, upload, now, data )
        )
        is_last_question = question_no == len( activity.data['questions'] ) - 1

        if action == 'started':
            user_activity = self.question_started( user_activity, activity, question_no, now )
        elif action == 'completed':
            user_activity = self.question_completed(
                request       = request,
                user_activity = user_activity,
                activity      = activity,
                questionIdx   = question_no,
                date_time     = now,
                answer        = answer,
                upload        = upload,
                data          = data,
            )
            if is_last_question:
                user_activity.scores = self.get_activity_scores( request, activity, user_activity )

        user_activity.save()

        if action == 'completed' and is_last_question:
            update_user_profile( request.user ) # save user_activity before updating user_profile

        return cors_json_response( request, { 'data': steps[-1], 'scores': user_activity.scores } )


    def send_activity_completed_email( self, request, user_activity ):
        origin = request.META ['HTTP_ORIGIN']
        if user_activity.activity.checker:
            email = user_activity.activity.checker.email
            url = '%s/ae/#/checker-answers/invitation/%s' % ( origin, user_activity.invitation.id )
        else:
            email = user_activity.invitation.inviter.email
            url = '%s/ae/#/facilitator-activity/%s' % ( origin, user_activity.invitation.id )

        if not email:
            logging.error( 'No email address found for User-Activity: %s' % user_activity.id )
            return

        recipients = [ email ]
        title = user_activity.activity.title.strip()
        msg = EmailMessage(
            from_email = 'KurioCities<kuriocitiez@gmail.com>',
            to  = recipients,
            subject = 'Activity Completed: %s' % title,
            body = url,
        )
        logging.warn( 'Emailing to %s' % email )
        msg.send()

    def update_invitation( self, request, user_activity, date_time ):
        invitation = user_activity.invitation
        if invitation:
            username  = user_activity.user.username
            usernames = invitation.invitees.get( 'completed' )
            if username in usernames and not usernames [username]:
                usernames [username] = date_time.isoformat()
                if invitation.completed():
                    invitation.date_completed = date_time
                    self.send_activity_completed_email( request, user_activity )
                invitation.save()
