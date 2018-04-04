using System;
using bevrand.authenticationapi.Models;

namespace bevrand.authenticationapi.DAL.Models
{
    public class PostUserModel
    {
        public string UserName { get; set; }
        
        public string EmailAddress { get; set; }
        
        public string PassWord { get; set; }
        
        public bool Active { get; set; }
                
    }
}