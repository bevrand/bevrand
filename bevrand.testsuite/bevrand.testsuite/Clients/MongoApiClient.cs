using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.testsuite.Models.MongoApi;
using Flurl.Http;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace bevrand.testsuite.Clients
{
    public class MongoApiClient
    {
        protected static string ApiUrl;
        
        public MongoApiClient(string url)
        {
            ApiUrl = url;
        }

        public Frontpage FrontPageGetWithList(string requeststring)
        {
            try
            {
                var getStatusUrl = ApiUrl + "/api/frontpage" + requeststring;
                var res = getStatusUrl.AllowAnyHttpStatus().GetAsync().Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = JsonConvert.DeserializeObject<Frontpage>(content);
                responseModel.statusCode = (int) res.StatusCode;

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerExceptions.FirstOrDefault() as FlurlHttpException;
                return null;
            }
        }

        public FrontPageList FrontPageGetWithoutList()
        {
            try
            {
                var getStatusUrl = ApiUrl + "/api/frontpage";
                var res = getStatusUrl.AllowAnyHttpStatus().GetAsync().Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var jsonModel = JsonConvert.DeserializeObject<List<Frontpage>>(content);

                var responseModel = new FrontPageList();
                responseModel.statusCode = (int) res.StatusCode;
                responseModel.listOfFrontPages = jsonModel;

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerExceptions.FirstOrDefault() as FlurlHttpException;
                return null;
            }
        }

        public List<string> GetUsers()
        {
            
        }
    }
}