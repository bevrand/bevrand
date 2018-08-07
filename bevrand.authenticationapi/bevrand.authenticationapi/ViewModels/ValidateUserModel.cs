using System;
using bevrand.authenticationapi.ViewModels;

namespace bevrand.authenticationapi.Models
{

    public class ValidateUserModel
    {
        public string UserName { get; set; }
        
        public string emailAddress { get; set; }
        
        public string PassWord { get; set; }
    }
}