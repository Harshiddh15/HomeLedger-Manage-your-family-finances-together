using FinanceManagementNet.Filters;
using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
    [AdminOnly]
    public class MemberController : Controller
    {
        private readonly AppDbContext _context;

        public MemberController(AppDbContext context)
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

            var members = _context.Members
                .Where(m => m.FamilyId == familyDbId.Value)
                .OrderBy(m => m.Id)
                .ToList();

            return View(members);
        }

        public IActionResult Create()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            return View(new Member());
        }

        [HttpPost]
        public IActionResult Create(Member member)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (string.IsNullOrWhiteSpace(member.MemberName) || string.IsNullOrWhiteSpace(member.Relation))
            {
                ModelState.AddModelError("", "Member Name aur Relation required hain.");
                return View(member);
            }

            member.FamilyId = familyDbId.Value;
            member.MemberName = member.MemberName.Trim();
            member.Relation = member.Relation.Trim();
            member.Mobile = member.Mobile?.Trim();
            member.ProfileImage = member.ProfileImage?.Trim();

            var rel = member.Relation.ToLower();
            var name = member.MemberName.ToLower();

            if (rel == "father" || rel == "head" || name == "father")
            {
                member.Password = null; // Father/Head uses Admin Login
            }
            else if (!string.IsNullOrWhiteSpace(member.Password))
            {
                member.Password = BCrypt.Net.BCrypt.HashPassword(member.Password.Trim());
            }
            else
            {
                // Default password is 123 if left blank
                member.Password = BCrypt.Net.BCrypt.HashPassword("123");
            }

            _context.Members.Add(member);
            _context.SaveChanges();

            TempData["Success"] = $"Member '{member.MemberName}' successfully add ho gaya!";
            return RedirectToAction("Index");
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var member = _context.Members.FirstOrDefault(m => m.Id == id && m.FamilyId == familyDbId.Value);
            if (member == null)
            {
                return NotFound();
            }

            return View(member);
        }

        [HttpPost]
        public IActionResult Edit(Member member)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (string.IsNullOrWhiteSpace(member.MemberName) || string.IsNullOrWhiteSpace(member.Relation))
            {
                ModelState.AddModelError("", "Member Name aur Relation required hain.");
                return View(member);
            }

            var existingMember = _context.Members.FirstOrDefault(m => m.Id == member.Id && m.FamilyId == familyDbId.Value);
            if (existingMember == null)
            {
                return NotFound();
            }

            existingMember.MemberName = member.MemberName.Trim();
            existingMember.Relation = member.Relation.Trim();
            existingMember.Mobile = member.Mobile?.Trim();
            existingMember.ProfileImage = member.ProfileImage?.Trim();

            var rel = member.Relation.ToLower();
            var name = member.MemberName.ToLower();

            if (rel == "father" || rel == "head" || name == "father")
            {
                existingMember.Password = null; // Father must use Admin Login
            }
            else if (!string.IsNullOrWhiteSpace(member.Password))
            {
                // Admin entered a new password to update
                existingMember.Password = BCrypt.Net.BCrypt.HashPassword(member.Password.Trim());
            }
            // else keep existingMember.Password unchanged!

            _context.SaveChanges();
            TempData["Success"] = $"Member '{existingMember.MemberName}' details successfully update ho gayi!";
            return RedirectToAction("Index");
        }

        public IActionResult Delete(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var member = _context.Members.FirstOrDefault(m => m.Id == id && m.FamilyId == familyDbId.Value);
            if (member == null)
            {
                return NotFound();
            }

            return View(member);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var member = _context.Members.FirstOrDefault(m => m.Id == id && m.FamilyId == familyDbId.Value);
            if (member != null)
            {
                _context.Members.Remove(member);
                _context.SaveChanges();
                TempData["Success"] = $"Member '{member.MemberName}' delete ho gaya.";
            }

            return RedirectToAction("Index");
        }
    }
}
