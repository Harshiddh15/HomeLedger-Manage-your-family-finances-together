using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Linq;

namespace FinanceManagementNet.Controllers
{
    public class HomeController : Controller
    {
        private readonly AppDbContext _context;

        public HomeController(AppDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            if (HttpContext.Session.GetInt32("FamilyDbId") == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType == "Member")
            {
                return RedirectToAction("MemberDashboard");
            }

            return RedirectToAction("Dashboard");
        }

        public IActionResult Dashboard()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType == "Member")
            {
                TempData["Error"] = "Admin Dashboard is locked for Member accounts. You have been redirected to Member Portal.";
                return RedirectToAction("MemberDashboard");
            }

            // Get Total Income (Family Total)
            var totalIncome = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value)
                .Sum(i => (decimal?)i.Amount) ?? 0;

            // Get Total Expense (Family Total)
            var totalExpense = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value)
                .Sum(e => (decimal?)e.Amount) ?? 0;

            var remainingBalance = totalIncome - totalExpense;

            // Get Udhar (Lene Hai) - money given to others
            var totalLene = _context.Udhar
                .Where(u => u.FamilyId == familyDbId.Value && u.Type == "Lene Hai" && u.Status == "Pending")
                .Sum(u => (decimal?)u.RemainingAmount) ?? 0;

            // Get Udhar (Dene Hai) - money taken from others
            var totalDene = _context.Udhar
                .Where(u => u.FamilyId == familyDbId.Value && u.Type == "Dene Hai" && u.Status == "Pending")
                .Sum(u => (decimal?)u.RemainingAmount) ?? 0;

            // Get Recent Activities
            var incomeActivities = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value)
                .Select(i => new RecentActivity
                {
                    Type = "Income",
                    Title = i.Source,
                    Amount = i.Amount,
                    Date = i.Date
                });

            var expenseActivities = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value)
                .Select(e => new RecentActivity
                {
                    Type = "Expense",
                    Title = e.Category,
                    Amount = e.Amount,
                    Date = e.Date
                });

            var activities = incomeActivities
                .Union(expenseActivities)
                .OrderByDescending(a => a.Date)
                .Take(5)
                .ToList();

            var viewModel = new DashboardViewModel
            {
                TotalIncome = totalIncome,
                TotalExpense = totalExpense,
                RemainingBalance = remainingBalance,
                TotalLene = totalLene,
                TotalDene = totalDene,
                RecentActivities = activities
            };

            return View(viewModel);
        }

        public IActionResult MemberDashboard()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var memberName = HttpContext.Session.GetString("MemberName") ?? "Member";

            // Member-specific statistics
            var myIncome = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value && i.MemberName == memberName)
                .Sum(i => (decimal?)i.Amount) ?? 0;

            var myExpenses = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value && e.MemberName == memberName)
                .Sum(e => (decimal?)e.Amount) ?? 0;

            var myUdharDene = _context.Udhar
                .Where(u => u.FamilyId == familyDbId.Value && u.MemberName == memberName && u.Type == "Dene Hai" && u.Status == "Pending")
                .Sum(u => (decimal?)u.RemainingAmount) ?? 0;

            var myUdharLene = _context.Udhar
                .Where(u => u.FamilyId == familyDbId.Value && u.MemberName == memberName && u.Type == "Lene Hai" && u.Status == "Pending")
                .Sum(u => (decimal?)u.RemainingAmount) ?? 0;

            // Member-specific recent activities
            var incomeActivities = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value && i.MemberName == memberName)
                .Select(i => new RecentActivity
                {
                    Type = "Income",
                    Title = i.Source,
                    Amount = i.Amount,
                    Date = i.Date
                });

            var expenseActivities = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value && e.MemberName == memberName)
                .Select(e => new RecentActivity
                {
                    Type = "Expense",
                    Title = e.Category,
                    Amount = e.Amount,
                    Date = e.Date
                });

            var activities = incomeActivities
                .Union(expenseActivities)
                .OrderByDescending(a => a.Date)
                .Take(6)
                .ToList();

            var viewModel = new DashboardViewModel
            {
                TotalIncome = myIncome,
                TotalExpense = myExpenses,
                RemainingBalance = myIncome - myExpenses,
                TotalLene = myUdharLene,
                TotalDene = myUdharDene,
                RecentActivities = activities
            };

            ViewBag.MemberName = memberName;
            ViewBag.FamilyName = HttpContext.Session.GetString("FamilyName") ?? "Family";

            return View(viewModel);
        }

        public IActionResult Privacy()
        {
            return View();
        }
    }
}
