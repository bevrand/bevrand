using System.Collections.Generic;

namespace bevrand.testsuite.Models.RandomizerApi
{
    public class RandomizePostRequest
    {
        public List<string> beverages { get; set; }
        public string list { get; set; }
        public string user { get; set; }
    }
}