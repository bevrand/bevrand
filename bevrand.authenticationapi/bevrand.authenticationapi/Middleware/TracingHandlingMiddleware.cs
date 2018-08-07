 using System.Collections.Generic;
 using System.IO;
 using System.Threading.Tasks;
 using Microsoft.AspNetCore.Http;
 using Newtonsoft.Json;
 using OpenTracing;
 
 namespace bevrand.authenticationapi.Middleware
 {
     public class TracingHandlingMiddleware
     {
         private readonly RequestDelegate _next;
         private readonly ITracer _tracer;
         //private const string spanName = "error-handling-middleware";
 
         public TracingHandlingMiddleware(RequestDelegate next, ITracer tracer)
         {
             _next = next;
             _tracer = tracer;
         }
 
         public async Task Invoke(HttpContext context)
         {
            await _next(context);
            var response = context.Response;
            response.Body.Seek(0, SeekOrigin.Begin);
            var result = await new StreamReader(response.Body).ReadToEndAsync();
            response.Body.Seek(0, SeekOrigin.Begin);
            using (var scope = _tracer.BuildSpan("TRACING MIDDLEWARE").StartActive(true))
            {
                scope.Span.Log(new Dictionary<string, object>
                {
                    [LogFields.Event] = "TRACING MIDDLEWARE",
                    ["value"] = JsonConvert.SerializeObject(result)
                });      
                scope.LogResult("TRACING MIDDLEWARE", result);
            }
        }
    }
 }