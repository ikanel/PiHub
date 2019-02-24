using Microsoft.AspNetCore.Http;
using System.Threading.Tasks;
using Transport.Exceptions;

namespace WebSocketASPNetCore.WebSocketManager
{
    /// <summary>
    /// This should the last middleware in the pipeline when use websocket
    /// </summary>
    public class WebSocketMiddleware
    {
        private readonly RequestDelegate _next;
        private WebSocketHandler _webSocketHandler { get; set; }

        public WebSocketMiddleware(RequestDelegate next, WebSocketHandler webSocketHandler)
        {
            _next = next;
            _webSocketHandler = webSocketHandler;
        }

        public async Task Invoke(HttpContext context)
        {
            if (context.WebSockets.IsWebSocketRequest)
            {
                try
                {
                    var connection = await _webSocketHandler.OnConnected(context);
                    if (connection != null)
                    {
                        await _webSocketHandler.ListenConnection(connection);
                    }
                    else
                    {
                        context.Response.StatusCode = 404;
                    }
                }
                catch (NotAuthorizedException e)
                {
                    context.Response.StatusCode = 401;
                    await context.Response.WriteAsync(e.Message);
                }
            }
        }
    }
}

