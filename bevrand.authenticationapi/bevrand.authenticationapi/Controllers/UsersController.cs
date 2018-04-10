using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.Data;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.DAL.Models;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.ViewModels;
using Microsoft.AspNetCore.Mvc;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class UsersController : Controller
    {

       private readonly IUserRepository _userRepository;

       public UsersController(IUserRepository userRepository)
       {
           _userRepository = userRepository;
       }


        [HttpGet]
        public IActionResult Get()
        {
            try
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
                
                return Ok(returnModel);
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
        
        [HttpGet("{id}")]
        public IActionResult GetById(int id)
        {
            try
            {
                var model = _userRepository.GetSingleUser(id);

                var getModel = new GetUserModel
                {
                    Id = model.Id,
                    Username = model.UserName,
                    Active = model.Active,
                    EmailAddress = model.EmailAddress
                };
                    
                return Ok(getModel);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = id,
                    Message = "User or Id not found"
                };
                return NotFound(req);
            }
        }
        
        [HttpGet("by-email/{emailaddress}", Name = "GetByEmail")]
        public IActionResult GetByEmail(string emailaddress)
        {
            try
            {
                var model = _userRepository.GetSingleUserEmail(emailaddress);
                
                var getModel = new GetUserModel
                {
                    Id = model.Id,
                    Username = model.UserName,
                    Active = model.Active,
                    EmailAddress = model.EmailAddress
                };
                    
                return Ok(getModel);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Message = "User or Id not found"
                };
                return NotFound(req);
            }
        }
        

        
        [HttpGet("by-username/{username}", Name = "GetByUserName")]
        public IActionResult GetByUserName(string username)
        {
            try
            {
                var model = _userRepository.GetSingleUser(username.ToLowerInvariant());
                
                var getModel = new GetUserModel
                {
                    Id = model.Id,
                    Username = model.UserName,
                    Active = model.Active,
                    EmailAddress = model.EmailAddress
                };
                    
                return Ok(getModel);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Message = "User or Id not found"
                };
                return NotFound(req);
            }
        }
        
        [HttpPost]
        public IActionResult Create([FromBody] PostUserModel user)
        {
            if (string.IsNullOrWhiteSpace(user.PassWord) || string.IsNullOrWhiteSpace(user.UserName))
            {
                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.UserName,
                    Message = "You must provide at least a username and password"
                };
                return BadRequest(req);
            }

            var userExists = _userRepository.CheckIfUserExists(user.UserName);
            if(userExists)
            {
                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.UserName,
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
                        Username = user.UserName,
                        Message = $"{user.EmailAddress} was not a valid mailaddress"
                    };
                    return BadRequest(req);
                }
            }
            
            var hashedPassword = PasswordHasher.SetPassword(user.PassWord);
            var userToPost = new UserModel
            {
                UserName = user.UserName.ToLowerInvariant(),
                Active = user.Active,
                EmailAddress = user.EmailAddress,
                PassWord = hashedPassword,
                Created = DateTime.UtcNow
            };

            try
            {
                _userRepository.Add(userToPost);
                var returnModel = _userRepository.GetSingleUser(user.UserName.ToLowerInvariant());
                return CreatedAtRoute("GetByUserName", new {username = user.UserName}, returnModel);
            }
            catch (Exception e)
            {

                var req = new BadRequestModel
                {
                    Id = null,
                    Username = user.UserName,
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
                var selectedUser = _userRepository.GetSingleUser(id);
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

                    if (user.Username != selectedUser.UserName)
                    {
                        var userExists = _userRepository.CheckIfUserExists(user.Username);
                        if(userExists)
                        {
                            var req = new BadRequestModel
                            {
                                Id = null,
                                Username = user.Username,
                                Message = "User already exists cannot put"
                            };
                            return BadRequest(req);
                        }
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
                        UserName = user.Username.ToLowerInvariant(),
                        Active = user.Active,
                        EmailAddress = user.EmailAddress,
                        PassWord = selectedUser.PassWord,
                        Updated = DateTime.UtcNow
                        
                    };
                    _userRepository.Update(userToPut);
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
                return NotFound(req);
            }

        }

        [HttpDelete]
        public IActionResult Delete([FromQuery]int id)
        {
            try
            {
                var user = _userRepository.GetSingleUser(id);
                if (user != null)
                {
                    _userRepository.Delete(user);
                }
                else
                {
                    var req = new BadRequestModel
                    {
                        Id = id,
                        Username = null,
                        Message = "Update not successful, user not found"
                    };
                    return NotFound(req);
                }

                return new NoContentResult();
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



