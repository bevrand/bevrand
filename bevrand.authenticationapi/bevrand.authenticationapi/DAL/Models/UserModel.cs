using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace bevrand.authenticationapi.Models
{
    public class UserModel
    {
        [Key]
        [Column]
        public int Id { get; set; }
        
        [Column]
        public string UserName { get; set; }
        
        [Column]
        public string PassWord { get; set; }
        
        [Column]
        public string Session { get; set; }
        
        [Column]
        public DateTime Created { get; set; } = DateTime.UtcNow;
        
        [Column]
        public DateTime Updated { get; set; } = DateTime.UtcNow;
    }
}