using System;
using Microsoft.AspNetCore.Http;
using System.Linq;
using System.Net.WebSockets;
using System.Threading;
using System.Threading.Tasks;
using Transport.Exceptions;
using WebSocketASPNetCore.WebSocketManager;

namespace WebSocketASPNetCore.Chart
{
    public class PiHubHandler : WebSocketHandler
    {
        protected override int BufferSize { get => 1024 * 1024 * 10; }
        public override async Task<WebSocketConnection> OnConnected(HttpContext context)
        {
            var channelId = context.Request.Query["channelId"];
            var subscriberId = context.Request.Query["subscriberId"];
            var key = context.Request.Query["key"];

            if (string.IsNullOrEmpty(subscriberId) || string.IsNullOrEmpty(channelId))
            {
                return null;
            }

            var connection = Connections.FirstOrDefault(m => ((PiHubConnection)m).ChannelId == channelId && ((PiHubConnection)m).SubscriberId == subscriberId);
            if (connection != null)
            {
                try
                {
                    await connection.WebSocket.CloseAsync(WebSocketCloseStatus.PolicyViolation,
                        "The connection was reused from the other client", CancellationToken.None);
                }
                catch (Exception e)
                {
                   
                }
                finally
                {
                    Connections.Remove(connection);
                }

                
            }

            if (Connections.Any(c => ((PiHubConnection)c).Key != key && ((PiHubConnection)c).ChannelId==channelId))
            {
                throw new NotAuthorizedException("provided key does not match the channel");
            }

            var webSocket = await context.WebSockets.AcceptWebSocketAsync();
            connection = new PiHubConnection(this, channelId, subscriberId, key)
            {
                WebSocket = webSocket
            };

            Connections.Add(connection);
            return connection;
        }
    }
}
