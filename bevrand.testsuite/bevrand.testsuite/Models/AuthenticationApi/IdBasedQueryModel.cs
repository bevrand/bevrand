namespace bevrand.testsuite.Models.AuthenticationApi
{
    public interface IIdBasedQueryModel
    {
        int Id { get; set; }
    }

    public class IdBasedQueryModel : IIdBasedQueryModel
    {
        public int Id { get; set; }
    }
}