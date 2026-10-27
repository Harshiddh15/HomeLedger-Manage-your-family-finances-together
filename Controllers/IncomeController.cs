using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;

namespace FinanceManagementNet.Controllers
{
    public class IncomeController : Controller
    {
        private readonly AppDbContext _context;

        public IncomeController(AppDbContext context)
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

            var incomes = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value)
                .Where(i => string.IsNullOrEmpty(search) || 
                           i.Source.Contains(search) || 
                           i.MemberName.Contains(search) ||
                           (i.Description != null && i.Description.Contains(search)))
                .OrderByDescending(i => i.Date)
                .ToList();

            return View(incomes);
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
        public IActionResult Create(Income income)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                income.FamilyId = familyDbId.Value;
                _context.Incomes.Add(income);
                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(income);
        }

        public IActionResult Edit(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.Incomes.FirstOrDefault(i => i.Id == id && i.FamilyId == familyDbId.Value);
            if (income == null)
            {
                return NotFound();
            }

            return View(income);
        }

        [HttpPost]
        public IActionResult Edit(Income income)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (ModelState.IsValid)
            {
                var existingIncome = _context.Incomes.FirstOrDefault(i => i.Id == income.Id && i.FamilyId == familyDbId.Value);
                if (existingIncome == null)
                {
                    return NotFound();
                }

                existingIncome.MemberName = income.MemberName;
                existingIncome.Amount = income.Amount;
                existingIncome.Source = income.Source;
                existingIncome.Date = income.Date;
                existingIncome.Description = income.Description;

                _context.SaveChanges();
                return RedirectToAction("Index");
            }

            return View(income);
        }

        public IActionResult Delete(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.Incomes.FirstOrDefault(i => i.Id == id && i.FamilyId == familyDbId.Value);
            if (income == null)
            {
                return NotFound();
            }

            return View(income);
        }

        [HttpPost, ActionName("Delete")]
        public IActionResult DeleteConfirmed(int id)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var income = _context.Incomes.FirstOrDefault(i => i.Id == id && i.FamilyId == familyDbId.Value);
            if (income != null)
            {
                _context.Incomes.Remove(income);
                _context.SaveChanges();
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

            var incomes = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value)
                .OrderByDescending(i => i.Date)
                .ToList();

            var csv = "Date,Member Name,Source,Amount,Description\n";
            foreach (var income in incomes)
            {
                csv += $"{income.Date:yyyy-MM-dd},{income.MemberName},{income.Source},{income.Amount},{income.Description}\n";
            }

            var bytes = System.Text.Encoding.UTF8.GetBytes(csv);
            return File(bytes, "text/csv", "incomes.csv");
        }

        public IActionResult ExportToPdf()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var incomes = _context.Incomes
                .Where(i => i.FamilyId == familyDbId.Value)
                .OrderByDescending(i => i.Date)
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
                                column.Item().Text("Income Report").Bold().FontSize(20).FontColor(Colors.Green.Medium);
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
                                header.Cell().Element(CellStyle).Text("Source").Bold();
                                header.Cell().Element(CellStyle).Text("Amount").Bold();
                                header.Cell().Element(CellStyle).Text("Description").Bold();
                            });

                            foreach (var income in incomes)
                            {
                                table.Cell().Element(CellStyle).Text(income.Date.ToString("dd MMM yyyy"));
                                table.Cell().Element(CellStyle).Text(income.MemberName);
                                table.Cell().Element(CellStyle).Text(income.Source);
                                table.Cell().Element(CellStyle).Text($"₹{income.Amount:N2}").FontColor(Colors.Green.Medium);
                                table.Cell().Element(CellStyle).Text(income.Description ?? "-");
                            }
                        });
                    });

                    page.Footer().AlignRight().Text(x =>
                    {
                        x.Span("Page ");
                        x.CurrentPageNumber();
                    });
                });
            });

            var pdfBytes = document.GeneratePdf();
            return File(pdfBytes, "application/pdf", "incomes.pdf");
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
