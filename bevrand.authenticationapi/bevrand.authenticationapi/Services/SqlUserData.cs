using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.DAL.Models;

namespace bevrand.authenticationapi.Services
{
    public class SqlUserData : IUserData
    {
        private UserContext _context;
        
        public SqlUserData(UserContext context)
        {
            _context = context;
        }
        
        public bool CheckIfUserExists(string name)
        {
            var sqlResult = _context.UserModel.All(u => u.UserName == name);
            return sqlResult;
        }

        public IEnumerable<UserModel> GetAllUsers()
        {
            return _context.UserModel.OrderBy(u => u.Id);
        }

    }
}


