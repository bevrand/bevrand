using System;
using System.ComponentModel.DataAnnotations;

namespace bevrand.authenticationapi.Services.Extensions
{
    public static class Validator
    {
        public static void CheckForNulls(this UsersLogic userLogic, string username, string email, string password)
        {   
            CheckUserForNull(username);
            CheckEmailForNull(email);
            CheckPassWordForNull(password);
        }
        
        public static void CheckForNulls(this UsersLogic userLogic, string username, string email)
        {   
            CheckUserForNull(username);
            CheckEmailForNull(email);
        }

        public static void ValidateEmailAddress(this UsersLogic usersLogic, string emailAddress)
        {
            var valid = new EmailAddressAttribute().IsValid(emailAddress);
            if (!valid)
            {
                throw new ArgumentException($"{emailAddress} was not a valid mailaddress");
            }
        }

        private static void CheckPassWordForNull(string password)
        {
            if (string.IsNullOrWhiteSpace(password))
            {
                throw new ArgumentException(
                    $"You have to provide a valid password");
            }
        }
        private static void CheckUserForNull(string username)
        {   
            if (string.IsNullOrWhiteSpace(username))
            {
                throw new ArgumentException(
                    $"You have to provide a user, provided was '{username}'");
            }

        }

        private static void CheckEmailForNull(string email)
        {
            if (string.IsNullOrWhiteSpace(email))
            {
                throw new ArgumentException(
                    $"You have to provide an email, provided was '{email}'");
            }
        }
    }
}