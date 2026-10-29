using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System;
using System.Collections.Generic;
using System.Globalization;
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
                .OrderBy(i => i.Date)
                .ToList();

            var expenses = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value && e.Date >= startDate && e.Date <= endDate)
                .OrderBy(e => e.Date)
                .ToList();

            var categoryWiseExpenses = expenses
                .GroupBy(e => string.IsNullOrWhiteSpace(e.Category) ? "General" : e.Category)
                .Select(g => new CategoryWiseExpense { Category = g.Key, Amount = g.Sum(e => e.Amount) })
                .OrderByDescending(c => c.Amount)
                .ToList();

            var categoryWiseIncomes = incomes
                .GroupBy(i => string.IsNullOrWhiteSpace(i.Source) ? "Other" : i.Source)
                .Select(g => new CategoryWiseIncome { Source = g.Key, Amount = g.Sum(i => i.Amount) })
                .OrderByDescending(c => c.Amount)
                .ToList();

            int daysInMonth = DateTime.DaysInMonth(targetYear, targetMonth);
            var dailyData = new List<DailyReportItem>();
            for (int day = 1; day <= daysInMonth; day++)
            {
                var dayDate = new DateTime(targetYear, targetMonth, day);
                var dayIncome = incomes.Where(i => i.Date.Date == dayDate).Sum(i => i.Amount);
                var dayExpense = expenses.Where(e => e.Date.Date == dayDate).Sum(e => e.Amount);
                
                dailyData.Add(new DailyReportItem
                {
                    Day = day,
                    DateLabel = $"{day:D2} {dayDate:MMM}",
                    Income = dayIncome,
                    Expense = dayExpense
                });
            }

            var viewModel = new MonthlyReportViewModel
            {
                Year = targetYear,
                Month = targetMonth,
                TotalIncome = incomes.Sum(i => i.Amount),
                TotalExpense = expenses.Sum(e => e.Amount),
                Incomes = incomes,
                Expenses = expenses,
                CategoryWiseExpenses = categoryWiseExpenses,
                CategoryWiseIncomes = categoryWiseIncomes,
                DailyData = dailyData
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

            var monthlyData = new List<MonthlyOverviewItem>();
            for (int m = 1; m <= 12; m++)
            {
                var monthStart = new DateTime(targetYear, m, 1);
                var monthEnd = monthStart.AddMonths(1).AddDays(-1);

                monthlyData.Add(new MonthlyOverviewItem
                {
                    Month = m,
                    MonthName = CultureInfo.CurrentCulture.DateTimeFormat.GetMonthName(m),
                    Income = incomes.Where(i => i.Date >= monthStart && i.Date <= monthEnd).Sum(i => i.Amount),
                    Expense = expenses.Where(e => e.Date >= monthStart && e.Date <= monthEnd).Sum(e => e.Amount)
                });
            }

            var viewModel = new YearlyReportViewModel
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
