using System;
using System.Runtime.Serialization;

namespace Messaging.Bus
{
    [Serializable]
    public class ChannelNotFoundException : ApplicationException
    {
        public ChannelNotFoundException()
        {
        }

        public ChannelNotFoundException(string message) : base(message)
        {
        }

        public ChannelNotFoundException(string message, Exception innerException) : base(message, innerException)
        {
        }

        protected ChannelNotFoundException(SerializationInfo info, StreamingContext context) : base(info, context)
        {
        }
    }
}