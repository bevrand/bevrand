using System.Collections.Generic;

namespace bevrand.testsuite.Models.PlaylistApi
{
    public class BasePlaylist
    {
        public string displayName { get; set; }
        public string imageUrl { get; set; }
        public List<string> beverages { get; set; }
    }
}