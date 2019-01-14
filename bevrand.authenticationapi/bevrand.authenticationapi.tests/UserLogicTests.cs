using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.authenticationapi.Middleware;
using bevrand.authenticationapi.Models;
using bevrand.authenticationapi.Repository;
using bevrand.authenticationapi.Repository.Models;
using bevrand.authenticationapi.Services;
using Moq;
using Xunit;

namespace bevrand.authenticationapi.tests
{
    public class UserLogicTests
    {
        [Fact]
        public void CheckForPasswordFailsWhenEmailAndUserAreNullTest()
        {
            var mock = new Mock<IUserRepository>();

            var users = new List<UserModel>
            {
                new UserModel
                {
                    Id = 1,
                    PassWord = "password",
                    UserName = "someuser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                },
                new UserModel
                {
                    Id = 2,
                    PassWord = "password",
                    UserName = "someotheruser",
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "someother@email.nl",
                    Updated = new DateTime()
                },
            };

            mock.Setup(e => e.GetAllUsers()).Returns(users);

            var service = new UsersLogic(mock.Object);

            var returnedUsers = service.GetAllUsersFromDataBase();
            Assert.True(returnedUsers.AllUsers.Count() == 2);
        }

        [Fact]
        public void IdThatIsNotFoundThrowsARecordNotFoundException()
        {
            var mock = new Mock<IUserRepository>();

            var id = 1;

            mock.Setup(e => e.GetSingleUser(id)).Returns((UserModel) null);

            var service = new UsersLogic(mock.Object);

            Assert.Throws<RecordNotFoundException>(() => service.GetById(id));
        }
        
        [Fact]
        public void UserThatIsNotFoundThrowsARecordNotFoundException()
        {
            var mock = new Mock<IUserRepository>();

            var username = "someusername";

            mock.Setup(e => e.GetSingleUser(username)).Returns((UserModel) null);

            var service = new UsersLogic(mock.Object);

            Assert.Throws<RecordNotFoundException>(() => service.GetByUserName(username));
        }

        [Fact]
        public void EmailThatIsNotFoundThrowsARecordNotFoundException()
        {
            var mock = new Mock<IUserRepository>();

            var emailAddress = "someusername@someemail.com";

            mock.Setup(e => e.GetSingleUserEmail(emailAddress)).Returns((UserModel) null);

            var service = new UsersLogic(mock.Object);

            Assert.Throws<RecordNotFoundException>(() => service.GetByEmailAddress(emailAddress));
        }
        
        [Fact]
        public void GetByUserIdReturnsAValidUser()
        {
            var mock = new Mock<IUserRepository>();
            var id = 1;
            var username = "someuser";
            var password = "someotherpassword";

            mock.Setup(e => e.GetSingleUser(id)).Returns(
                new UserModel
                {
                    Id = id,
                    PassWord = password,
                    UserName = username,
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new UsersLogic(mock.Object);
            var sut = service.GetById(id);
            Assert.Equal(sut.Id, id);
            Assert.Equal(sut.Username, username);
        }
        
        [Fact]
        public void GetByUserUserNameReturnsAValidUser()
        {
            var mock = new Mock<IUserRepository>();
            var id = 1;
            var username = "someuser";
            var password = "someotherpassword";

            mock.Setup(e => e.GetSingleUser(username)).Returns(
                new UserModel
                {
                    Id = id,
                    PassWord = password,
                    UserName = username,
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = "some@email.nl",
                    Updated = new DateTime()
                });

            var service = new UsersLogic(mock.Object);
            var sut = service.GetByUserName(username);
            Assert.Equal(sut.Id, id);
            Assert.Equal(sut.Username, username);
        }
        
        [Fact]
        public void GetByUserEmailReturnsAValidUser()
        {
            var mock = new Mock<IUserRepository>();
            var id = 1;
            var username = "someuser";
            var password = "someotherpassword";
            var email = "some@email.nl";

            mock.Setup(e => e.GetSingleUserEmail(email)).Returns(
                new UserModel
                {
                    Id = id,
                    PassWord = password,
                    UserName = username,
                    Active = true,
                    Created = new DateTime(),
                    EmailAddress = email,
                    Updated = new DateTime()
                });

            var service = new UsersLogic(mock.Object);
            var sut = service.GetByEmailAddress(email);
            Assert.Equal(sut.Id, id);
            Assert.Equal(sut.Username, username);
            Assert.Equal(sut.EmailAddress, email);
        }
    }
}