using System.Linq;
using bevrand.authenticationapi.DAL.Models;

namespace bevrand.authenticationapi.DAL
{
    public class DbAccess
    {            
        
        private readonly UserContext _userContext;

        public DbAccess(UserContext userContext)
        {
            _userContext = userContext;
          //  _userContext = new UserContext(connectionstring)
        }

        public bool CheckIfUserExists(string name)
        {
             var sqlResult = _userContext.UserModel.All(u => u.UserName == name);
             return sqlResult;
        }

    }
}

