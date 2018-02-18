using System;
using System.Linq;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class ValidateController : Controller
    {
        private readonly UserContext _Usercontext;
        
        public ValidateController(UserContext userContext)
        {
            _Usercontext = userContext;
        }
        
        [HttpPost]
        public IActionResult Check([FromBody] ValidateUserModel validate)
        {
            try
            {
                var dbPassword = validate.Id != null ? _Usercontext.UserModel.FirstOrDefault(u => u.Id == validate.Id).PassWord 
                    : _Usercontext.UserModel.FirstOrDefault(u => u.UserName == validate.Username).PassWord;
                var validPassword = PasswordHasher.DoesPasswordMatch(validate.PassWord, dbPassword);
                return Ok(validPassword);
            }
            catch (Exception)
            {
                var req = new BadRequestModel
                {
                    Id = validate.Id,
                    Username = validate.Username,
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
                var sqlResult = _Usercontext.UserModel.FirstOrDefault(v => v.Id == id);
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
                
                _Usercontext.UserModel.Update(sqlResult);
                _Usercontext.SaveChanges();

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