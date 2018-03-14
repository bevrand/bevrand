using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.Data;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Services;
using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Rewrite.Internal.UrlActions;
using Microsoft.EntityFrameworkCore;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UserController : Controller
    {
        
        private readonly IUserData _userData;

        public UserController(IUserData userData)
        {
            _userData = userData;
        }


        [HttpGet]
        public IActionResult Get([FromQuery] string username, [FromQuery] string emailaddress, [FromQuery] int? id)
        {
            try
            {
                var model = new UserModel();
                
                if (id != null)
                {
                    model = _userData.GetSingleUser((int)id);
                }
                else if (!string.IsNullOrWhiteSpace(username))
                {
                    model = _userData.GetSingleUser(username);
                }
                else if (!string.IsNullOrWhiteSpace(emailaddress) && string.IsNullOrWhiteSpace(username))
                {
                    model = _userData.GetSingleUserEmail(emailaddress);
                }
                else
                {
                    var req = new BadRequestModel
                    {
                        Id = id,
                        Username = username,
                        Message = "Nothing to query"
                    };
                    return BadRequest(req);
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
           
            if (string.IsNullOrWhiteSpace(user.PassWord) || string.IsNullOrWhiteSpace(user.Username))
            {
                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.Username,
                    Message = "You must provide at least a username and password"
                };
                return BadRequest(req);
            }

            var userExists = _userData.CheckIfUserExists(user.Username);
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
                var returnModel = _userData.Add(userToPost);
                var croppedReturnModel = new BaseModel
                {
                    Id = returnModel.Id,
                    Username = returnModel.UserName
                };
            
                return Ok(croppedReturnModel);
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

        }

        [HttpPut]
        public IActionResult Put([FromQuery]int id, [FromBody]PutUserModel user)
        {
            try
            {
                var selectedUser = _userData.GetSingleUser(id);
                if (selectedUser != null)
                {
                    if (user.Active == null)
                    {
                        user.Active = selectedUser.Active;
                    }

                    if (string.IsNullOrWhiteSpace(user.EmailAddress))
                    {
                        user.EmailAddress = selectedUser.EmailAddress;
                    }

                    if (string.IsNullOrWhiteSpace(user.Username))
                    {
                        user.Username = selectedUser.UserName;
                    }
                    
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
                    
                    var userToPut = new UserModel
                    {
                        Id = selectedUser.Id,
                        UserName = user.Username,
                        Active = user.Active,
                        EmailAddress = user.EmailAddress,
                        PassWord = selectedUser.PassWord,
                        Updated = DateTime.UtcNow
                        
                    };
                    _userData.Update(userToPut);
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
                var user = _userData.GetSingleUser(id);
                if (user != null)
                {
                    _userData.Delete(user);
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