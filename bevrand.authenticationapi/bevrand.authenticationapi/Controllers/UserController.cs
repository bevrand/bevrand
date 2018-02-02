using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Rewrite.Internal.UrlActions;
using Microsoft.EntityFrameworkCore;

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


        [HttpGet]
        public IActionResult Get([FromQuery] string username, [FromQuery] string emailaddress, [FromQuery] int? id)
        {
            try
            {
                var model = new UserModel();
                
                if (username != null)
                {
                     model = _Usercontext.UserModel.FirstOrDefault(u => u.UserName == username);
                }
                else if (id != null)
                {
                    model = _Usercontext.UserModel.FirstOrDefault(u => u.Id == id);
                }
                else
                {
                    model = _Usercontext.UserModel.FirstOrDefault(u => u.EmailAddress == emailaddress);
                }
                
                var getModel = new GetUserModel
                {
                    Active = model.Active,
                    EmailAddress = model.EmailAddress,
                    Id = model.Id,
                    Username = model.UserName
                };
                    
                return Ok(getModel);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = id,
                    Username = username,
                    Message = "User or Id not found"
                };
                return BadRequest(req);
            }
        }
        


        [HttpPost]
        public IActionResult Create([FromBody] PostUserModel user)
        {
            if (user == null || user.PassWord == null || user.Username == null)
            {
                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.Username,
                    Message = "You must provide at least a username and password"
                };
                return BadRequest(req);
            }

            var userExists = _Usercontext.UserModel.Any(i => i.UserName == user.Username);
            if(userExists)
            {
                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.Username,
                    Message = "User already exists cannot post"
                };
                return BadRequest(req);
            }

            if (user.EmailAddress != null)
            {
                var validateEmail = EmailValidator.EmailIsValid(user.EmailAddress);
                if (!validateEmail)
                {
                    var req = new BadRequestModel
                    {
                        Id = null,
                        Username = user.Username,
                        Message = $"{user.EmailAddress} was not a valid mailaddress"
                    };
                    return BadRequest(req);
                }
            }
            
            var hashedPassword = PasswordHasher.SetPassword(user.PassWord);
            var userToPost = new UserModel
            {
                UserName = user.Username,
                Active = user.Active,
                EmailAddress = user.EmailAddress,
                PassWord = hashedPassword,
                Created = DateTime.UtcNow
            };

            try
            {
                _Usercontext.UserModel.Add(userToPost);
                _Usercontext.SaveChanges();
            }
            catch (Exception e)
            {

                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.Username,
                    Message = $"Exception: {e.Message} Inner Exception: {e.InnerException.Message}" 
                };
                return BadRequest(req);
            }

            
            var returnModel = _Usercontext.UserModel.FirstOrDefault(u => u.UserName == user.Username);
            var croppedReturnModel = new BaseModel
            {
                Id = returnModel.Id,
                Username = returnModel.UserName
            };
            
            return Ok(croppedReturnModel);
        }

        [HttpPut]
        public IActionResult Put([FromQuery]int id, [FromBody]PutUserModel user)
        {
            try
            {
                var selectedUser = _Usercontext.UserModel.AsNoTracking().FirstOrDefault(x => x.Id == id);
                if (selectedUser != null)
                {
                    if (user.Active == null)
                    {
                        user.Active = selectedUser.Active;
                    }

                    if (user.EmailAddress == null)
                    {
                        user.EmailAddress = selectedUser.EmailAddress;
                    }

                    if (user.Username == null)
                    {
                        user.Username = selectedUser.UserName;
                    }
                
                    
                    var userToPut = new UserModel
                    {
                        Id = selectedUser.Id,
                        UserName = user.Username,
                        Active = user.Active,
                        EmailAddress = user.EmailAddress,
                        PassWord = selectedUser.PassWord,
                        Updated = DateTime.UtcNow
                        
                    };
                    
                   // selectedUser = userToPut;
                    
                    _Usercontext.UserModel.Update(userToPut);
                    _Usercontext.SaveChanges();
                }

                return Ok();
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = id,
                    Username = null,
                    Message = "Update not successful, user not found"
                };
                return BadRequest(req);
            }

        }

        [HttpDelete]
        public IActionResult Delete([FromQuery]int id)
        {
            try
            {
                var user = _Usercontext.UserModel.FirstOrDefault(x => x.Id == id);
                if (user != null)
                {
                    _Usercontext.UserModel.Remove(user);
                    _Usercontext.SaveChanges();
                }
                else
                {
                    var req = new BadRequestModel
                    {
                        Id = id,
                        Username = null,
                        Message = "Update not successful, user not found"
                    };
                    return BadRequest(req);
                }

                return Ok();
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = id,
                    Username = null,
                    Message = "Update not successful, user not found"
                };
                return BadRequest(req);
            }

            
        }
    }
}