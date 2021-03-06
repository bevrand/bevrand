﻿using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository.Models;
using bevrand.authenticationapi.ViewModels;
using Microsoft.AspNetCore.JsonPatch;

namespace bevrand.authenticationapi.Services
{
    public interface IUsersLogic
    {
        GetAllUsersModels GetAllUsersFromDataBase();
        GetUserModel GetByUserName(string username);
        GetUserModel GetById(int id);
        GetUserModel GetByEmailAddress(string emailAddress);
        void CreateANewUser(PostUserModel user);
        void DeleteAUser(int id);
        void UpdateAUser(int id, PutUserModel user);
    }
}
