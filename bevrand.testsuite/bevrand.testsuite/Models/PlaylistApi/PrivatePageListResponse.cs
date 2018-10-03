using System.Collections.Generic;

namespace bevrand.testsuite.Models.MongoApi
{
    public class PrivatePageListResponse : BaseResponseModel
    {
        public List<string> Lists { get; set; }
    }
}