using System;
using System.Linq;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using Microsoft.AspNetCore.Mvc;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UserController : Controller
    {
        
        private readonly UserContext _Usercontext;

        public UserController(UserContext userContext)
        {
            _Usercontext = userContext;
        }
        
               
        [HttpGet("{username}")]
        public string Get(string username)
        {
            return "This Controller works";
        }
        
        
        [HttpGet("{id}")]
        public string Get(int id)
        {
            try
            {
                var sqlResult = _Usercontext.UserModel.FirstOrDefault(i => i.Id == id);
                var item = sqlResult;
                return item.UserName;
            }
            catch (Exception e)
            {
                Console.WriteLine(e);
                return "no go amigo";
            }

        }

        [HttpPost]
        public IActionResult Create([FromBody] UserModel user)
        {
            if (user == null)
            {
                return BadRequest();
            }

            _Usercontext.UserModel.Add(user);
            _Usercontext.SaveChanges();
            
            return CreatedAtRoute("User", new { user = user.Id }, user);
        }
        
    }
}