namespace bevrand.testsuite.Models
{
    public class BaseErrorResponse : BaseResponseModel
    {
        public string ErrorMessage { get; set; }
        
        public string UserError { get; set; }
    }
}