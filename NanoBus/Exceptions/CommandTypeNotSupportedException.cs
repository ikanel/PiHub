using System;
using System.Runtime.Serialization;

namespace Messaging.Bus
{
    [Serializable]
    internal class CommandTypeNotSupportedException : Exception
    {
        public CommandTypeNotSupportedException()
        {
        }

        public CommandTypeNotSupportedException(string message) : base(message)
        {
        }

        public CommandTypeNotSupportedException(string message, Exception innerException) : base(message, innerException)
        {
        }

        protected CommandTypeNotSupportedException(SerializationInfo info, StreamingContext context) : base(info, context)
        {
        }
    }
}