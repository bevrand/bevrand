using System.Collections.Generic;

namespace bevrand.testsuite.Models.PlaylistApi
{
    public class PublicPageListResponse : BaseResponseModel
    {
        public List<PlayListResponse> result { get; set; }
    }
}