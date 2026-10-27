using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Linq;

namespace FinanceManagementNet.Controllers
{
    public class ReportController : Controller
    {
        private readonly AppDbContext _context;

        public ReportController(AppDbContext context)
        {
            _context = context;
        }

        public IActionResult Index()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            return View();
        }

        public IActionResult MonthlyReport(int? year, int? month)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            int targetYear = (year.HasValue && year.Value >= 2000 && year.Value <= 2100) ? year.Value : DateTime.Now.Year;
            int targetMonth = (month.HasValue && month.Value >= 1 && month.Value <= 12) ? month.Value : DateTime.Now.Month;

            var startDate = new DateTime(targetYear, targetMonth, 1);
            var endDate = startDate.AddMonths(1).AddDays(-1);

            var incomes = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value && i.Date >= startDate && i.Date <= endDate)
                .ToList();

            var expenses = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value && e.Date >= startDate && e.Date <= endDate)
                .ToList();

            var categoryWiseExpenses = expenses
                .GroupBy(e => e.Category)
                .Select(g => new CategoryWiseExpense { Category = g.Key, Amount = g.Sum(e => e.Amount) })
                .ToList();

            var viewModel = new MonthlyReportViewModel
            {
                Year = targetYear,
                Month = targetMonth,
                TotalIncome = incomes.Sum(i => i.Amount),
                TotalExpense = expenses.Sum(e => e.Amount),
                Incomes = incomes,
                Expenses = expenses,
                CategoryWiseExpenses = categoryWiseExpenses
            };

            return View(viewModel);
        }

        public IActionResult YearlyReport(int? year)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            int targetYear = (year.HasValue && year.Value >= 2000 && year.Value <= 2100) ? year.Value : DateTime.Now.Year;

            var startDate = new DateTime(targetYear, 1, 1);
            var endDate = new DateTime(targetYear, 12, 31);

            var incomes = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value && i.Date >= startDate && i.Date <= endDate)
                .ToList();

            var expenses = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value && e.Date >= startDate && e.Date <= endDate)
                .ToList();

            var monthlyData = new List<object>();
            for (int m = 1; m <= 12; m++)
            {
                var monthStart = new DateTime(targetYear, m, 1);
                var monthEnd = monthStart.AddMonths(1).AddDays(-1);

                monthlyData.Add(new
                {
                    Month = m,
                    Income = incomes.Where(i => i.Date >= monthStart && i.Date <= monthEnd).Sum(i => i.Amount),
                    Expense = expenses.Where(e => e.Date >= monthStart && e.Date <= monthEnd).Sum(e => e.Amount)
                });
            }

            var viewModel = new
            {
                Year = targetYear,
                TotalIncome = incomes.Sum(i => i.Amount),
                TotalExpense = expenses.Sum(e => e.Amount),
                MonthlyData = monthlyData
            };

            return View(viewModel);
        }
    }
}
