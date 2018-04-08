using System.Collections.Generic;
using bevrand.authenticationapi.DAL.Models;

namespace bevrand.authenticationapi.Repository
{
    public interface IUserRepository
    {
        UserModel Add(UserModel user);
        void Update(UserModel user);
        void Delete(UserModel user);
        bool CheckIfUserExists(string name);
        IEnumerable<UserModel> GetAllUsers();
        UserModel GetSingleUser(int id);
        UserModel GetSingleUser(string userName);
        UserModel GetSingleUserEmail(string emailAddress);
    }
}