using System.Collections.Generic;
using bevrand.authenticationapi.DAL.Models;

namespace bevrand.authenticationapi.Services
{
    public interface IUserData
    {
        bool CheckIfUserExists(string name);
        IEnumerable<UserModel> GetAllUsers();
    }
}