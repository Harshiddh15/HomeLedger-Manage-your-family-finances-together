using FinanceManagementNet.Filters;
using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    [AdminOnly]
    public class RecurringIncomeController : Controller
    {
        private readonly AppDbContext _context;

        public RecurringIncomeController(AppDbContext context)
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

            var incomes = _context.RecurringIncomes
                .Where(r => r.FamilyId == familyDbId.Value)
                .OrderBy(r => r.DayOfMonth)
                .ToList();

            return View(incomes);
        }

        public IActionResult Create()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            return View();
        }

        [HttpPost]
        public IActionResult Create(RecurringIncome income)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                income.FamilyId = familyDbId.Value;
                _context.RecurringIncomes.Add(income);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(income);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.RecurringIncomes.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (income == null)
            {
                return NotFound();
            }

            return View(income);
        }

        [HttpPost]
        public IActionResult Edit(RecurringIncome income)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingIncome = _context.RecurringIncomes.FirstOrDefault(r => r.Id == income.Id && r.FamilyId == familyDbId.Value);
                if (existingIncome == null)
                {
                    return NotFound();
                }

                existingIncome.MemberName = income.MemberName;
                existingIncome.Source = income.Source;
                existingIncome.Amount = income.Amount;
                existingIncome.Frequency = income.Frequency;
                existingIncome.DayOfMonth = income.DayOfMonth;
                existingIncome.Description = income.Description;
                existingIncome.IsActive = income.IsActive;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(income);
        }

        public IActionResult ToggleActive(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.RecurringIncomes.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (income != null)
            {
                income.IsActive = !income.IsActive;
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }

        public IActionResult Delete(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.RecurringIncomes.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (income == null)
            {
                return NotFound();
            }

            return View(income);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.RecurringIncomes.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (income != null)
            {
                _context.RecurringIncomes.Remove(income);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}

