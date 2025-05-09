# Django Imports
import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from asgiref.sync import sync_to_async
from django.utils.timezone import make_aware
from datetime import datetime

# Project Imports
from apps.reader_leak.models import FlowRating
from apps.reader_leak.serializers import FlowReadingSerializer

# WebSocket consumer class for handling flow readings
class FlowReadingConsumer(AsyncJsonWebsocketConsumer):

    # Method called when a WebSocket connection is established
    async def connect(self):

        # Define the WebSocket group name
        self.reader_name = 'reader_leak'
        self.reader_group_name = f"channel_{self.reader_name}"

        # Add the WebSocket connection to the group
        await self.channel_layer.group_add(
            self.reader_group_name,
            self.channel_name
        )

        # Accept the WebSocket connection
        await self.accept()

    # Method called when a WebSocket connection is closed
    async def disconnect(self, close_code):  

        # Remove the WebSocket connection from the group
        await self.channel_layer.group_discard(
            self.reader_group_name,
            self.channel_name
        )

    # Method called when a message is received from the WebSocket
    async def receive(self, text_data):

        # Parse the received data as JSON
        flow_data_json = json.loads(text_data)

        # Log the received data
        print(f"Received data: {flow_data_json}")

        # Extract the flow rate and times_tamp from the received data
        flow_rate = flow_data_json.get('flow_rate')
        times_tamp_str = flow_data_json.get('times_tamp')

        # Check if the required fields are present
        if flow_rate is None or times_tamp_str is None:
            print("Error: 'flow_rate' not found in data")
            return
        
        try:

            dt = datetime.strptime(times_tamp_str, "%d/%m/%Y %H:%M:%S")

            aware_dt = make_aware(dt)

            # Create a new flow reading record in the database
            flow_reading = await create_flow_reading(
                flow_rate=flow_rate,
                times_tamp=aware_dt
            )

            # Serialize the flow reading record
            serializer = FlowReadingSerializer(instance=flow_reading)

            # Prepare the serialized data to be sent
            message = serializer.data

            # Send the flow reading to the WebSocket group
            await self.channel_layer.group_send(
                self.reader_group_name,
                {
                    'type': 'send_flow_reading',  # Event type
                    'message': message           # Serialized data
                }
            )

        except Exception as e:
            # Log any errors that occur
            print(f"Error: {e}")
            return

    # Method to send messages from the group back to the WebSocket
    async def send_flow_reading(self, event):

        # Extract the message from the event
        message = event['message']

        # Send the message back to the WebSocket
        await self.send(
            text_data=json.dumps({
                'message': message
            })
        )

# Function to create a flow reading record in the database (sync-to-async wrapper)
@sync_to_async
def create_flow_reading(flow_rate, times_tamp):
    # Create and return a new FlowRating record
    return FlowRating.objects.create(flow_rate=flow_rate, times_tamp=times_tamp)