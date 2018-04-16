using bevrand.authenticationapi.Models;

namespace bevrand.authenticationapi.Services.Interfaces
{
    public interface IValidationLogic
    {
        bool CheckIfPassWordIsCorrect(ValidateUserModel validate);
        void UpdateUserPasswordInDatabase(int id, PutValidateUser validate);
    }
}