using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Security.Cryptography;
using System.Text;
using BCrypt.Net;

namespace FinanceManagementNet.Controllers
{
    public class AccountController : Controller
    {
        private readonly AppDbContext _context;
        private readonly ILogger<AccountController> _logger;

        public AccountController(AppDbContext context, ILogger<AccountController> logger)
        {
            _context = context;
            _logger = logger;
        }

        [HttpGet]
        public IActionResult Login()
        {
            if (HttpContext.Session.GetInt32("FamilyDbId") != null)
            {
                return RedirectToAction("Dashboard", "Home");
            }
            return View();
        }

        [HttpPost]
        public IActionResult Login(string familyId, string password)
        {
            if (string.IsNullOrEmpty(familyId) || string.IsNullOrEmpty(password))
            {
                TempData["Error"] = "Please fill all fields.";
                return View();
            }

            try
            {
                var family = _context.Families.FirstOrDefault(f => f.FamilyId == familyId);

                if (family != null)
                {
                    if (VerifyPassword(password, family.Password))
                    {
                        HttpContext.Session.SetInt32("FamilyDbId", family.Id);
                        HttpContext.Session.SetString("FamilyId", family.FamilyId);
                        HttpContext.Session.SetString("FamilyName", family.FamilyName);
                        
                        // Set login type as Admin
                        HttpContext.Session.SetString("LoginType", "Admin");
                        
                        return RedirectToAction("Dashboard", "Home");
                    }
                    else
                    {
                        TempData["Error"] = "Invalid password.";
                    }
                }
                else
                {
                    TempData["Error"] = "Family ID not found.";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred during login for FamilyId: {FamilyId}", familyId);
                TempData["Error"] = "System error: " + ex.Message;
            }

            return View();
        }

        public IActionResult Logout()
        {
            HttpContext.Session.Clear();
            return RedirectToAction("Login");
        }

        [HttpGet]
        public IActionResult Register()
        {
            return View();
        }

        [HttpPost]
        public IActionResult Register(string familyId, string familyName, string password, string confirmPassword)
        {
            if (string.IsNullOrEmpty(familyId) || string.IsNullOrEmpty(familyName) || 
                string.IsNullOrEmpty(password) || string.IsNullOrEmpty(confirmPassword))
            {
                TempData["Error"] = "Please fill all fields.";
                return View();
            }

            if (password != confirmPassword)
            {
                TempData["Error"] = "Passwords do not match.";
                return View();
            }

            if (password.Length < 6)
            {
                TempData["Error"] = "Password must be at least 6 characters long.";
                return View();
            }

            try
            {
                var existingFamily = _context.Families.FirstOrDefault(f => f.FamilyId == familyId);
                if (existingFamily != null)
                {
                    TempData["Error"] = "Family ID already exists. Please choose another.";
                    return View();
                }

                var hashedPassword = BCrypt.Net.BCrypt.HashPassword(password);

                var newFamily = new Family
                {
                    FamilyId = familyId,
                    FamilyName = familyName,
                    Password = hashedPassword,
                    CreatedAt = DateTime.UtcNow
                };

                _context.Families.Add(newFamily);
                _context.SaveChanges();

                TempData["Success"] = "Registration successful! Please login with your credentials.";
                return RedirectToAction("Login");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred during registration for FamilyId: {FamilyId}", familyId);
                TempData["Error"] = "System error: " + ex.Message;
                return View();
            }
        }

        [HttpGet]
        public IActionResult ForgotPassword()
        {
            return View();
        }

        [HttpPost]
        public IActionResult ForgotPassword(string familyId)
        {
            if (string.IsNullOrEmpty(familyId))
            {
                TempData["Error"] = "Please enter your Family ID.";
                return View();
            }

            try
            {
                var family = _context.Families.FirstOrDefault(f => f.FamilyId == familyId);
                if (family == null)
                {
                    TempData["Error"] = "Family ID not found.";
                    return View();
                }

                // Store family ID in session for reset password page
                HttpContext.Session.SetString("ResetFamilyId", familyId);
                TempData["Success"] = "Family ID found. You can now reset your password.";
                return RedirectToAction("ResetPassword");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred during forgot password for FamilyId: {FamilyId}", familyId);
                TempData["Error"] = "System error: " + ex.Message;
                return View();
            }
        }

        [HttpGet]
        public IActionResult ResetPassword()
        {
            var familyId = HttpContext.Session.GetString("ResetFamilyId");
            if (string.IsNullOrEmpty(familyId))
            {
                return RedirectToAction("ForgotPassword");
            }
            return View();
        }

        [HttpPost]
        public IActionResult ResetPassword(string newPassword, string confirmPassword)
        {
            var familyId = HttpContext.Session.GetString("ResetFamilyId");
            if (string.IsNullOrEmpty(familyId))
            {
                TempData["Error"] = "Session expired. Please start over.";
                return RedirectToAction("ForgotPassword");
            }

            if (string.IsNullOrEmpty(newPassword) || string.IsNullOrEmpty(confirmPassword))
            {
                TempData["Error"] = "Please fill all fields.";
                return View();
            }

            if (newPassword != confirmPassword)
            {
                TempData["Error"] = "Passwords do not match.";
                return View();
            }

            if (newPassword.Length < 6)
            {
                TempData["Error"] = "Password must be at least 6 characters long.";
                return View();
            }

            try
            {
                var family = _context.Families.FirstOrDefault(f => f.FamilyId == familyId);
                if (family == null)
                {
                    TempData["Error"] = "Family not found.";
                    return RedirectToAction("ForgotPassword");
                }

                var hashedPassword = BCrypt.Net.BCrypt.HashPassword(newPassword);
                family.Password = hashedPassword;
                _context.SaveChanges();

                HttpContext.Session.Remove("ResetFamilyId");
                TempData["Success"] = "Password reset successful! Please login with your new password.";
                return RedirectToAction("Login");
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred during password reset for FamilyId: {FamilyId}", familyId);
                TempData["Error"] = "System error: " + ex.Message;
                return View();
            }
        }

        private bool VerifyPassword(string password, string hashedPassword)
        {
            if (string.IsNullOrEmpty(hashedPassword)) return false;

            try
            {
                return BCrypt.Net.BCrypt.Verify(password, hashedPassword);
            }
            catch
            {
                // Fallback for plain-text password comparison if unhashed in DB
                return password == hashedPassword;
            }
        }

        [HttpGet]
        public IActionResult MemberLogin()
        {
            return View();
        }

        [HttpPost]
        public IActionResult MemberLogin(string familyId, string memberName, string password)
        {
            if (string.IsNullOrEmpty(familyId) || string.IsNullOrEmpty(memberName) || string.IsNullOrEmpty(password))
            {
                TempData["Error"] = "Please fill all fields.";
                return View();
            }

            try
            {
                // Find family first
                var memberFamily = _context.Families.FirstOrDefault(f => f.FamilyId == familyId);
                if (memberFamily == null)
                {
                    TempData["Error"] = "Family ID not found.";
                    return View();
                }

                // Find member in that family
                var member = _context.Members.FirstOrDefault(m => m.MemberName == memberName && m.FamilyId == memberFamily.Id);

                if (member != null)
                {
                    if (string.IsNullOrEmpty(member.Password))
                    {
                        TempData["Error"] = "This member account doesn't have a password set. Please contact family admin.";
                        return View();
                    }

                    if (VerifyPassword(password, member.Password))
                    {
                        // Set session for member login
                        HttpContext.Session.SetInt32("MemberId", member.Id);
                        HttpContext.Session.SetString("MemberName", member.MemberName);
                        HttpContext.Session.SetInt32("FamilyDbId", member.FamilyId);
                        
                        // Get family info
                        var familyInfo = _context.Families.FirstOrDefault(f => f.Id == member.FamilyId);
                        if (familyInfo != null)
                        {
                            HttpContext.Session.SetString("FamilyId", familyInfo.FamilyId);
                            HttpContext.Session.SetString("FamilyName", familyInfo.FamilyName);
                        }
                        
                        // Set login type as Member
                        HttpContext.Session.SetString("LoginType", "Member");
                        
                        return RedirectToAction("Dashboard", "Home");
                    }
                    else
                    {
                        TempData["Error"] = "Invalid password.";
                    }
                }
                else
                {
                    TempData["Error"] = "Member not found.";
                }
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error occurred during member login for MemberName: {MemberName}", memberName);
                TempData["Error"] = "System error: " + ex.Message;
            }

            return View();
        }

        [HttpGet]
        public IActionResult MemberLogout()
        {
            HttpContext.Session.Remove("MemberId");
            HttpContext.Session.Remove("MemberName");
            return RedirectToAction("Dashboard", "Home");
        }
    }
}
