using System;
using bevrand.authenticationapi.BLL;
using Xunit;

namespace bevrand.authenticationapi.tests
{
    public class PassWordHasherTests
    {
        [Fact]
        public void HashPassWord()
        {
            var passWord = "thisisatest";
            var hashedPassword = PasswordHasher.SetPassword(passWord);
            Assert.NotEqual(passWord, hashedPassword);       
        }

        [Fact]
        public void HashedPassWordMatches()
        {
            var passWord = "thisisatest";
            var hashedPassword = PasswordHasher.SetPassword(passWord);
            var passWordHashed = PasswordHasher.DoesPasswordMatch(passWord, hashedPassword);
            Assert.True(passWordHashed);
        }

        [Fact]
        public void ChangedPassWordDoesNotMatch()
        {
            var passWord = "thisisatest";
            var hashedPassword = PasswordHasher.SetPassword(passWord);
            var passWordHashed = PasswordHasher.DoesPasswordMatch("thisisanotherpassword", hashedPassword);
            Assert.False(passWordHashed);
        }
    }
}