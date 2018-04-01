using System.Collections.Generic;

namespace bevrand.testsuite.Models.MongoApi
{
    public class Frontpage : BaseModel
    {
        public string id { get; set; }
        public string displayName { get; set; }
        public string imageUrl { get; set; }
        public string dateinserted { get; set; }
        public string dateupdated { get; set; }
        public List<string> beverages { get; set; }
    }
}
