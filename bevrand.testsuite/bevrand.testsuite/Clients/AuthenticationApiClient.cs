namespace bevrand.testsuite.Clients
{
    public class AuthenticationApiClient
    {
        protected static string ApiUrl;
        
        public AuthenticationApiClient(string url)
        {
            ApiUrl = url;
        }
    }
}