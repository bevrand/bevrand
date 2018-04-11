using bevrand.authenticationapi.Models;

namespace bevrand.authenticationapi.DAL.Models
{
    public class PatchUserModel
    {
        public string Username { get; set; }
        
        public string EmailAddress { get; set; }
        
        public bool ?Active { get; set; }
    }
}