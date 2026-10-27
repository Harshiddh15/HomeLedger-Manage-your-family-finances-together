using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Models
{
    public class Family
    {
        [Key]
        public int Id { get; set; }

        [Required]
        [StringLength(100)]
        public string FamilyName { get; set; } = string.Empty;

        [Required]
        [StringLength(50)]
        [Column("family_id")]
        public string FamilyId { get; set; } = string.Empty;

        [Required]
        [StringLength(255)]
        [JsonIgnore]
        public string Password { get; set; } = string.Empty;

        public DateTime CreatedAt { get; set; } = DateTime.UtcNow;

        [JsonIgnore]
        public ICollection<Member> Members { get; set; } = new List<Member>();

        [JsonIgnore]
        public ICollection<Income> Incomes { get; set; } = new List<Income>();

        [JsonIgnore]
        public ICollection<Expense> Expenses { get; set; } = new List<Expense>();

        [JsonIgnore]
        public ICollection<Udhar> Udhar { get; set; } = new List<Udhar>();

        [JsonIgnore]
        public ICollection<Reminder> Reminders { get; set; } = new List<Reminder>();

        [JsonIgnore]
        public ICollection<Budget> Budgets { get; set; } = new List<Budget>();

        [JsonIgnore]
        public ICollection<SavingsGoal> SavingsGoals { get; set; } = new List<SavingsGoal>();

        [JsonIgnore]
        public ICollection<RecurringExpense> RecurringExpenses { get; set; } = new List<RecurringExpense>();

        [JsonIgnore]
        public ICollection<RecurringIncome> RecurringIncomes { get; set; } = new List<RecurringIncome>();
    }
}
