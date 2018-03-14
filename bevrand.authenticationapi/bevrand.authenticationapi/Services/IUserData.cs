using System.Collections.Generic;
using bevrand.authenticationapi.DAL.Models;

namespace bevrand.authenticationapi.Services
{
    public interface IUserData
    {
        UserModel Add(UserModel user);
        void Update(UserModel user);
        void Delete(UserModel user);
        bool CheckIfUserExists(string name);
        IEnumerable<UserModel> GetAllUsers();
        UserModel GetSingleUser(int id);
        UserModel GetSingleUser(string query, bool user);
    }
}