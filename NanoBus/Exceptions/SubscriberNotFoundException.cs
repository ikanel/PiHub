using System;
using System.Collections.Generic;
using System.Text;

namespace NanoBus.Exceptions
{
   public class SubscriberNotFoundException:ApplicationException
    {
        public SubscriberNotFoundException(string message) : base(message)
        {
            
        }
    }
}
