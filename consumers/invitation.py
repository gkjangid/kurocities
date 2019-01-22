from   asgiref.sync                 import async_to_sync
from   channels.db                  import database_sync_to_async
from   channels.generic.websocket   import AsyncWebsocketConsumer, WebsocketConsumer
from   django.core.serializers.json import DjangoJSONEncoder
from   django.forms                 import model_to_dict
from   django.utils                 import timezone as datetime
from   django.utils.dateparse       import parse_datetime
from   ..                           import models

import asyncio
import json
import logging

# from   django.forms.models          import model_to_dict
from   pprint                       import pformat

__all__ = [ 'InvitationConsumer' ]


def file_logger( data, filename='consumer.log' ):
    with open( filename, 'a' ) as f:
        f.write( '%s' % data )
        f.write( '\n' )


class InvitationConsumerAsync( AsyncWebsocketConsumer ):

    async def connect( self ):
        self.invitation_id = self.scope ['url_route'] ['kwargs'] ['invitation_id']
        self.team          = self.scope ['url_route'] ['kwargs'].get( 'team_name' )

        get_invitation = self.get_invitation( self.invitation_id )

        group_add = self.channel_layer.group_add(
            f'invitation.{self.invitation_id}',
            self.channel_name,
        )

        await asyncio.wait([
            group_add,
            get_invitation,
        ])

        await self.accept()


    async def chat_message( self, event ):
        if not self.manager_access:
            if event ['team'] and event ['team'] != self.team:
                return
        data = json.dumps( event, default=DjangoJSONEncoder )
        await self.send( data )


    async def disconnect( self, close_code ):
        await self.channel_layer.group_discard(
            f'invitation.{self.invitation_id}',
            self.channel_name,
        )


    @database_sync_to_async
    def get_invitation( self, invitation_id ):
        self.invitation = models.Invitation.objects.select_related().get(
            pk = int( invitation_id )
        )
        self.manager_access = self.is_manager( self.invitation )


    def is_manager( self, invitation ):
        if invitation.inviter == self.scope ['user']:
            return True
        if invitation.activity.data ['coach'] == self.scope ['user'].username:
            return True


    async def receive( self, text_data ):
        data = json.loads( text_data )
        data ['type']     = 'chat_message'
        data ['fromUser'] = self.scope ['user'].username
        data ['time']     = datetime.now().isoformat()
        await self.channel_layer.group_send(
            f'invitation.{self.invitation_id}',
            data,
        )
        await self.save_message( data )


    @database_sync_to_async
    def save_message( self, data ):
        models.ChatMessage.objects.create(
            invitation_id   = self.invitation_id,
            user            = self.scope ['user'],
            team            = data.get( 'team' ) or '',
            message         = data ['message'],
            time            = parse_datetime( data ['time'] ),
        )



InvitationConsumer = InvitationConsumerAsync
