using System;
using System.Runtime.Serialization;

namespace Messaging.Bus
{
    [Serializable]
    internal class UnknownMessageTypeException : Exception
    {
        public UnknownMessageTypeException()
        {
        }

        public UnknownMessageTypeException(string message) : base(message)
        {
        }

        public UnknownMessageTypeException(string message, Exception innerException) : base(message, innerException)
        {
        }

        protected UnknownMessageTypeException(SerializationInfo info, StreamingContext context) : base(info, context)
        {
        }
    }
}