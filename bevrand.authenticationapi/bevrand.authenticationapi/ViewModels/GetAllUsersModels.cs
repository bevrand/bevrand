using System.Collections.Generic;
using bevrand.authenticationapi.Models;

namespace bevrand.authenticationapi.ViewModels
{
    public class GetAllUsersModels
    {
        public IEnumerable<GetUserModel> AllUsers { get; set; }

    }
}