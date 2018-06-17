using bevrand.authenticationapi.ViewModels;

namespace bevrand.authenticationapi.Models
{
    public class GetUserModel : BaseModel
    {
        public string EmailAddress { get; set; }
        
        public bool Active { get; set; }
    }
}