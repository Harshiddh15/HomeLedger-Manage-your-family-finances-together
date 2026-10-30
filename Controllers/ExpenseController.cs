using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;

namespace FinanceManagementNet.Controllers
{
    public class ExpenseController : Controller
    {
        private readonly AppDbContext _context;

        public ExpenseController(AppDbContext context)
        {
            _context = context;
        }

        public IActionResult Index(string search = "")
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            var memberName = HttpContext.Session.GetString("MemberName");

            var query = _context.Expenses.Where(e => e.FamilyId == familyDbId.Value);

            // Members only see their own expenses
            if (loginType == "Member")
            {
                query = query.Where(e => e.MemberName == memberName);
            }

            if (!string.IsNullOrEmpty(search))
            {
                query = query.Where(e => e.Category.Contains(search) || 
                                       (e.MemberName != null && e.MemberName.Contains(search)) ||
                                       (e.Description != null && e.Description.Contains(search)));
            }

            var expenses = query.OrderByDescending(e => e.Date).ToList();

            ViewBag.IsMember = (loginType == "Member");
            ViewBag.MemberName = memberName;
            return View(expenses);
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

            var expense = new Expense
            {
                Date = DateTime.Today,
                MemberName = (loginType == "Member" ? memberName : "")
            };

            ViewBag.IsMember = (loginType == "Member");
            ViewBag.MemberName = memberName;
            return View(expense);
        }

        [HttpPost]
        public IActionResult Create(Expense expense)
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
                expense.MemberName = memberName ?? "Member";
            }

            if (ModelState.IsValid)
            {
                expense.FamilyId = familyDbId.Value;
                _context.Expenses.Add(expense);
                _context.SaveChanges();

                TempData["Success"] = "Expense successfully recorded!";

                // Members stay strictly inside Member Dashboard
                if (loginType == "Member")
                {
                    return RedirectToAction("MemberDashboard", "Home");
                }

                return RedirectToAction("Index");
            }

            ViewBag.IsMember = (loginType == "Member");
            ViewBag.MemberName = memberName;
            return View(expense);
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
                TempData["Error"] = "Admin function is locked. Members cannot edit expense records.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var expense = _context.Expenses.FirstOrDefault(e => e.Id == id && e.FamilyId == familyDbId.Value);
            if (expense == null)
            {
                return NotFound();
            }

            return View(expense);
        }

        [HttpPost]
        public IActionResult Edit(Expense expense)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot edit expense records.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            if (ModelState.IsValid)
            {
                var existingExpense = _context.Expenses.FirstOrDefault(e => e.Id == expense.Id && e.FamilyId == familyDbId.Value);
                if (existingExpense == null)
                {
                    return NotFound();
                }

                existingExpense.MemberName = expense.MemberName;
                existingExpense.Category = expense.Category;
                existingExpense.Amount = expense.Amount;
                existingExpense.Date = expense.Date;
                existingExpense.Description = expense.Description;

                _context.SaveChanges();
                TempData["Success"] = "Expense record updated successfully.";
                return RedirectToAction("Index");
            }

            return View(expense);
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
                TempData["Error"] = "Admin function is locked. Members cannot delete expense records.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var expense = _context.Expenses.FirstOrDefault(e => e.Id == id && e.FamilyId == familyDbId.Value);
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

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Members cannot delete expense records.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var expense = _context.Expenses.FirstOrDefault(e => e.Id == id && e.FamilyId == familyDbId.Value);
            if (expense != null)
            {
                _context.Expenses.Remove(expense);
                _context.SaveChanges();
                TempData["Success"] = "Expense record deleted successfully.";
            }

            return RedirectToAction("Index");
        }

        public IActionResult ExportToCsv()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Only Admin can export family expense reports.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var expenses = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value)
                .OrderByDescending(e => e.Date)
                .ToList();

            var csv = "Date,Member Name,Category,Amount,Description\n";
            foreach (var expense in expenses)
            {
                csv += $"{expense.Date:yyyy-MM-dd},{expense.MemberName},{expense.Category},{expense.Amount},{expense.Description}\n";
            }

            var bytes = System.Text.Encoding.UTF8.GetBytes(csv);
            return File(bytes, "text/csv", "expenses.csv");
        }

        public IActionResult ExportToPdf()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var loginType = HttpContext.Session.GetString("LoginType");
            if (loginType != "Admin")
            {
                TempData["Error"] = "Admin function is locked. Only Admin can export family expense reports.";
                return RedirectToAction("MemberDashboard", "Home");
            }

            var expenses = _context.Expenses
                .Where(e => e.FamilyId == familyDbId.Value)
                .OrderByDescending(e => e.Date)
                .ToList();

            var document = Document.Create(container =>
            {
                container.Page(page =>
                {
                    page.Size(PageSizes.A4);
                    page.Margin(2, Unit.Centimetre);
                    page.PageColor(Colors.White);
                    page.DefaultTextStyle(x => x.FontSize(10));

                    page.Header().Element(container =>
                    {
                        container.Row(row =>
                        {
                            row.RelativeItem().Column(column =>
                            {
                                column.Item().Text("Expense Report").Bold().FontSize(20).FontColor(Colors.Blue.Medium);
                                column.Item().Text($"Generated on: {DateTime.Now:dd MMM yyyy}").FontSize(8);
                            });
                        });
                    });

                    page.Content().Element(container =>
                    {
                        container.Table(table =>
                        {
                            table.ColumnsDefinition(columns =>
                            {
                                columns.ConstantColumn(100);
                                columns.ConstantColumn(120);
                                columns.ConstantColumn(100);
                                columns.ConstantColumn(80);
                                columns.RelativeColumn();
                            });

                            table.Header(header =>
                            {
                                header.Cell().Element(CellStyle).Text("Date").Bold();
                                header.Cell().Element(CellStyle).Text("Member").Bold();
                                header.Cell().Element(CellStyle).Text("Category").Bold();
                                header.Cell().Element(CellStyle).Text("Amount").Bold();
                                header.Cell().Element(CellStyle).Text("Description").Bold();
                            });

                            foreach (var expense in expenses)
                            {
                                table.Cell().Element(CellStyle).Text(expense.Date.ToString("dd MMM yyyy"));
                                table.Cell().Element(CellStyle).Text(expense.MemberName);
                                table.Cell().Element(CellStyle).Text(expense.Category);
                                table.Cell().Element(CellStyle).Text($"₹{expense.Amount:N2}").FontColor(Colors.Red.Medium);
                                table.Cell().Element(CellStyle).Text(expense.Description ?? "-");
                            }
                        });
                    });

                    page.Footer().AlignCenter().Text(x =>
                    {
                        x.Span("Page ");
                        x.CurrentPageNumber();
                    });
                });
            });

            var pdfBytes = document.GeneratePdf();
            return File(pdfBytes, "application/pdf", "expenses.pdf");
        }

        static IContainer CellStyle(IContainer container)
        {
            return container
                .Border(1)
                .BorderColor(Colors.Grey.Lighten2)
                .Padding(5)
                .AlignCenter()
                .AlignMiddle();
        }
    }
}
