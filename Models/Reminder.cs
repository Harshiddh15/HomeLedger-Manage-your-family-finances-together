using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Models
{
    public class Reminder
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int FamilyId { get; set; }

        [Required]
        [StringLength(150)]
        public string Title { get; set; } = string.Empty;

        [Required]
        [Column(TypeName = "date")]
        public DateTime Date { get; set; }

        public string? Description { get; set; }

        [JsonIgnore]
        [ForeignKey("FamilyId")]
        public Family? Family { get; set; }
    }
}
