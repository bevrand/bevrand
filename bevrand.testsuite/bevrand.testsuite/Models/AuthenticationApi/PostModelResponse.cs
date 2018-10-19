namespace bevrand.testsuite.Models.AuthenticationApi
{
    public class PostModelResponse : BaseResponseModel
    {
        public int id { get; set; }
        public string userName { get; set; }
        public string emailAddress { get; set; }
        public bool active { get; set; }
    }
}