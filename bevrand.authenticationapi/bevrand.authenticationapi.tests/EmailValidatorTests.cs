using bevrand.authenticationapi.BLL;
using Xunit;

namespace bevrand.authenticationapi.tests
{
    public class EmailValidatorTests
    {

        [Fact]
        public void ValidEmail()
        {
            var validMail = "beverage@beveragerandomizer.com";
            var emailIsValid = EmailValidator.EmailIsValid(validMail);
            Assert.True(emailIsValid);
        }

        [Fact]
        public void MailHasNoAdd()
        {
            var invalidMail = "beveragebeveragerandomizer.com";
            var emailIsValid = EmailValidator.EmailIsValid(invalidMail);
            Assert.False(emailIsValid);
            
        }
        
        [Fact]
        public void MailHasNoDotEnding()
        {
            var invalidMail = "beverage@";
            var emailIsValid = EmailValidator.EmailIsValid(invalidMail);
            Assert.False(emailIsValid);
            
        }
    }
}