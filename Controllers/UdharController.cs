using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    public class UdharController : Controller
    {
        private readonly AppDbContext _context;

        public UdharController(AppDbContext context)
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

            var udharRecords = _context.Udhar
                .Where(u => u.FamilyId == familyDbId.Value)
                .OrderByDescending(u => u.Date)
                .ToList();

            return View(udharRecords);
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
        public IActionResult Create(Udhar udhar)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                udhar.FamilyId = familyDbId.Value;
                udhar.RemainingAmount = udhar.Amount - udhar.PaidAmount;
                udhar.Status = "Pending";
                _context.Udhar.Add(udhar);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(udhar);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var udhar = _context.Udhar.FirstOrDefault(u => u.Id == id && u.FamilyId == familyDbId.Value);
            if (udhar == null)
            {
                return NotFound();
            }

            return View(udhar);
        }

        [HttpPost]
        public IActionResult Edit(Udhar udhar)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingUdhar = _context.Udhar.FirstOrDefault(u => u.Id == udhar.Id && u.FamilyId == familyDbId.Value);
                if (existingUdhar == null)
                {
                    return NotFound();
                }

                existingUdhar.PersonName = udhar.PersonName;
                existingUdhar.MemberName = udhar.MemberName;
                existingUdhar.Type = udhar.Type;
                existingUdhar.Amount = udhar.Amount;
                existingUdhar.PaidAmount = udhar.PaidAmount;
                existingUdhar.RemainingAmount = udhar.Amount - udhar.PaidAmount;
                existingUdhar.Reason = udhar.Reason;
                existingUdhar.Date = udhar.Date;
                existingUdhar.Status = udhar.RemainingAmount <= 0 ? "Completed" : "Pending";

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(udhar);
        }

        public IActionResult Delete(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var udhar = _context.Udhar.FirstOrDefault(u => u.Id == id && u.FamilyId == familyDbId.Value);
            if (udhar == null)
            {
                return NotFound();
            }

            return View(udhar);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var udhar = _context.Udhar.FirstOrDefault(u => u.Id == id && u.FamilyId == familyDbId.Value);
            if (udhar != null)
            {
                _context.Udhar.Remove(udhar);
                _context.SaveChanges();
            }

            return RedirectToAction("Index");
        }
    }
}
