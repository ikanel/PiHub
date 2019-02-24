using System;
using System.Collections.Generic;
using System.Text;

namespace NanoBus.Exceptions
{
   public class SubscriberAlreadyExistsException : ApplicationException
    {
        public SubscriberAlreadyExistsException(string message) : base(message)
        {
            
        }
    }
}
