using System;
using Newtonsoft.Json.Linq;

namespace bevrand.authenticationapi.Middleware
{
    /// <summary>
    /// Used for indicating a record could not be found in the backend or database, when exactly one record was expected.
    /// </summary>
    public class RecordNotFoundException : Exception
    {
        public RecordNotFoundException(string message) : base(message)
        {
        }
         public RecordNotFoundException(Exception inner) : this(inner.ToString()) { }
    }
} 