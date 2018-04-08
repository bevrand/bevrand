using System;
using System.Linq;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.Data;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class ValidateController : Controller
    {
        private readonly IUserRepository _userRepository;

        public ValidateController(IUserRepository userRepository)
        {
            _userRepository = userRepository;
        }
        
        [HttpPost]
        public IActionResult Check([FromBody] ValidateUserModel validate)
        {
            try
            {
                bool validPassword = false;
                
                if (validate.Id != null)
                {
                    var dbPassword =  _userRepository.GetSingleUser(validate.Id).PassWord; 
                    validPassword = PasswordHasher.DoesPasswordMatch(validate.PassWord, dbPassword);
                    
                }
                return Ok(validPassword);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = validate.Id,
                    Message = "User not found"
                };
                return BadRequest(req);
            }


        }

        [HttpPut]
        public IActionResult Put([FromQuery] int id, [FromBody] PutValidateUser validate)
        {
            try
            {
                var sqlResult = _userRepository.GetSingleUser(id);
                var validPassword = PasswordHasher.DoesPasswordMatch(validate.OldPassWord, sqlResult.PassWord);
                if (!validPassword)
                {
                    var req = new BadRequestModel
                        {
                            Id = id,
                            Message = "Password provided is not valid so won't take action"
                        };
                        return BadRequest(req);
                }

                var newlyHashedPassword = PasswordHasher.SetPassword(validate.NewPassWord);
                sqlResult.PassWord = newlyHashedPassword;

                _userRepository.Update(sqlResult);
                
                return Ok();
            }
            catch (Exception e)
            {
             var req = new BadRequestModel
                {
                    Id = id,
                    Message = $"Exception: {e.Message} InnerException: {e.InnerException.Message}"
                };
                return BadRequest(req);
            }
        }

    }
}