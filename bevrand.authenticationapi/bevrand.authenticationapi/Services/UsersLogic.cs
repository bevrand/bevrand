﻿using System;
using System.Linq;
using AutoMapper;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Middleware;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
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
                throw new HttpNotFoundException($"User with username: {username} was not found");
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
                throw new HttpNotFoundException($"User with id: {id} was not found");
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
                throw new HttpNotFoundException($"User with emailaddress: {emailAddress} was not found");
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

            CheckForNulls(user.UserName, user.EmailAddress, user.PassWord);
            CheckIfEmailAndUserExistAndAreValid(user.UserName, user.EmailAddress);

            var hashedPassword = PasswordHasher.SetPassword(user.PassWord);
            var userToPost = new UserModel
            {
                UserName = user.UserName.ToLowerInvariant(),
                Active = user.Active,
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
                throw new ArgumentException(
                    $"Unable to delete user because it does not exist, id provided was: {id}");
            }

            var user = _userRepository.GetSingleUser(id);
            _userRepository.Delete(user);
        }

        public UserModel PatchAUser(int id, JsonPatchDocument<PatchUserModel> user)
        {
            var userExists = _userRepository.CheckIfIdExists(id);
            if (!userExists)
            {
                throw new ArgumentException(
                    $"Unable to patch user because it does not exist, id provided was: {id}");
            }

            var selectedUser = _userRepository.GetSingleUser(id);
             
            AutoMapper.Mapper.Initialize(c => c.CreateMap<PatchUserModel, UserModel>());
            var patchUserDTO = AutoMapper.Mapper.Map<PatchUserModel>(selectedUser);
           
            user.ApplyTo(patchUserDTO);
            AutoMapper.Mapper.Map(patchUserDTO, selectedUser);
            selectedUser.Updated = DateTime.UtcNow;
            _userRepository.Update(selectedUser);
            Mapper.Reset();
            return selectedUser;

        }



        private void CheckForNulls(string username, string email, string password)
        {
            if (string.IsNullOrWhiteSpace(username))
            {
                throw new ArgumentException(
                    $"You have to provide a user, provided was '{username}'");
            }
            
            if (string.IsNullOrWhiteSpace(password))
            {
                throw new ArgumentException(
                    "You have to provide a password");
            }
            
            if (string.IsNullOrWhiteSpace(email))
            {
                throw new ArgumentException(
                    $"You have to provide an email, provided was '{email}'");
            }
        }
        
        
        private void CheckIfEmailAndUserExistAndAreValid(string userName, string emailAddress)
        {
            var userExists = _userRepository.CheckIfUserExists(userName);
            if (userExists)
            {
                throw new ArgumentException($"User: {userName} already exists cannot post");
            }

            var emailExists = _userRepository.CheckIfEmailExists(emailAddress);
            if (emailExists)
            {
                throw new ArgumentException($"Email: {emailAddress} already exists cannot post");
            }

            var validateEmail = EmailValidator.EmailIsValid(emailAddress);
            if (!validateEmail)
            {
                throw new ArgumentException($"{emailAddress} was not a valid mailaddress");
            }
        }

    }
}

