using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    public class RecurringExpenseController : Controller
    {
        private readonly AppDbContext _context;

        public RecurringExpenseController(AppDbContext context)
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

            var expenses = _context.RecurringExpenses
                .Where(r => r.FamilyId == familyDbId.Value)
                .OrderBy(r => r.DayOfMonth)
                .ToList();

            return View(expenses);
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
        public IActionResult Create(RecurringExpense expense)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                expense.FamilyId = familyDbId.Value;
                _context.RecurringExpenses.Add(expense);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(expense);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var expense = _context.RecurringExpenses.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (expense == null)
            {
                return NotFound();
            }

            return View(expense);
        }

        [HttpPost]
        public IActionResult Edit(RecurringExpense expense)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingExpense = _context.RecurringExpenses.FirstOrDefault(r => r.Id == expense.Id && r.FamilyId == familyDbId.Value);
                if (existingExpense == null)
                {
                    return NotFound();
                }

                existingExpense.MemberName = expense.MemberName;
                existingExpense.Category = expense.Category;
                existingExpense.Amount = expense.Amount;
                existingExpense.Frequency = expense.Frequency;
                existingExpense.DayOfMonth = expense.DayOfMonth;
                existingExpense.Description = expense.Description;
                existingExpense.IsActive = expense.IsActive;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(expense);
        }

        public IActionResult ToggleActive(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var expense = _context.RecurringExpenses.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (expense != null)
            {
                expense.IsActive = !expense.IsActive;
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

            var expense = _context.RecurringExpenses.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (expense == null)
            {
                return NotFound();
            }

            return View(expense);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var expense = _context.RecurringExpenses.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (expense != null)
            {
                _context.RecurringExpenses.Remove(expense);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}
