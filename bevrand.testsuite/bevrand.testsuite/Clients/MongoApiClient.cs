using System;
using System.Collections.Generic;
using System.Linq;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.MongoApi;
using Flurl.Http;
using Flurl;
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

        public BaseResponseModel FrontPageGetWithList(string requeststring)
        {
            try
            {
                var getStatusUrl = ApiUrl + "/api/frontpage" + requeststring;
                var res = getStatusUrl.GetAsync().Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = JsonConvert.DeserializeObject<FrontpageResponse>(content);
                responseModel.StatusCode = (int) res.StatusCode;

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerException as FlurlHttpException;
                var responseModel = new ErrorModel
                {
                    message = flurlException.Message,
                    StatusCode = (int) flurlException.Call.Response.StatusCode
                };
                return responseModel;
            }
        }

        public BaseResponseModel FrontPageGetWithoutList()
        {
            try
            {
                var getStatusUrl = ApiUrl + "/api/frontpage";
                var res = getStatusUrl.GetAsync().Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var jsonModel = JsonConvert.DeserializeObject<List<FrontpageResponse>>(content);

                var responseModel = new FrontPageListResponse();
                responseModel.StatusCode = (int) res.StatusCode;
                responseModel.listOfFrontPages = jsonModel;

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerException as FlurlHttpException;
                var responseModel = new ErrorModel
                {
                    message = flurlException.Message,
                    StatusCode = (int) flurlException.Call.Response.StatusCode
                };
                return responseModel;
            }
        }

        public BaseResponseModel GetUsers()
        {

            try
            {
                var getStatusUrl = ApiUrl + "/api/users";
                var res = getStatusUrl.GetAsync().Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = JsonConvert.DeserializeObject<UsersResponse>(content);
                responseModel.StatusCode = (int) res.StatusCode;
                
                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerException as FlurlHttpException;
                var responseModel = new ErrorModel
                {
                    message = flurlException.Message,
                    StatusCode = (int) flurlException.Call.Response.StatusCode
                };
                return responseModel;
            }
        }

        public BaseResponseModel GetUser(string requeststring)
        {

            try
            {
                var getStatusUrl = ApiUrl + "/api/user" + requeststring;
                var res = getStatusUrl.GetAsync().Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = JsonConvert.DeserializeObject<UserResponse>(content);  
                responseModel.StatusCode = (int) res.StatusCode;

                return responseModel;
            }
            catch (AggregateException e)
            {
                var flurlException = e.InnerException as FlurlHttpException;
                var responseModel = new ErrorModel
                {
                    message = flurlException.Message,
                    StatusCode = (int) flurlException.Call.Response.StatusCode
                };
                return responseModel;
            }
        }
    }
}