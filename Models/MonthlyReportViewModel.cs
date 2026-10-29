using FinanceManagementNet.Models;
using System.Collections.Generic;

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
        public List<CategoryWiseIncome> CategoryWiseIncomes { get; set; } = new();
        public List<DailyReportItem> DailyData { get; set; } = new();
    }

    public class CategoryWiseExpense
    {
        public string Category { get; set; } = string.Empty;
        public decimal Amount { get; set; }
    }

    public class CategoryWiseIncome
    {
        public string Source { get; set; } = string.Empty;
        public decimal Amount { get; set; }
    }

    public class DailyReportItem
    {
        public int Day { get; set; }
        public string DateLabel { get; set; } = string.Empty;
        public decimal Income { get; set; }
        public decimal Expense { get; set; }
    }
}
