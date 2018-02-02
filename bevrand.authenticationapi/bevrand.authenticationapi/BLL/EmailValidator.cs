using System.ComponentModel.DataAnnotations;

namespace bevrand.authenticationapi.BLL
{
    public static class EmailValidator
    {
        public static bool EmailIsValid(string mailAddress)
        {
            return new EmailAddressAttribute().IsValid(mailAddress);
        }
    }
}