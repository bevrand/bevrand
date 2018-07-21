using System.Collections.Generic;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Services;
using bevrand.authenticationapi.ViewModels;
using Microsoft.AspNetCore.JsonPatch;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;
using OpenTracing;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UsersController : Controller
    {

       private readonly IUsersLogic _usersLogic;
       private readonly ITracer _tracer;
       private const string spanName = "user-controller";

       public UsersController(IUsersLogic usersLogic, ITracer tracer)
       {
           _usersLogic = usersLogic;
           _tracer = tracer;
       }


        [HttpGet]
        public IActionResult GetAllUsers()
        {
            using (var scope = _tracer.BuildSpan(spanName).StartActive(true))
            {
                 var result = _usersLogic.GetAllUsersFromDataBase();
                 scope.Span.Log(new Dictionary<string, object>
                     {
                         [LogFields.Event] = "Get all users result",
                         ["value"] = JsonConvert.SerializeObject(result)
                     });   
                return Ok(result);
            }
        }

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            using (var scope = _tracer.BuildSpan(spanName).StartActive(true))
            {
                var result = _usersLogic.GetById(id);
                scope.Span.Log(new Dictionary<string, object>
                {
                    [LogFields.Event] = "Get user by id",
                    ["value"] = JsonConvert.SerializeObject(result)
                });
                return Ok(result);
            }
        }

        [HttpGet("by-email/{emailaddress}", Name = "GetByEmail")]
        public IActionResult GetByEmail(string emailaddress)
        {
            var result = _usersLogic.GetByEmailAddress(emailaddress);
            return Ok(result);
        }
        
        
        [HttpGet("by-username/{username}", Name = "GetByUserName")]
        public IActionResult GetByUserName(string username)
        {
            var result = _usersLogic.GetByUserName(username);
            return Ok(result);
        }
        
        [HttpPost]
        public IActionResult Create([FromBody] PostUserModel user)
        {
           _usersLogic.CreateANewUser(user);
            var userToReturn = _usersLogic.GetByUserName(user.UserName);
            return CreatedAtRoute("GetByUserName", new {username = user.UserName}, userToReturn);
        }

        [HttpPut]
        public IActionResult Update([FromQuery]int id, [FromBody] PutUserModel user)
        {
            _usersLogic.UpdateAUser(id, user);
            return new NoContentResult();

        }

        [HttpDelete]
        public IActionResult Delete([FromQuery]int id)
        {
            _usersLogic.DeleteAUser(id);
            return new NoContentResult();
        }
    }
}



