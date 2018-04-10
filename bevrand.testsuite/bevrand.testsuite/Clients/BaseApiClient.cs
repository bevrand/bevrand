using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using bevrand.testsuite.Models;
using bevrand.testsuite.Models.AuthenticationApi;
using Flurl.Http;
using Newtonsoft.Json;
using Newtonsoft.Json.Linq;

namespace bevrand.testsuite.Clients
{
    public class BaseApiClient
    {
        public async Task<BaseResponseModel> GenericGet<TType>(string requeststring)
            where TType : BaseResponseModel
        {
            try
            {
                var res = await requeststring.GetAsync();
                var content = res.Content.ReadAsStringAsync().Result;

                try
                {
                    var responseModel = JsonConvert.DeserializeObject<TType>(content);

                    responseModel.StatusCode = (int) res.StatusCode;
                    return responseModel;

                }
                catch (AggregateException e)
                {
                    var responseModel = new BaseErrorResponse
                    {
                        StatusCode = (int) res.StatusCode,
                        ErrorMessage = e.Message
                    };
                    return responseModel;
                }
            }
            catch (FlurlHttpException e)
            {
                var responseModel = new BaseErrorResponse
                {
                    StatusCode = (int) e.Call.HttpStatus,
                    ErrorMessage = e.Message,
                    UserError = e.GetResponseString()
                };
                return responseModel;
            }
        }
        

        public async Task<BaseResponseModel> GenericPostObject<TType>(string requeststring, object objectToPost)
            where TType : BaseResponseModel
        {
            try
            {
                var res = requeststring.PostJsonAsync(objectToPost).Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = JsonConvert.DeserializeObject<TType>(content);
                responseModel.StatusCode = (int) res.StatusCode;
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
        
        public BaseResponseModel GenericDeleteObject(string requeststring)
        {
            try
            {
                var res = requeststring.DeleteAsync().Result;
                var responseModel = new BaseResponseModel
                {
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
        
                
        public async Task<BaseResponseModel> GenericUpdateObject<TType>(string requeststring, object objectToPost)
            where TType : BaseResponseModel
        {
            try
            {
                var res = requeststring.PostJsonAsync(objectToPost).Result;
                var content = res.Content.ReadAsStringAsync().Result;
                var responseModel = JsonConvert.DeserializeObject<TType>(content);
                responseModel.StatusCode = (int) res.StatusCode;
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