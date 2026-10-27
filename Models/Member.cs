using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Models
{
    public class Member
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int FamilyId { get; set; }

        [Required]
        [StringLength(100)]
        public string MemberName { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        public string Relation { get; set; } = string.Empty;

        [StringLength(15)]
        public string? Mobile { get; set; }

        [StringLength(255)]
        public string? ProfileImage { get; set; }

        [StringLength(255)]
        [JsonIgnore]
        public string? Password { get; set; }

        [JsonIgnore]
        [ForeignKey("FamilyId")]
        public Family? Family { get; set; }
    }
}
