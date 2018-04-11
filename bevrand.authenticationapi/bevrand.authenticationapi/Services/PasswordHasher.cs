using BCrypt;

namespace bevrand.authenticationapi.BLL
{
    public static class PasswordHasher
    {
        public static string SetPassword(string submittedPassword)
        {
            // hash and save a password
            return BCrypt.Net.BCrypt.HashPassword(submittedPassword);
        }

        public static bool DoesPasswordMatch(string submittedPassword, string hashedPassword)
        {
            // check a password
            return BCrypt.Net.BCrypt.Verify(submittedPassword, hashedPassword);
        }
    }
}





