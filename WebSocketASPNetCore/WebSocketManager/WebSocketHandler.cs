using Microsoft.AspNetCore.Http;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.WebSockets;
using System.Text;
using System.Threading;
using System.Threading.Tasks;

namespace WebSocketASPNetCore.WebSocketManager
{
    public abstract class WebSocketHandler
    {
        protected abstract int BufferSize { get; }

        private List<WebSocketConnection> _connections = new List<WebSocketConnection>();

        public List<WebSocketConnection> Connections { get => _connections; }

        public async Task ListenConnection(WebSocketConnection connection)
        {
            var buffer = new byte[BufferSize];

            while (connection.WebSocket.State == WebSocketState.Open)
            {
                WebSocketReceiveResult result = null;
                List<byte> bytes = new List<byte>();
                try
                {
                    do
                    {
                        result = await connection.WebSocket.ReceiveAsync(
                            buffer: new ArraySegment<byte>(buffer),
                            cancellationToken: CancellationToken.None);
                        bytes.AddRange(buffer.Take(result.Count));
                    } while (!result.EndOfMessage);


                    if (result.MessageType == WebSocketMessageType.Text)
                    {
                        var message = Encoding.UTF8.GetString(bytes.ToArray(), 0, bytes.Count);
                        bytes = null;
                        await connection.ReceiveAsync(message);
                    }
                    else if (result.MessageType == WebSocketMessageType.Close)
                    {
                        await OnDisconnected(connection);
                    }
                }
                catch (InvalidOperationException e)
                {

                }
            }
            await OnDisconnected(connection);
        }

        public virtual async Task OnDisconnected(WebSocketConnection connection)
        {
            if (connection != null)
            {
                _connections.Remove(connection);
                if (connection.WebSocket.State != WebSocketState.Closed && connection.WebSocket.State != WebSocketState.Aborted)
                {
                    await connection.WebSocket.CloseAsync(
                        closeStatus: WebSocketCloseStatus.NormalClosure,
                        statusDescription: "Closed by the WebSocketHandler",
                        cancellationToken: CancellationToken.None);
                }
            }
        }

        public abstract Task<WebSocketConnection> OnConnected(HttpContext context);
    }
}
