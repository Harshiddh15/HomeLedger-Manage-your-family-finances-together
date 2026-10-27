using FinanceManagementNet.Models;

namespace FinanceManagementNet.Models
{
    public class MonthlyReportViewModel
    {
        public int Year { get; set; }
        public int Month { get; set; }
        public decimal TotalIncome { get; set; }
        public decimal TotalExpense { get; set; }
        public List<Income> Incomes { get; set; } = new();
        public List<Expense> Expenses { get; set; } = new();
        public List<CategoryWiseExpense> CategoryWiseExpenses { get; set; } = new();
    }

    public class CategoryWiseExpense
    {
        public string Category { get; set; } = string.Empty;
        public decimal Amount { get; set; }
    }
}
