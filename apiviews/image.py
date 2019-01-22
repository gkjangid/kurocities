from    django.conf                 import settings
from    django.views                import View
from    .base                       import cors_json_response, get_post_data
from    ..                          import models
import os
import time

from pdb import set_trace as st
import logging


class Image_V1( View ):

    def _get_upload( self, request, files ):
        if not len( files.keys() ): return 400
        upload_path = os.path.join( 'UserImage', str( request.user.id ) )
        disk_path   = os.path.join( settings.MEDIA_ROOT, upload_path )
        os.makedirs( disk_path, exist_ok=True )

        uploads = {}
        for name, uploadedFile in files.items():
            filename  = str( time.time() )
            file_path = os.path.join( disk_path, filename )
            with open( file_path, 'wb' ) as f:
                for chunk in files[ name ].chunks():
                    f.write( chunk )
            uploads [name] = os.path.join( settings.MEDIA_URL, upload_path, filename )
        return uploads


    def post( self, request, **kwargs ):
        data    = get_post_data( request )
        uploads = self._get_upload( request, request.FILES )
        if isinstance( uploads, int ):
            return cors_json_response( '', status=uploads )
        return cors_json_response( request, { 'uploads': uploads } )
