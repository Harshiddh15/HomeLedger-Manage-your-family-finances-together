namespace FinanceManagementNet.Models
{
    public class DashboardViewModel
    {
        public decimal TotalIncome { get; set; }
        public decimal TotalExpense { get; set; }
        public decimal RemainingBalance { get; set; }
        public decimal TotalLene { get; set; }
        public decimal TotalDene { get; set; }
        public List<RecentActivity> RecentActivities { get; set; } = new List<RecentActivity>();
    }

    public class RecentActivity
    {
        public string Type { get; set; } = string.Empty;
        public string Title { get; set; } = string.Empty;
        public decimal Amount { get; set; }
        public DateTime Date { get; set; }
    }
}
