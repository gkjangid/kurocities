from    django.http             import JsonResponse, Http404, HttpResponseForbidden
from    django.http.request     import RawPostDataException
from    functools               import wraps
from    json.decoder            import JSONDecodeError
from    ..                      import models
import  json

from pdb import set_trace as st


class CorsJsonResponse( JsonResponse ):

    def __init__(
        self,
        content=b'',
        allow_origin='*',
        json_dumps_params={ 'indent': 2 },
        *args,
        **kwargs,
    ):
        kwargs ['json_dumps_params'] = json_dumps_params
        super( CorsJsonResponse, self ).__init__( content, *args, **kwargs )
        self ['Access-Control-Allow-Origin']      = allow_origin
        self ['Access-Control-Allow-Credentials'] = 'true'


def calculate_total_scores( questions, activity_scores ):

    def get_type_scores( total_scores, score_type, sub_types, question_score ):
        if not isinstance( sub_types, list ):
            sub_types = [sub_types]
        for sub_type in sub_types:
            total_scores.setdefault( sub_type, [ 0, 0 ] )
            total_scores [sub_type] [0] += question_score[ 0 ] # scores obtained
            total_scores [sub_type] [1] += question_score[ 1 ] # max scores
        return total_scores

    # -----

    activity_scores = activity_scores or {}
    activity_questions_scores = activity_scores.get( 'questions', {} )

    for questionIdx, question in enumerate( questions ):
        try:
            question_score = activity_questions_scores [str( questionIdx )]
        except:
            question_score = activity_questions_scores [questionIdx]

        if question_score is not None:
            for score_type in [ 'skill', 'subjects' ]:
                sub_types = question.get( score_type, [] )
                activity_scores[ score_type ] = get_type_scores(
                    question_score  = question_score,
                    score_type      = score_type,
                    sub_types       = sub_types,
                    total_scores    = activity_scores.get( score_type, {} ),
                )
    return activity_scores


def cors_json_response( request, data, **kwargs ):
    if not 'allow_origin' in kwargs:
        allow_origin = '*'
        if hasattr( request, 'META' ):
            allow_origin = request.META.get( 'HTTP_ORIGIN', '*' )
        kwargs ['allow_origin'] = allow_origin
    return CorsJsonResponse( data, **kwargs )


def get_basic_activity_info( queryset ):
    return [
        {
            "pk":           x.pk,
            "title":        x.title,
            "modified":     x.modified,
            "description":  x.data.get( 'briefDescription', '' ),
            "pictureUrl":   x.data.get( 'pictureUrl',  '' ),
            "locations":    x.data.get( 'locations', [] ),
            "fromDate":     x.data.get( 'fromDate', '' ),
            "toDate":       x.data.get( 'toDate', '' ),
            "fromTime":     x.data.get( 'fromTime', '' ),
            "toTime":       x.data.get( 'toTime', '' ),
            "duration":     x.data.get( 'duration' ),
            "cost":         x.data.get( 'cost' ),
            "situation":    x.data.get( 'situation' ),
            "datesComment": x.data.get( 'datesComment' ),
            "timesComment": x.data.get( 'timesComment' ),
            "status":       x.data.get( 'status' ),
        }
        for x in queryset
    ]


def get_post_data( request ):
    try:
        return json.loads( request.body.decode('utf-8') )
    except ( RawPostDataException, JSONDecodeError, UnicodeDecodeError ):
        return request.POST.dict()


def group_access( group ):
    if not isinstance( group, list ):
        group = [group]

    def decorator( func ):
        @wraps( func )
        def wrapper( self, request, *args, **kwargs ):
            if not request.user.groups.filter( name__in=group ):
                return HttpResponseForbidden( group )
            return func( self, request, *args, **kwargs )
        return wrapper
    return decorator


def update_user_profile( user ):
    user_profile, created = models.UserProfile.objects.get_or_create( user = user )
    scores = {}

    for user_activity in models.UserActivity.objects.filter( user = user ):

        for score_type, activity_scores in user_activity.scores.items():
            if score_type == 'questions':  continue
            scores.setdefault( score_type, {} )
            user_type_score = scores[ score_type ]

            for key, score in activity_scores.items():
                user_type_score.setdefault( key, [ 0, 0 ] )
                if isinstance( score[0], str ) and score[0].strip() == '':
                    continue
                user_type_score [key] [0] += int( score [0] ) # scores obtained
                user_type_score [key] [1] += int( score [1] ) # max scores

    user_profile.scores = scores
    user_profile.save()
