using System.Collections.Generic;

namespace bevrand.testsuite.Models.MongoApi
{
    public class FrontPageListResponse : BaseResponseModel
    {
        public List<FrontpageResponse> listOfFrontPages { get; set; }
    }
}