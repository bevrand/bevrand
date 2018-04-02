using System;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.MongoApi;
using bevrand.testsuite.Models.RandomizerApi;
using Flurl.Http;
using Newtonsoft.Json;

namespace bevrand.testsuite.Clients
{
    public class RandomizerApiClient
    {
        protected static string ApiUrl;
        
        public RandomizerApiClient(string url)
        {
            ApiUrl = url;
        }
        
        public BaseResponseModel PostASimpleList(RandomizePostRequest request)
        {
            try
            {
                var getStatusUrl = ApiUrl + "/api/randomize";
                var res = getStatusUrl.PostJsonAsync(request).Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = new RandomizePostResult
                {
                    beverage = content,
                    statusCode = (int) res.StatusCode
                };

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerException as FlurlHttpException;
                var responseModel = new ErrorModel
                {
                    message = flurlException.Message,
                    statusCode = (int) flurlException.Call.Response.StatusCode
                };
                return responseModel;
            }
        }

    }
}