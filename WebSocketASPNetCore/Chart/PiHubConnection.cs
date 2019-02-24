using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using WebSocketASPNetCore.WebSocketManager;
using Newtonsoft.Json;
using Messaging.Messages;

namespace WebSocketASPNetCore.Chart
{
    public class PiHubConnection : WebSocketConnection
    {
        public PiHubConnection(WebSocketHandler handler, string channelid, string subscriberid, string key) : base(handler)
        {
            this.SubscriberId = subscriberid;
            this.ChannelId = channelid;
            this.Key = key;
        }

        public string ChannelId { get; set; }

        public string SubscriberId { get; set; }
        public string Key { get;  set; }

        public override async Task ReceiveAsync(string message)
        {
            var receiveMessage = JsonConvert.DeserializeObject<Message>(message);

            var receivers = Handler.Connections.Where(m => ((PiHubConnection)m).ChannelId==ChannelId && receiveMessage.Recipients.Contains(((PiHubConnection)m).SubscriberId));


            IEnumerable<WebSocketConnection> messageReceivers;
            if (receiveMessage.MessageType == MessageType.Broadcast)
            {
                messageReceivers = Handler.Connections.Where(q=> ((PiHubConnection)q).SubscriberId!=receiveMessage.Originator);
            }
            else
            {
                messageReceivers = receivers;
            }

            foreach (var receiver in messageReceivers)
            {
                receiveMessage.Originator=SubscriberId;
                await receiver.SendMessageAsync(receiveMessage);
            }
        }
    }
}