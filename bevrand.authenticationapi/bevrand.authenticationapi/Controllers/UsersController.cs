using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Services;
using Microsoft.AspNetCore.Mvc;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UsersController : Controller
    {

       // private readonly IUserData _userData;

    //    public UsersController(IUserData userData)
    //    {
    //        _userData = userData;
     //   }
        private readonly UserContext _Usercontext;

        public UsersController(UserContext userContext)
        {
            _Usercontext = userContext;
        }
        
        [HttpGet]
        public IActionResult Get()
        {
            try
            {
               // var models = _userData.GetAllUsers();

                var models =  _Usercontext.UserModel.ToList(); //.OrderBy(u => u.Id);
                var returnModels = new List<GetAllUsersModels>();
                foreach (var model in models)
                {
                    returnModels.Add(new GetAllUsersModels
                    {
                        Id = model.Id,
                        Username = model.UserName,
                        Active = model.Active
                    });

                }

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



