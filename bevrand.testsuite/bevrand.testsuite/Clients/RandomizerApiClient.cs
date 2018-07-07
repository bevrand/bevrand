using System;
using System.Threading.Tasks;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.MongoApi;
using bevrand.testsuite.Models.RandomizerApi;
using Flurl.Http;
using Newtonsoft.Json;

namespace bevrand.testsuite.Clients
{
    public class RandomizerApiClient
    {
        public async Task<BaseResponseModel> PostASampleListWithBeverages(string requeststring, RandomizePostRequest request)
        {
            try
            {
                var res = requeststring.PostJsonAsync(request).Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = new RandomizePostResult
                {
                    result = content,
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