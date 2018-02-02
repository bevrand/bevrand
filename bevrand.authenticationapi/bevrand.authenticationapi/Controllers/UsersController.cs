using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using Microsoft.AspNetCore.Mvc;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UsersController : Controller
    {
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
                var returnModels = new List<GetAllUsersModels>();
                var models = _Usercontext.UserModel.AsEnumerable();
                foreach (var model in models)
                {
                    var innerModel = new GetAllUsersModels
                    {
                        Id = model.Id,
                        Username = model.UserName,
                        Active = model.Active
                    };
                returnModels.Add(innerModel);

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