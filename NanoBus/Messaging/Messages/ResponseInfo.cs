using System;
using System.Linq;
using System.Text;



namespace Messaging.Messages {
	public class ResponseInfo {

        /// <summary>
        /// The id of the command which requested this response
        /// </summary>
        public string RequestId { get; set; }
        public int ResponseCode { get; set; }
        public Boolean Success { get; set; }
        public string Error { get; set; }

    }//end ResponseInfo

}//end namespace Messages