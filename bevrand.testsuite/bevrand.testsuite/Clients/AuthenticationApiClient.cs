namespace bevrand.testsuite.Clients
{
    public class AuthenticationApiClient : BaseApiClient
    {
        protected static string ApiUrl;
        
        public AuthenticationApiClient(string url)
        {
            ApiUrl = url;
        }
    }
}