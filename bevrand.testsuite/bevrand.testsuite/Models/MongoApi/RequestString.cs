namespace bevrand.testsuite.Models.MongoApi
{
    public interface IRequestString
    {
        string user { get; set; }
        string list { get; set; }
    }

    public class RequestString : IRequestString
    {
        public string user { get; set; }
        public string list { get; set; }
    }
}