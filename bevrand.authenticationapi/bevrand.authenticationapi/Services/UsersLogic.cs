using System;
using System.Linq;
using AutoMapper;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Middleware;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.Repository.Models;
using bevrand.authenticationapi.Services.Extensions;
using bevrand.authenticationapi.ViewModels;
using Microsoft.AspNetCore.JsonPatch;

namespace bevrand.authenticationapi.Services
{

    public class UsersLogic : IUsersLogic
    {
        private readonly IUserRepository _userRepository;

        public UsersLogic(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }

        public GetAllUsersModels GetAllUsersFromDataBase()
        {
            var models = _userRepository.GetAllUsers();
            var returnModels = models.Select(model => new GetUserModel
                {
                    Id = model.Id,
                    Username = model.UserName,
                    Active = model.Active,
                    EmailAddress = model.EmailAddress
                })
                .ToList();

            var returnModel = new GetAllUsersModels
            {
                AllUsers = returnModels
            };

            return returnModel;
        }

        public GetUserModel GetByUserName(string username)
        {
            var model = _userRepository.GetSingleUser(username.ToLowerInvariant());
            if (model == null)
            {
                throw new RecordNotFoundException($"User with username: {username} was not found");
            }

            var userModel = new GetUserModel
            {
                Id = model.Id,
                Username = model.UserName,
                Active = model.Active,
                EmailAddress = model.EmailAddress
            };

            return userModel;
        }

        public GetUserModel GetById(int id)
        {
            var model = _userRepository.GetSingleUser(id);
            if (model == null)
            {
                throw new RecordNotFoundException($"User with id: {id} was not found");
            }

            var idModel = new GetUserModel
            {
                Id = model.Id,
                Username = model.UserName,
                Active = model.Active,
                EmailAddress = model.EmailAddress
            };

            return idModel;
        }

        public GetUserModel GetByEmailAddress(string emailAddress)
        {
            var model = _userRepository.GetSingleUserEmail(emailAddress);
            if (model == null)
            {
                throw new RecordNotFoundException($"User with emailaddress: {emailAddress} was not found");
            }

            var emailModel = new GetUserModel
            {
                Id = model.Id,
                Username = model.UserName,
                Active = model.Active,
                EmailAddress = model.EmailAddress
            };

            return emailModel;
        }

        public void CreateANewUser(PostUserModel user)
        {

            this.CheckForNulls(user.UserName, user.EmailAddress, user.PassWord);
            CheckIfUserExists(user.UserName);
            CheckIfEmailExists(user.EmailAddress);

            var hashedPassword = PasswordHasher.SetPassword(user.PassWord);
            var userToPost = new UserModel
            {
                UserName = user.UserName.ToLowerInvariant(),
                Active = true,
                EmailAddress = user.EmailAddress,
                PassWord = hashedPassword,
                Created = DateTime.UtcNow,
                Updated = DateTime.UtcNow
            };
            _userRepository.Add(userToPost);
        }

        public void DeleteAUser(int id)
        {
            var userExists = _userRepository.CheckIfIdExists(id);
            if (!userExists)
            {
                throw new RecordNotFoundException(
                    $"Unable to delete user because it does not exist, id provided was: {id}");
            }

            var user = _userRepository.GetSingleUser(id);
            _userRepository.Delete(user);
        }


        public void UpdateAUser(int id, PutUserModel user)
        {
            var userExists = _userRepository.CheckIfIdExists(id);
            if (!userExists)
            {
                throw new RecordNotFoundException(
                    $"Unable to patch user because it does not exist, id provided was: {id}");
            }
            
            var userToUpdate = _userRepository.GetSingleUser(id);
            
            if (user.EmailAddress != null)
            {
                CheckIfEmailExists(user.EmailAddress);
                userToUpdate.EmailAddress = user.EmailAddress;
            }

            if (user.Username != null)
            {
                CheckIfUserExists(user.Username);
                userToUpdate.UserName = user.Username;
            }

            if (!user.Active)
            {
                userToUpdate.Active = false;
            }
            
            userToUpdate.Updated = DateTime.UtcNow;
            
            _userRepository.Update(userToUpdate);
            
        }

        
        private void CheckIfUserExists(string userName)
        {
            var userExists = _userRepository.CheckIfUserExists(userName);
            if (userExists)
            {
                throw new ArgumentException($"User: {userName} already exists cannot post");
            }

        }
        
        private void CheckIfEmailExists(string emailAddress)
        {

            var emailExists = _userRepository.CheckIfEmailExists(emailAddress);
            if (emailExists)
            {
                throw new ArgumentException($"Email: {emailAddress} already exists cannot post");
            }

            this.ValidateEmailAddress(emailAddress);
        }
    }
}