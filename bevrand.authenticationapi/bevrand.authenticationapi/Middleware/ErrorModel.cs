using System;

namespace bevrand.authenticationapi.Middleware
{
    internal class ErrorModel
    {
        public string Error { get; set; }
        
        public Guid ErrorId { get; set; } = Guid.NewGuid();
    }
}