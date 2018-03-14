using System;
using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace bevrand.authenticationapi.DAL.Models
{
    [Table("users")]
    public class UserModel
    {
        [Key]
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        [Column("id")]
        public int Id { get; set; }
        
        [Column("username")]
        public string UserName { get; set; }
        
        [Column("email")]
        public string EmailAddress { get; set; }
        
        [Column("password")]
        public string PassWord { get; set; }
        
        [Column("active")]
        public bool? Active { get; set; }
        
        [DatabaseGenerated(DatabaseGeneratedOption.Identity)]
        [Column("datecreated")]
        public DateTime Created { get; set; }
        
        
        [Column("dateupdated")]
        public DateTime Updated { get; set; } = DateTime.UtcNow;
    }
}