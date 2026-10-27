using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;

namespace FinanceManagementNet.Controllers
{
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

            return View();
        }

        [HttpPost]
        public IActionResult Create(Member member)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                member.FamilyId = familyDbId.Value;
                _context.Members.Add(member);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(member);
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

            if (ModelState.IsValid)
            {
                var existingMember = _context.Members.FirstOrDefault(m => m.Id == member.Id && m.FamilyId == familyDbId.Value);
                if (existingMember == null)
                {
                    return NotFound();
                }

                existingMember.MemberName = member.MemberName;
                existingMember.Relation = member.Relation;
                existingMember.Mobile = member.Mobile;
                existingMember.ProfileImage = member.ProfileImage;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(member);
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
            }

            return RedirectToAction("Index");
        }
    }
}
