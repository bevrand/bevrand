using System;
using System.Data.SqlClient;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Middleware;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.Repository.Models;
using bevrand.authenticationapi.Services.Interfaces;

namespace bevrand.authenticationapi.Services
{
    public class ValidationLogic : IValidationLogic
    {
        private readonly IUserRepository _userRepository;

        public ValidationLogic(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }

        public bool CheckIfPassWordIsCorrect(ValidateUserModel validate)
        {
            var userFromDatabase = GetIdFromEmailOrUsername(validate);

            return PasswordHasher.DoesPasswordMatch(validate.PassWord, userFromDatabase.PassWord);
        }

        public void UpdateUserPasswordInDatabase(int id, PutValidateUser validate)
        {

            var sqlResult = _userRepository.GetSingleUser(id);
            var validPassword = PasswordHasher.DoesPasswordMatch(validate.OldPassWord, sqlResult.PassWord);
            if (!validPassword)
            {
                throw new ArgumentException("Password provided is not valid so won't take action");
            }

            var newlyHashedPassword = PasswordHasher.SetPassword(validate.NewPassWord);
            sqlResult.PassWord = newlyHashedPassword;

            _userRepository.Update(sqlResult);
        }

        private ValidateUserModel GetIdFromEmailOrUsername(ValidateUserModel validate)
        {
            if (validate.UserName == null && validate.emailAddress == null)
            {
                throw new ArgumentException("You need to provide a username or email");
            }

            var user = new UserModel();

            if (validate.UserName != null)
            {
                user = _userRepository.GetSingleUser(validate.UserName);
                if (user == null)
                {
                    throw new HttpNotFoundException($"User with name: {validate.UserName} was not found");
                }

                var validateModel = new ValidateUserModel
                {
                    emailAddress = user.EmailAddress,
                    PassWord = user.PassWord,
                    UserName = user.UserName
                };
                return validateModel;
            }

            else
            {
                user = _userRepository.GetSingleUserEmail(validate.emailAddress);
                if (user == null)
                {
                    throw new HttpNotFoundException($"User with email: {validate.emailAddress} was not found");
                }

                var validateModel = new ValidateUserModel
                {
                    emailAddress = user.EmailAddress,
                    PassWord = user.PassWord,
                    UserName = user.UserName
                };
                return validateModel;
            }
        }

    }

}