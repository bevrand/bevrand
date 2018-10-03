using System.Collections.Generic;

namespace bevrand.testsuite.Models.PlaylistApi
{
    public class PlayListResponse : CreatePlayList
    {
        public string id { get; set; }
        public string user { get; set; }
    }
}