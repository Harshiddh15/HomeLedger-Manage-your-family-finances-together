using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Models
{
    public class SavingsGoal
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int FamilyId { get; set; }

        [Required]
        [StringLength(150)]
        public string GoalName { get; set; } = string.Empty;

        [Required]
        [Column(TypeName = "decimal(10,2)")]
        public decimal TargetAmount { get; set; }

        [Required]
        [Column(TypeName = "decimal(10,2)")]
        public decimal CurrentAmount { get; set; }

        [Required]
        [Column(TypeName = "date")]
        public DateTime TargetDate { get; set; }

        public string? Description { get; set; }

        [JsonIgnore]
        [ForeignKey("FamilyId")]
        public Family? Family { get; set; }
    }
}
