using System.Collections.Generic;
using System.Net;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Middleware;
using bevrand.authenticationapi.Models;
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
                
                scope.LogResult("Get all users result", result);

                return Ok(result);
            }
        }

        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            using (var scope = _tracer.BuildSpan(spanName).StartActive(true))
            {
                var result = _usersLogic.GetById(id);
                
                scope.LogResult("Get user by id", result);
                
                return Ok(result);
            }
        }

        [HttpGet("by-email/{emailaddress}", Name = "GetByEmail")]
        public IActionResult GetByEmail(string emailaddress)
        {
            var result = _usersLogic.GetByEmailAddress(emailaddress);
            return Ok(result);
        }
        
        /// <summary>
        /// Returns the user based on the provided <paramref name="username"/>
        /// </summary>
        /// <param name="username">Username to search user by in database.</param>
        /// <response code="200" cref="GetUserModel">Gives the email address and active status of the user with the provided <paramref name="username"/>.</response>
        /// <response code="404" cref="ErrorModel">Could not find any user with the given <paramref name="username"/>.</response>
        /// <returns><see cref="GetAllUsersModels"/> response with email address and active status.</returns>
        [ProducesResponseType(typeof(ErrorModel), (int)HttpStatusCode.NotFound)]
        [ProducesResponseType(typeof(GetUserModel), (int)HttpStatusCode.OK)]
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
