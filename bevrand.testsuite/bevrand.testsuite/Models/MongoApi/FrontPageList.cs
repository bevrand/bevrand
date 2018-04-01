using System.Collections.Generic;

namespace bevrand.testsuite.Models.MongoApi
{
    public class FrontPageList : BaseModel
    {
        public List<Frontpage> listOfFrontPages { get; set; }
    }
}