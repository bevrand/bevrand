using System.Collections.Generic;
using Newtonsoft.Json;
using Newtonsoft.Json.Serialization;

namespace bevrand.testsuite.Models.MongoApi
{
    public class PrivatePageResponse : BaseResponseModel
    {
        [JsonProperty("Active Users")]
        public List<string> ActiveUsers { get; set; }
    }
}