using System.Collections.Generic;

namespace bevrand.testsuite.Models.PlaylistApi
{
    public class PrivatePageUserPlaylistsResponse : BaseResponseModel
    {
        public List<string> result { get; set; }
    }
}