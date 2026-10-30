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

            var loginType = HttpContext.Session.GetString("LoginType");
            var memberName = HttpContext.Session.GetString("MemberName");

            var query = _context.Udhar.Where(u => u.FamilyId == familyDbId.Value);

            // Members only see their own udhar entries
            if (loginType == "Member")
            {
                query = query.Where(u => u.MemberName == memberName);
            }

            var udharRecords = query.OrderByDescending(u => u.Date).ToList();

            ViewBag.IsMember = (loginType == "Member");
            ViewBag.MemberName = memberName;
            return View(udharRecords);
        }

        public IActionResult Create()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            var memberName = HttpContext.Session.GetString("MemberName");

            var udhar = new Udhar
            {
                Date = DateTime.Today,
                MemberName = (loginType == "Member" ? memberName : "")
            };

            ViewBag.IsMember = (loginType == "Member");
            ViewBag.MemberName = memberName;
            return View(udhar);
        }

        [HttpPost]
        public IActionResult Create(Udhar udhar)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            var memberName = HttpContext.Session.GetString("MemberName");

            // Enforce logged in member's name for member accounts
            if (loginType == "Member")
            {
                udhar.MemberName = memberName ?? "Member";
            }

            if (ModelState.IsValid)
            {
                udhar.FamilyId = familyDbId.Value;
                udhar.RemainingAmount = udhar.Amount - udhar.PaidAmount;
                udhar.Status = udhar.RemainingAmount <= 0 ? "Completed" : "Pending";
                _context.Udhar.Add(udhar);
                _context.SaveChanges();

                TempData["Success"] = "Udhar record successfully added!";

                // Members stay strictly inside Member Dashboard
                if (loginType == "Member")
                {
                    return RedirectToAction("MemberDashboard", "Home");
                }

                return RedirectToAction("Index");
            }

            ViewBag.IsMember = (loginType == "Member");
            ViewBag.MemberName = memberName;
            return View(udhar);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot edit udhar records.";
                return RedirectToAction("MemberDashboard", "Home");
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

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot edit udhar records.";
                return RedirectToAction("MemberDashboard", "Home");
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
                TempData["Success"] = "Udhar record updated successfully.";
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

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot delete udhar records.";
                return RedirectToAction("MemberDashboard", "Home");
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

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot delete udhar records.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var udhar = _context.Udhar.FirstOrDefault(u => u.Id == id && u.FamilyId == familyDbId.Value);
            if (udhar != null)
            {
                _context.Udhar.Remove(udhar);
                _context.SaveChanges();
                TempData["Success"] = "Udhar record deleted successfully.";
            }

            return RedirectToAction("Index");
        }
    }
}
