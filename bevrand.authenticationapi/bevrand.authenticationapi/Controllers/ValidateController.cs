using System;
using System.Linq;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.Data;
using bevrand.authenticationapi.DAL;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.Services.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Microsoft.CodeAnalysis.CSharp.Syntax;
using Microsoft.EntityFrameworkCore;

namespace bevrand.authenticationapi.Controllers
{
    [Route("api/[controller]")]
    public class ValidateController : Controller
    {
        private readonly IValidationLogic _validationLogic;

        public ValidateController(IValidationLogic validation)
        {
            _validationLogic = validation;
        }

        [HttpPost]
        public IActionResult Check([FromBody] ValidateUserModel validate)
        {
            var valid = _validationLogic.CheckIfPassWordIsCorrect(validate);
            return Ok(valid);
        }

        [HttpPut]
        public IActionResult Put([FromQuery] int id, [FromBody] PutValidateUser validate)
        {
            _validationLogic.UpdateUserPasswordInDatabase(id, validate);
            return Ok();
        }

    }
}