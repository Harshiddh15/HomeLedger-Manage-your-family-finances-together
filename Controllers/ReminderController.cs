using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    public class ReminderController : Controller
    {
        private readonly AppDbContext _context;

        public ReminderController(AppDbContext context)
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

            var reminders = _context.Reminders
                .Where(r => r.FamilyId == familyDbId.Value)
                .OrderBy(r => r.Date)
                .ToList();

            return View(reminders);
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
        public IActionResult Create(Reminder reminder)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                reminder.FamilyId = familyDbId.Value;
                _context.Reminders.Add(reminder);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(reminder);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var reminder = _context.Reminders.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (reminder == null)
            {
                return NotFound();
            }

            return View(reminder);
        }

        [HttpPost]
        public IActionResult Edit(Reminder reminder)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingReminder = _context.Reminders.FirstOrDefault(r => r.Id == reminder.Id && r.FamilyId == familyDbId.Value);
                if (existingReminder == null)
                {
                    return NotFound();
                }

                existingReminder.Title = reminder.Title;
                existingReminder.Date = reminder.Date;
                existingReminder.Description = reminder.Description;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(reminder);
        }

        public IActionResult Delete(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var reminder = _context.Reminders.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (reminder == null)
            {
                return NotFound();
            }

            return View(reminder);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var reminder = _context.Reminders.FirstOrDefault(r => r.Id == id && r.FamilyId == familyDbId.Value);
            if (reminder != null)
            {
                _context.Reminders.Remove(reminder);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}
