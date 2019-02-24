using Newtonsoft.Json;
using Newtonsoft.Json.Converters;
using System;
using NanoBus.Messaging.Messages;

namespace Messaging.Messages
{
    public class Message
    {
        public DateTime? Date { get; set; }
        public DateTime? ExpiresAt { get; set; }
        public string Id { get; set; }
        public string Name { get; set; }
        public string Originator { get; set; }
        public string[] Recipients { get; set; }
        public BlobObject Blob { get; set; }
        [JsonConverter(typeof(StringEnumConverter))]
        public MessageType MessageType { get; set; }
        public EnvironmentInfo Environment { get; set; }
        public SystemInfo SysInfo { get; set; }
        public ResponseInfo Response { get; set; }
        public DirectoryInfo Directory { get; set; }
        public string GpIoPins { get; set; }
        public string Value { get; set; }
    }//end Message
}//end namespace Messages