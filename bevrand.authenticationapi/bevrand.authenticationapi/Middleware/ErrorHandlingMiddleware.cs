using System;
using System.Net;
using System.Threading.Tasks;
using Microsoft.AspNetCore.Http;
using Newtonsoft.Json;
using Microsoft.Extensions.Logging;

namespace bevrand.authenticationapi.Middleware
{
    public class ErrorHandlingMiddleware
    {
        private static ILogger _logger;
        private readonly RequestDelegate _next;

        public ErrorHandlingMiddleware(RequestDelegate next)
        {
            _next = next;
        }

        public async Task Invoke(HttpContext context, ILoggerFactory loggerFactory)
        {
            try
            {
                if (_logger == null)
                    _logger = loggerFactory.CreateLogger(null);

                await _next(context);
            }
            catch (Exception ex)
            {
                await HandleExceptionAsync(context, ex);
            }
        }
        private static Task HandleExceptionAsync(HttpContext context, Exception exception)
        {
            var code = HttpStatusCode.InternalServerError; // 500 if unexpected

            if (exception is ArgumentException)
            {
                code = HttpStatusCode.BadRequest;
            }

            if (exception is NotImplementedException)
            {
                code = HttpStatusCode.NotImplemented;
            }

            var errorModel = new ErrorModel {Error = exception.Message + " " + exception.InnerException?.Message};
            
            var result = JsonConvert.SerializeObject(errorModel,
                new JsonSerializerSettings()
                {
                    ReferenceLoopHandling = ReferenceLoopHandling.Ignore
                });
            context.Response.ContentType = "application/json";
            context.Response.StatusCode = (int) code;
            return context.Response.WriteAsync(result);
        }
    }
}

/*


 */