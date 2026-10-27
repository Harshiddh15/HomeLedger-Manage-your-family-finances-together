using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    public class SavingsGoalController : Controller
    {
        private readonly AppDbContext _context;

        public SavingsGoalController(AppDbContext context)
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

            var goals = _context.SavingsGoals
                .Where(s => s.FamilyId == familyDbId.Value)
                .OrderBy(s => s.TargetDate)
                .ToList();

            return View(goals);
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
        public IActionResult Create(SavingsGoal goal)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                goal.FamilyId = familyDbId.Value;
                goal.CurrentAmount = 0;
                _context.SavingsGoals.Add(goal);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(goal);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var goal = _context.SavingsGoals.FirstOrDefault(s => s.Id == id && s.FamilyId == familyDbId.Value);
            if (goal == null)
            {
                return NotFound();
            }

            return View(goal);
        }

        [HttpPost]
        public IActionResult Edit(SavingsGoal goal)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingGoal = _context.SavingsGoals.FirstOrDefault(s => s.Id == goal.Id && s.FamilyId == familyDbId.Value);
                if (existingGoal == null)
                {
                    return NotFound();
                }

                existingGoal.GoalName = goal.GoalName;
                existingGoal.TargetAmount = goal.TargetAmount;
                existingGoal.CurrentAmount = goal.CurrentAmount;
                existingGoal.TargetDate = goal.TargetDate;
                existingGoal.Description = goal.Description;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(goal);
        }

        public IActionResult AddAmount(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var goal = _context.SavingsGoals.FirstOrDefault(s => s.Id == id && s.FamilyId == familyDbId.Value);
            if (goal == null)
            {
                return NotFound();
            }

            return View(goal);
        }

        [HttpPost]
        public IActionResult AddAmount(int id, decimal amount)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var goal = _context.SavingsGoals.FirstOrDefault(s => s.Id == id && s.FamilyId == familyDbId.Value);
            if (goal != null && amount > 0)
            {
                goal.CurrentAmount += amount;
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

            var goal = _context.SavingsGoals.FirstOrDefault(s => s.Id == id && s.FamilyId == familyDbId.Value);
            if (goal == null)
            {
                return NotFound();
            }

            return View(goal);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var goal = _context.SavingsGoals.FirstOrDefault(s => s.Id == id && s.FamilyId == familyDbId.Value);
            if (goal != null)
            {
                _context.SavingsGoals.Remove(goal);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}
