using bevrand.authenticationapi.ViewModels;

namespace bevrand.authenticationapi.Models
{
    public class GetAllUsersModels : BaseModel
    {
        public bool ?Active { get; set; }
    }
}