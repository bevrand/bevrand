using System.Collections.Generic;

namespace bevrand.testsuite.Models.MongoApi
{
    public class FrontPageList : BaseResponseModel
    {
        public List<Frontpage> listOfFrontPages { get; set; }
    }
}