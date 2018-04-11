using System.Collections.Generic;
using bevrand.authenticationapi.ViewModels;
using Newtonsoft.Json;

namespace bevrand.authenticationapi.Models
{
    public class GetAllUsersModels
    {
        public IEnumerable<GetUserModel> AllUsers { get; set; }

    }
}