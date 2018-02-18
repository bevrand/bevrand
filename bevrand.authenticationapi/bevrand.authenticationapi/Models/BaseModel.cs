namespace bevrand.authenticationapi.Models
{
    public class BaseModel
    {
        public virtual string Username { get; set; }
        
        public int ?Id { get; set; }
    }
}