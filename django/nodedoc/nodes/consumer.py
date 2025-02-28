import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NodeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("nodes", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("nodes", self.channel_name)

    async def send_nodes_update(self, event):
        await self.send(text_data=json.dumps(event["nodes"])) 