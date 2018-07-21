using System;
using System.Collections.Generic;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using OpenTracing;
using OpenTracing.Tag;

namespace bevrand.authenticationapi.Middleware
{
    public class ErrorHandlingMiddleware
    {
        private readonly RequestDelegate _next;
        private readonly ITracer _tracer;
        private const string spanName = "error-handling-middleware";

        public ErrorHandlingMiddleware(RequestDelegate next, ITracer tracer)
        {
            _next = next;
            _tracer = tracer;
        }

        public async Task Invoke(HttpContext context)
        {
            try
            {
                await _next(context);
            }
            catch (Exception ex)
            {
                await HandleExceptionAsync(context, ex);
            }
        }

        private Task HandleExceptionAsync(HttpContext context, Exception exception)
        {
            using (var scope = _tracer.BuildSpan(spanName).StartActive(true))
            {
                Tags.Error.Set(scope.Span, true);
                var code = HttpStatusCode.InternalServerError; // 500 if unexpected

                switch (exception)
                {
                    case ArgumentException _:
                        code = HttpStatusCode.BadRequest;
                        break;
                    case NotImplementedException _:
                        code = HttpStatusCode.NotImplemented;
                        break;
                    case HttpNotFoundException _:
                        code = HttpStatusCode.NotFound;
                        break;
                }

                var errorModel = new ErrorModel
                {
                    Error = exception.Message + " " + exception.InnerException?.Message
                };

                var result = JsonConvert.SerializeObject(errorModel,
                    new JsonSerializerSettings
                    {
                        ReferenceLoopHandling = ReferenceLoopHandling.Ignore
                    });

                context.Response.ContentType = "application/json";
                context.Response.StatusCode = (int) code;
                scope.Span.Log(new Dictionary<string, object>
                {
                    ["level"] = "error",
                    [LogFields.Event] = "error",
                    [LogFields.ErrorKind] = exception.GetType().ToString(),
                    [LogFields.ErrorObject] = exception,
                    [LogFields.Stack] = exception.StackTrace,
                    [LogFields.Message] = exception.Message,
                    ["error_id"] = errorModel.ErrorId,
                    ["value"] = result,
                    ["status_code"] = (int) code

                });
                
                return context.Response.WriteAsync(result);
            }
        }
    }
}




 
