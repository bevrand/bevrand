using System;
using System.Threading.Tasks;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.AuthenticationApi;
using Flurl.Http;

namespace bevrand.testsuite.Clients
{
    public class AuthenticationApiClient
    {        
        public async Task<BaseResponseModel> PostAValidation(string requeststring, ValidateUser request)
        {
            try
            {
                var res = requeststring.PostJsonAsync(request).Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = new ValidatePostResult
                {
                    Valid =  Convert.ToBoolean(content),
                    StatusCode = (int) res.StatusCode
                };

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerException as FlurlHttpException;
                var responseModel = new BaseErrorResponse
                {
                    StatusCode = (int) flurlException.Call.HttpStatus,
                    ErrorMessage = flurlException.Message,
                    UserError = flurlException.GetResponseString()
                };
                return responseModel;
            }
        }
    }
}