using System.Collections.Generic;

namespace FinanceManagementNet.Models
{
    public class YearlyReportViewModel
    {
        public int Year { get; set; }
        public decimal TotalIncome { get; set; }
        public decimal TotalExpense { get; set; }
        public List<MonthlyOverviewItem> MonthlyData { get; set; } = new();
    }

    public class MonthlyOverviewItem
    {
        public int Month { get; set; }
        public string MonthName { get; set; } = string.Empty;
        public decimal Income { get; set; }
        public decimal Expense { get; set; }
        public decimal Balance => Income - Expense;
    }
}
