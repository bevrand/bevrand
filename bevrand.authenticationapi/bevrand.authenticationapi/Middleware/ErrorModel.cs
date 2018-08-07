using System;

namespace bevrand.authenticationapi.Middleware
{
{
    internal class ErrorModel
    /// <summary>
    /// Error model which can be returned by REST APIs when an non-recoverable error has occurred.
    /// </summary>
    public class ErrorModel
    {
        /// <summary>
        /// Describes the error in a human readable message.
        /// </summary>
        public string Error { get; set; }
        
        /// <summary>
        /// Unique ErrorId, as it will be found in logs. This may be used to diagnose errors.
        /// </summary>
        public Guid ErrorId { get; set; } = Guid.NewGuid();
    }
} 
}