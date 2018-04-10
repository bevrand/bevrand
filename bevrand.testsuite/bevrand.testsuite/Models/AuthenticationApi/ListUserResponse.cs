using System.Collections.Generic;
using Newtonsoft.Json;

namespace bevrand.testsuite.Models.AuthenticationApi
{
    public class ListUserResponse : BaseResponseModel
    {
        [JsonProperty(PropertyName = "allUsers")]
        public List<UserResponse> AllUsers { get; set; }
    }
}