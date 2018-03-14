using bevrand.authenticationapi.DAL.Models;
using Microsoft.EntityFrameworkCore;

namespace bevrand.authenticationapi.Data
{
    public class UserContext : DbContext
    {
        public UserContext(DbContextOptions options)
            : base(options)
        {
        }

        public DbSet<UserModel> Users { get; set; }
     
    }
}

