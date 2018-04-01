using System.Collections.Generic;

namespace bevrand.testsuite.Models.MongoApi
{
    public class UserResponse : BaseResponseModel
    {
        public List<string> Lists { get; set; }
    }
}