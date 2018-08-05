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

        private readonly JsonSerializerSettings _jsonSerializerSettings = new JsonSerializerSettings
        {
            ReferenceLoopHandling = ReferenceLoopHandling.Ignore
        };

        private const string ResponseContentType = "application/json";
        private const string JaegerSpanName = "error-handling-middleware";

        public ErrorHandlingMiddleware(RequestDelegate next, ITracer tracer)
        {
            _next = next;
            _tracer = tracer;
        }

        /// <summary>
        /// MiddleWare function, to catch unhandled exceptions
        /// </summary>
        /// <param name="context">HttpContext to process.</param>
        // ReSharper disable once UnusedMember.Global : MiddleWare function, is used implicitly.
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
            using (var scope = _tracer.BuildSpan(JaegerSpanName).StartActive(true))
            {
                HttpStatusCode code;

                switch (exception)
                {
                    case ArgumentException _:
                        code = HttpStatusCode.BadRequest;
                        break;
                    case RecordNotFoundException _:
                        code = HttpStatusCode.NotFound;
                        break;
                    case NotImplementedException _:
                        code = HttpStatusCode.NotImplemented;
                        Tags.Error.Set(scope.Span, true);
                        break;
                    default:
                        code = HttpStatusCode.InternalServerError; // 500 if unexpected
                        Tags.Error.Set(scope.Span, true);
                        break;
                }

                var errorModel = new ErrorModel
                {
                    Error = exception.Message + " " + exception.InnerException?.Message
                };

                var result = JsonConvert.SerializeObject(errorModel, _jsonSerializerSettings);

                context.Response.ContentType = ResponseContentType;
                context.Response.StatusCode = (int) code;
                
                scope.Span.Log(new Dictionary<string, object>
                {
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




 
