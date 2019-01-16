using System.Collections.Generic;
using Newtonsoft.Json;
using OpenTracing;

namespace bevrand.authenticationapi.Middleware
{
    public static class LogTracing
    {
        public static void LogResult(this IScope scope, string eventDescription, object returnValue)
        {
            scope.Span.Log(new Dictionary<string, object>
            {
                [LogFields.Event] = eventDescription,
                ["value"] = JsonConvert.SerializeObject(returnValue)
            });
        }
    }
}