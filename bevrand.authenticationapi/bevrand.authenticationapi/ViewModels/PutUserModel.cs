namespace bevrand.authenticationapi.ViewModels
{
    public class PutUserModel
    {
        public string Username { get; set; }
        
        public string EmailAddress { get; set; }
        
        public bool Active { get; set; }
    }
}