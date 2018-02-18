using System;

namespace bevrand.authenticationapi.Models
{

    public class ValidateUserModel : BaseModel
    {
        public override string Username { get; set; } = null;
        
        public string PassWord { get; set; }
    }
}