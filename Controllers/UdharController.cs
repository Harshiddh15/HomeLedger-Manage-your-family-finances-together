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

            // Remove calculated/navigation properties from validation
            ModelState.Remove("FamilyId");
            ModelState.Remove("RemainingAmount");
            ModelState.Remove("Status");
            ModelState.Remove("Family");

            if (ModelState.IsValid)
            {
                udhar.FamilyId = familyDbId.Value;

                // Ensure non-negative and bounded paid amount
                if (udhar.PaidAmount < 0) udhar.PaidAmount = 0;
                if (udhar.PaidAmount > udhar.Amount) udhar.PaidAmount = udhar.Amount;

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

            // Remove calculated/navigation properties from validation
            ModelState.Remove("FamilyId");
            ModelState.Remove("RemainingAmount");
            ModelState.Remove("Status");
            ModelState.Remove("Family");

            if (ModelState.IsValid)
            {
                var existingUdhar = _context.Udhar.FirstOrDefault(u => u.Id == udhar.Id && u.FamilyId == familyDbId.Value);
                if (existingUdhar == null)
                {
                    return NotFound();
                }

                // Validate and clamp paid amount
                if (udhar.PaidAmount < 0) udhar.PaidAmount = 0;
                if (udhar.PaidAmount > udhar.Amount) udhar.PaidAmount = udhar.Amount;

                existingUdhar.PersonName = udhar.PersonName;
                existingUdhar.MemberName = udhar.MemberName;
                existingUdhar.Type = udhar.Type;
                existingUdhar.Amount = udhar.Amount;
                existingUdhar.PaidAmount = udhar.PaidAmount;
                existingUdhar.RemainingAmount = existingUdhar.Amount - existingUdhar.PaidAmount;
                existingUdhar.Reason = udhar.Reason;
                existingUdhar.Date = udhar.Date;
                
                // CRITICAL FIX: Base status on existingUdhar.RemainingAmount
                existingUdhar.Status = existingUdhar.RemainingAmount <= 0 ? "Completed" : "Pending";

                _context.SaveChanges();
                TempData["Success"] = "Udhar record updated successfully.";
                return RedirectToAction("Index");
            }

            return View(udhar);
        }

        [HttpPost]
        public IActionResult Settle(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot settle udhar records.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var udhar = _context.Udhar.FirstOrDefault(u => u.Id == id && u.FamilyId == familyDbId.Value);
            if (udhar != null)
            {
                udhar.PaidAmount = udhar.Amount;
                udhar.RemainingAmount = 0;
                udhar.Status = "Completed";
                _context.SaveChanges();
                TempData["Success"] = $"Udhar record for {udhar.PersonName} has been fully settled!";
            }

            return RedirectToAction("Index");
        }

        [HttpPost]
        public IActionResult Reopen(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var udhar = _context.Udhar.FirstOrDefault(u => u.Id == id && u.FamilyId == familyDbId.Value);
            if (udhar != null)
            {
                udhar.PaidAmount = 0;
                udhar.RemainingAmount = udhar.Amount;
                udhar.Status = "Pending";
                _context.SaveChanges();
                TempData["Success"] = $"Udhar record for {udhar.PersonName} has been reopened as pending.";
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
