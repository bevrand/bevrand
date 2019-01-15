using System;
using bevrand.authenticationapi.BLL;
using bevrand.authenticationapi.Middleware;
using Xunit;
using bevrand.authenticationapi.Services.Interfaces;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.Repository.Models;
using bevrand.authenticationapi.Services;
using Moq;

namespace bevrand.authenticationapi.tests
{
    public class ValidationLogicTests
    {
        [Fact]
        public void CheckForPasswordFailsWhenEmailAndUserAreNullTest()
        {
            var mock = new Mock<IUserRepository>();

            var valdationModel = new ValidateUserModel
            {
                emailAddress = null,
                PassWord = "somepassword",
                UserName = null
            };

            var service = new ValidationLogic(mock.Object);

            Assert.Throws<ArgumentException>(() => service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void UserThatIsNotFoundThrowsARecordNotFoundException()
        {
            var mock = new Mock<IUserRepository>();

            var valdationModel = new ValidateUserModel
            {
                emailAddress = "some@email.com",
                PassWord = PasswordHasher.SetPassword("somepassword"),
                UserName = "someuser"
            };

            mock.Setup(e => e.GetSingleUser(valdationModel.UserName)).Returns((UserModel) null);

            var service = new ValidationLogic(mock.Object);

            Assert.Throws<RecordNotFoundException>(() => service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void EmailThatIsNotFoundThrowsARecordNotFoundException()
        {
            var mock = new Mock<IUserRepository>();

            var valdationModel = new ValidateUserModel
            {
                emailAddress = "some@email.com",
                PassWord = PasswordHasher.SetPassword("somepassword"),
                UserName = null
            };

            mock.Setup(e => e.GetSingleUserEmail(valdationModel.emailAddress)).Returns((UserModel) null);

            var service = new ValidationLogic(mock.Object);

            Assert.Throws<RecordNotFoundException>(() => service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void PasswordsDoNotMatchReturnsAFalse()
        {
            var mock = new Mock<IUserRepository>();

            var valdationModel = new ValidateUserModel
            {
                emailAddress = "some@email.com",
                PassWord = PasswordHasher.SetPassword("somepassword"),
                UserName = "someuser"
            };

            var password = PasswordHasher.SetPassword("someotherpassword");

            mock.Setup(e => e.GetSingleUser(valdationModel.UserName)).Returns(
                new UserModel
                {
                    Id = 1,
                    PassWord = password,
                    UserName = "someuser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new ValidationLogic(mock.Object);

            Assert.False(service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void PasswordsDoNotMatchReturnsAFalseWithEmail()
        {
            var mock = new Mock<IUserRepository>();

            var valdationModel = new ValidateUserModel
            {
                emailAddress = "some@email.com",
                PassWord = PasswordHasher.SetPassword("somepassword"),
                UserName = null
            };

            var password = PasswordHasher.SetPassword("someotherpassword");

            mock.Setup(e => e.GetSingleUserEmail(valdationModel.emailAddress)).Returns(
                new UserModel
                {
                    Id = 1,
                    PassWord = password,
                    UserName = "someuser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new ValidationLogic(mock.Object);

            Assert.False(service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void PasswordsDoNotMatchReturnsATrue()
        {
            var mock = new Mock<IUserRepository>();
            var password = "someotherpassword";
            var hashedPassword = PasswordHasher.SetPassword(password);

            var valdationModel = new ValidateUserModel
            {
                emailAddress = "some@email.com",
                PassWord = password,
                UserName = "someuser"
            };

            mock.Setup(e => e.GetSingleUser(valdationModel.UserName)).Returns(
                new UserModel
                {
                    Id = 1,
                    PassWord = hashedPassword,
                    UserName = "someuser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new ValidationLogic(mock.Object);

            Assert.True(service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void PasswordsDoNotMatchReturnsATrueEmail()
        {
            var mock = new Mock<IUserRepository>();
            var password = "someotherpassword";
            var hashedPassword = PasswordHasher.SetPassword(password);

            var valdationModel = new ValidateUserModel
            {
                emailAddress = "some@email.com",
                PassWord = password,
                UserName = null
            };

            mock.Setup(e => e.GetSingleUserEmail(valdationModel.emailAddress)).Returns(
                new UserModel
                {
                    Id = 1,
                    PassWord = hashedPassword,
                    UserName = "someuser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new ValidationLogic(mock.Object);

            Assert.True(service.CheckIfPassWordIsCorrect(valdationModel));
        }

        [Fact]
        public void UpdatePassWordThrowsArgumentExceptionWhenPasswordDoNotMatch()
        {
            var mock = new Mock<IUserRepository>();
            var id = 1;
            var password = "someotherpassword";
            var hashedPassword = PasswordHasher.SetPassword(password);

            var valdationModel = new PutValidateUser
            {
                NewPassWord = "newpassword",
                OldPassWord = "notsomeotherpassword"
            };

            mock.Setup(e => e.GetSingleUser(id)).Returns(
                new UserModel
                {
                    Id = id,
                    PassWord = hashedPassword,
                    UserName = "someuser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new ValidationLogic(mock.Object);
            Assert.Throws<ArgumentException>(() => service.UpdateUserPasswordInDatabase(id, valdationModel));
        }

        [Fact]
        public void ShouldBeAbleToUpdateUserIfPassWordsMatch()
        {
            var mock = new Mock<IUserRepository>();
            var id = 1;
            var password = "someotherpassword";
            var hashedPassword = PasswordHasher.SetPassword(password);

            var valdationModel = new PutValidateUser
            {
                NewPassWord = "newpassword",
                OldPassWord = "someotherpassword"
            };

            var newUserModel = new UserModel
            {
                Id = id,
                PassWord = hashedPassword,
                UserName = "someuser",
                Active = true,
                Created = new DateTime(),
                EmailAddress = "some@email.nl",
                Updated = new DateTime()
            };

            mock.Setup(e => e.GetSingleUser(id)).Returns(newUserModel);

            var service = new ValidationLogic(mock.Object);
            service.UpdateUserPasswordInDatabase(id, valdationModel);
            mock.Verify(x => x.Update(It.IsAny<UserModel>()), Times.Exactly(1));
        }
    }
}