using FinanceManagementNet.Filters;
using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    [AdminOnly]
    public class BudgetController : Controller
    {
        private readonly AppDbContext _context;

        public BudgetController(AppDbContext context)
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

            var budgets = _context.Budgets
                .Where(b => b.FamilyId == familyDbId.Value)
                .OrderByDescending(b => b.Month)
                .ToList();

            return View(budgets);
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
        public IActionResult Create(Budget budget)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                budget.FamilyId = familyDbId.Value;
                _context.Budgets.Add(budget);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(budget);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var budget = _context.Budgets.FirstOrDefault(b => b.Id == id && b.FamilyId == familyDbId.Value);
            if (budget == null)
            {
                return NotFound();
            }

            return View(budget);
        }

        [HttpPost]
        public IActionResult Edit(Budget budget)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingBudget = _context.Budgets.FirstOrDefault(b => b.Id == budget.Id && b.FamilyId == familyDbId.Value);
                if (existingBudget == null)
                {
                    return NotFound();
                }

                existingBudget.Category = budget.Category;
                existingBudget.Amount = budget.Amount;
                existingBudget.Month = budget.Month;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(budget);
        }

        public IActionResult Delete(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var budget = _context.Budgets.FirstOrDefault(b => b.Id == id && b.FamilyId == familyDbId.Value);
            if (budget == null)
            {
                return NotFound();
            }

            return View(budget);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var budget = _context.Budgets.FirstOrDefault(b => b.Id == id && b.FamilyId == familyDbId.Value);
            if (budget != null)
            {
                _context.Budgets.Remove(budget);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}

