using System;
using System.Runtime.Serialization;

namespace Messaging.Bus
{
    [Serializable]
    internal class BadMessageException : Exception
    {
        public BadMessageException()
        {
        }

        public BadMessageException(string message) : base(message)
        {
        }

        public BadMessageException(string message, Exception innerException) : base(message, innerException)
        {
        }

        protected BadMessageException(SerializationInfo info, StreamingContext context) : base(info, context)
        {
        }
    }
}