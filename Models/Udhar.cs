using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Models
{
    public class Udhar
    {
        [Key]
        public int Id { get; set; }

        [Required]
        public int FamilyId { get; set; }

        [Required]
        [StringLength(100)]
        public string PersonName { get; set; } = string.Empty;

        [StringLength(100)]
        public string? MemberName { get; set; }

        [StringLength(255)]
        public string? ProofImage { get; set; }

        [Required]
        public string Type { get; set; } = string.Empty; // 'Lene Hai' or 'Dene Hai'

        [Required]
        [Column(TypeName = "decimal(10,2)")]
        public decimal Amount { get; set; }

        [Column(TypeName = "decimal(10,2)")]
        public decimal PaidAmount { get; set; } = 0.00m;

        [Required]
        [Column(TypeName = "decimal(10,2)")]
        public decimal RemainingAmount { get; set; }

        public string? Reason { get; set; }

        [Required]
        [Column(TypeName = "date")]
        public DateTime Date { get; set; }

        [Required]
        public string Status { get; set; } = "Pending"; // 'Pending' or 'Completed'

        [JsonIgnore]
        [ForeignKey("FamilyId")]
        public Family? Family { get; set; }
    }
}
