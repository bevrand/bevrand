namespace bevrand.testsuite.Models.AuthenticationApi
{
    public class UserResponse : BaseResponseModel
    {
        public bool active { get; set; }
        public string username { get; set; }
        public string emailAddress { get; set; }
        public int id { get; set; }
    }
}