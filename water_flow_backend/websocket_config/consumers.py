# Django Imports
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from datetime import datetime
import pytz

# Project Imports
from apps.reader_leak.models import FlowRating
from apps.reader_leak.serializers import FlowReadingSerializer
class FlowReadginConsumer(AsyncJsonWebsocketConsumer):

    async def connect(self):

        # WebSocket group name
        self.reader_name = 'reader_leak'
        self.reader_group_name = f"channel_{self.reader_name}"

        # Adds the connection to the group
        await self.channel_layer.group_add(
            self.reader_group_name,
            self.channel_name
        )

        # Accepts the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):  

        # Removes the connection from the group
        await self.channel_layer.group_discard(
            self.reader_group_name,
            self.channel_name
        )

    async def receive(self, text_data):

        # Converts the received data stream into JSON
        flow_data_json = json.loads(text_data)

        print(f"Received data: {flow_data_json}")

        # Maps the received message field
        flow_rate = flow_data_json.get('flow_rate')
        timestamp_str = flow_data_json.get('timestamp')

        if flow_rate is None or timestamp_str is None:
            
            print("Error: 'flow_rate' not found in data")
            return
        
        try:

            flow_reading = await create_flow_reading(
                flow_rate=flow_rate,
                timestamp=timestamp_str
            )

            serializer = FlowReadingSerializer(instance=flow_reading)

            message = serializer.data


            # Sends the flow reading to the WebSocket group
            await self.channel_layer.group_send(
                self.reader_group_name,
                {
                    'type': 'send_flow_reading',
                    'message': message
                }
            )

        except Exception as e:
            print(f"Error: {e}")
            return

    # Function that receives messages from the group and sends them back to the WebSocket
    async def send_flow_reading(self, event):

        message = event['message']

        await self.send(
            text_data=json.dumps({
                'message': message
            })
        )

# Function to convert sync request to async
@sync_to_async
def create_flow_reading(flow_rate, timestamp):
    
    return FlowRating.objects.create(flow_rate=flow_rate, timestamp=timestamp)

