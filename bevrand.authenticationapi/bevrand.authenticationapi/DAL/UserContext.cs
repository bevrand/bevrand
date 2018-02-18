using bevrand.authenticationapi.DAL.Models;
using Microsoft.EntityFrameworkCore;
using Npgsql.EntityFrameworkCore.PostgreSQL;

namespace bevrand.authenticationapi.DAL
{
    public class UserContext : DbContext
    {
        public UserContext(DbContextOptions<UserContext> options)
            : base(options)
        {
        }

        public DbSet<UserModel> UserModel { get; set; }
        


    }


}

