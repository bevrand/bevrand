using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.Data;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Services;
using Microsoft.AspNetCore.Mvc;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UsersController : Controller
    {

       private readonly IUserData _userData;

       public UsersController(IUserData userData)
       {
           _userData = userData;
       }


        [HttpGet]
        public IActionResult Get()
        {
            try
            {
                var models = _userData.GetAllUsers();
                var returnModels = models.Select(model => new GetAllUsersModels
                    {
                        Id = model.Id,
                        Username = model.UserName,
                        Active = model.Active
                    })
                    .ToList();

                return Ok(returnModels);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = null,
                    Username = null,
                    Message = "DB is empty"
                };

                return BadRequest(req);
            }
        }
    }
}



