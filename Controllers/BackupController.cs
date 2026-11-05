using ClosedXML.Excel;
using FinanceManagementNet.Data;
using FinanceManagementNet.Filters;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using QuestPDF.Fluent;
using QuestPDF.Helpers;
using QuestPDF.Infrastructure;
using System.Globalization;
using System.Text;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Controllers
{
    [AdminOnly]
    public class BackupController : Controller
    {
        private readonly AppDbContext _context;

        public BackupController(AppDbContext context)
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

            ViewBag.MemberCount = _context.Members.Count(m => m.FamilyId == familyDbId.Value);
            ViewBag.IncomeCount = _context.Incomes.Count(i => i.FamilyId == familyDbId.Value);
            ViewBag.ExpenseCount = _context.Expenses.Count(e => e.FamilyId == familyDbId.Value);
            ViewBag.UdharCount = _context.Udhar.Count(u => u.FamilyId == familyDbId.Value);
            ViewBag.GoalCount = _context.SavingsGoals.Count(s => s.FamilyId == familyDbId.Value);
            ViewBag.CategoryCount = _context.Categories.Count(c => c.FamilyId == familyDbId.Value);

            return View();
        }

        #region 1. EXPORT METHODS (Excel, CSV, PDF, JSON)

        // EXCEL EXPORT (.xlsx)
        public IActionResult ExportExcel()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null) return RedirectToAction("Login", "Account");

            var data = FetchFamilyData(familyDbId.Value);
            using var workbook = new XLWorkbook();

            // 1. Summary Sheet
            var wsSummary = workbook.Worksheets.Add("Overview");
            wsSummary.Cell(1, 1).Value = "HomeLedger - Family Finance Master Report";
            wsSummary.Cell(1, 1).Style.Font.Bold = true;
            wsSummary.Cell(1, 1).Style.Font.FontSize = 16;
            wsSummary.Cell(1, 1).Style.Font.FontColor = XLColor.FromHtml("#10b981");

            wsSummary.Cell(3, 1).Value = "Family Name";
            wsSummary.Cell(3, 2).Value = data.Family?.FamilyName ?? "Family Portal";
            wsSummary.Cell(4, 1).Value = "Family Head";
            wsSummary.Cell(4, 2).Value = data.Members.FirstOrDefault(m => m.Relation == "Self" || m.Relation == "Head")?.MemberName ?? data.Members.FirstOrDefault()?.MemberName ?? data.Family?.FamilyName ?? "Family Head";
            wsSummary.Cell(5, 1).Value = "Export Date";
            wsSummary.Cell(5, 2).Value = DateTime.Now.ToString("dd MMMM yyyy, hh:mm tt");

            var totalIncome = data.Incomes.Sum(i => i.Amount);
            var totalExpense = data.Expenses.Sum(e => e.Amount);
            var balance = totalIncome - totalExpense;
            var udharLene = data.Udhar.Where(u => u.Type == "Lene Hai" && u.Status == "Pending").Sum(u => u.RemainingAmount);
            var udharDene = data.Udhar.Where(u => u.Type == "Dene Hai" && u.Status == "Pending").Sum(u => u.RemainingAmount);
            var totalSavings = data.SavingsGoals.Sum(s => s.CurrentAmount);

            wsSummary.Cell(7, 1).Value = "FINANCIAL KEY METRICS";
            wsSummary.Cell(7, 1).Style.Font.Bold = true;
            wsSummary.Cell(8, 1).Value = "Total Income"; wsSummary.Cell(8, 2).Value = totalIncome;
            wsSummary.Cell(9, 1).Value = "Total Expenses"; wsSummary.Cell(9, 2).Value = totalExpense;
            wsSummary.Cell(10, 1).Value = "Net Balance"; wsSummary.Cell(10, 2).Value = balance;
            wsSummary.Cell(11, 1).Value = "Udhar To Receive (Lene Hai)"; wsSummary.Cell(11, 2).Value = udharLene;
            wsSummary.Cell(12, 1).Value = "Udhar To Pay (Dene Hai)"; wsSummary.Cell(12, 2).Value = udharDene;
            wsSummary.Cell(13, 1).Value = "Accumulated Savings"; wsSummary.Cell(13, 2).Value = totalSavings;

            wsSummary.Range(7, 1, 13, 2).Style.Border.OutsideBorder = XLBorderStyleValues.Thin;
            wsSummary.Columns().AdjustToContents();

            // 2. Members Sheet
            var wsMembers = workbook.Worksheets.Add("Members");
            AddHeaders(wsMembers, new[] { "Member Name", "Relation", "Mobile Number" });
            int row = 2;
            foreach (var m in data.Members)
            {
                wsMembers.Cell(row, 1).Value = m.MemberName;
                wsMembers.Cell(row, 2).Value = m.Relation;
                wsMembers.Cell(row, 3).Value = m.Mobile ?? "-";
                row++;
            }
            wsMembers.Columns().AdjustToContents();

            // 3. Incomes Sheet
            var wsIncomes = workbook.Worksheets.Add("Incomes");
            AddHeaders(wsIncomes, new[] { "Date", "Family Member", "Source / Client", "Amount (INR)", "Description" });
            row = 2;
            foreach (var inc in data.Incomes)
            {
                wsIncomes.Cell(row, 1).Value = inc.Date.ToString("yyyy-MM-dd");
                wsIncomes.Cell(row, 2).Value = inc.MemberName;
                wsIncomes.Cell(row, 3).Value = inc.Source;
                wsIncomes.Cell(row, 4).Value = inc.Amount;
                wsIncomes.Cell(row, 5).Value = inc.Description ?? "";
                row++;
            }
            wsIncomes.Columns().AdjustToContents();

            // 4. Expenses Sheet
            var wsExpenses = workbook.Worksheets.Add("Expenses");
            AddHeaders(wsExpenses, new[] { "Date", "Family Member", "Category", "Amount (INR)", "Description" });
            row = 2;
            foreach (var exp in data.Expenses)
            {
                wsExpenses.Cell(row, 1).Value = exp.Date.ToString("yyyy-MM-dd");
                wsExpenses.Cell(row, 2).Value = exp.MemberName;
                wsExpenses.Cell(row, 3).Value = exp.Category;
                wsExpenses.Cell(row, 4).Value = exp.Amount;
                wsExpenses.Cell(row, 5).Value = exp.Description ?? "";
                row++;
            }
            wsExpenses.Columns().AdjustToContents();

            // 5. Udhar Ledger Sheet
            var wsUdhar = workbook.Worksheets.Add("Udhar");
            AddHeaders(wsUdhar, new[] { "Date", "Person / Store", "Member Involved", "Classification", "Total Amount", "Paid Amount", "Remaining Baaki", "Status", "Reason / Notes" });
            row = 2;
            foreach (var u in data.Udhar)
            {
                wsUdhar.Cell(row, 1).Value = u.Date.ToString("yyyy-MM-dd");
                wsUdhar.Cell(row, 2).Value = u.PersonName;
                wsUdhar.Cell(row, 3).Value = u.MemberName ?? "";
                wsUdhar.Cell(row, 4).Value = u.Type;
                wsUdhar.Cell(row, 5).Value = u.Amount;
                wsUdhar.Cell(row, 6).Value = u.PaidAmount;
                wsUdhar.Cell(row, 7).Value = u.RemainingAmount;
                wsUdhar.Cell(row, 8).Value = u.Status;
                wsUdhar.Cell(row, 9).Value = u.Reason ?? "";
                row++;
            }
            wsUdhar.Columns().AdjustToContents();

            // 6. Savings Goals Sheet
            var wsSavings = workbook.Worksheets.Add("SavingsGoals");
            AddHeaders(wsSavings, new[] { "Goal Name", "Target Amount", "Current Amount", "Target Date", "Description" });
            row = 2;
            foreach (var sg in data.SavingsGoals)
            {
                wsSavings.Cell(row, 1).Value = sg.GoalName;
                wsSavings.Cell(row, 2).Value = sg.TargetAmount;
                wsSavings.Cell(row, 3).Value = sg.CurrentAmount;
                wsSavings.Cell(row, 4).Value = sg.TargetDate.ToString("yyyy-MM-dd");
                wsSavings.Cell(row, 5).Value = sg.Description ?? "";
                row++;
            }
            wsSavings.Columns().AdjustToContents();

            // 7. Categories Sheet
            var wsCategories = workbook.Worksheets.Add("Categories");
            AddHeaders(wsCategories, new[] { "Category Name", "Classification Type", "Icon" });
            row = 2;
            foreach (var c in data.Categories)
            {
                wsCategories.Cell(row, 1).Value = c.Name;
                wsCategories.Cell(row, 2).Value = c.Type;
                wsCategories.Cell(row, 3).Value = c.Icon ?? "";
                row++;
            }
            wsCategories.Columns().AdjustToContents();

            // 8. Budgets Sheet
            var wsBudgets = workbook.Worksheets.Add("Budgets");
            AddHeaders(wsBudgets, new[] { "Category", "Month (YYYY-MM)", "Monthly Budget Amount" });
            row = 2;
            foreach (var b in data.Budgets)
            {
                wsBudgets.Cell(row, 1).Value = b.Category;
                wsBudgets.Cell(row, 2).Value = b.Month;
                wsBudgets.Cell(row, 3).Value = b.Amount;
                row++;
            }
            wsBudgets.Columns().AdjustToContents();

            // 9. Reminders Sheet
            var wsReminders = workbook.Worksheets.Add("Reminders");
            AddHeaders(wsReminders, new[] { "Reminder Date", "Title", "Notes" });
            row = 2;
            foreach (var r in data.Reminders)
            {
                wsReminders.Cell(row, 1).Value = r.Date.ToString("yyyy-MM-dd");
                wsReminders.Cell(row, 2).Value = r.Title;
                wsReminders.Cell(row, 3).Value = r.Description ?? "";
                row++;
            }
            wsReminders.Columns().AdjustToContents();

            using var stream = new MemoryStream();
            workbook.SaveAs(stream);
            var content = stream.ToArray();
            var fileName = $"Family_Finance_Backup_{DateTime.Now:yyyyMMdd_HHmmss}.xlsx";
            return File(content, "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", fileName);
        }

        // CSV EXPORT (.csv) - Master Universal File
        public IActionResult ExportCsv()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null) return RedirectToAction("Login", "Account");

            var data = FetchFamilyData(familyDbId.Value);
            var sb = new StringBuilder();

            // CSV Header
            sb.AppendLine("RecordType,Date,Name,MemberName,CategoryOrSource,TypeOrRelation,Amount,SecondaryAmount,RemainingAmount,StatusOrActive,TargetDate,DescriptionOrReason");

            // Members
            foreach (var m in data.Members)
            {
                sb.AppendLine($"MEMBER,\"\",{Escape(m.MemberName)},{Escape(m.MemberName)},\"\",{Escape(m.Relation)},0,0,0,\"\",\"\",{Escape(m.Mobile)}");
            }

            // Incomes
            foreach (var inc in data.Incomes)
            {
                sb.AppendLine($"INCOME,{inc.Date:yyyy-MM-dd},{Escape(inc.Source)},{Escape(inc.MemberName)},{Escape(inc.Source)},\"\",{inc.Amount.ToString("F2", CultureInfo.InvariantCulture)},0,0,\"\",\"\",{Escape(inc.Description)}");
            }

            // Expenses
            foreach (var exp in data.Expenses)
            {
                sb.AppendLine($"EXPENSE,{exp.Date:yyyy-MM-dd},{Escape(exp.Category)},{Escape(exp.MemberName)},{Escape(exp.Category)},\"\",{exp.Amount.ToString("F2", CultureInfo.InvariantCulture)},0,0,\"\",\"\",{Escape(exp.Description)}");
            }

            // Udhar
            foreach (var u in data.Udhar)
            {
                sb.AppendLine($"UDHAR,{u.Date:yyyy-MM-dd},{Escape(u.PersonName)},{Escape(u.MemberName)},\"\",{Escape(u.Type)},{u.Amount.ToString("F2", CultureInfo.InvariantCulture)},{u.PaidAmount.ToString("F2", CultureInfo.InvariantCulture)},{u.RemainingAmount.ToString("F2", CultureInfo.InvariantCulture)},{Escape(u.Status)},\"\",{Escape(u.Reason)}");
            }

            // Savings Goals
            foreach (var sg in data.SavingsGoals)
            {
                sb.AppendLine($"SAVINGS_GOAL,\"\",{Escape(sg.GoalName)},\"\",\"\",\"\",{sg.TargetAmount.ToString("F2", CultureInfo.InvariantCulture)},{sg.CurrentAmount.ToString("F2", CultureInfo.InvariantCulture)},0,\"\",{sg.TargetDate:yyyy-MM-dd},{Escape(sg.Description)}");
            }

            // Categories
            foreach (var c in data.Categories)
            {
                sb.AppendLine($"CATEGORY,\"\",{Escape(c.Name)},\"\",\"\",{Escape(c.Type)},0,0,0,\"\",\"\",{Escape(c.Icon)}");
            }

            // Budgets
            foreach (var b in data.Budgets)
            {
                sb.AppendLine($"BUDGET,\"\",{Escape(b.Category)},\"\",{Escape(b.Month)},\"\",{b.Amount.ToString("F2", CultureInfo.InvariantCulture)},0,0,\"\",\"\", \"\"");
            }

            // Reminders
            foreach (var r in data.Reminders)
            {
                sb.AppendLine($"REMINDER,{r.Date:yyyy-MM-dd},{Escape(r.Title)},\"\",\"\",\"\",0,0,0,\"\",\"\",{Escape(r.Description)}");
            }

            var bytes = Encoding.UTF8.GetPreamble().Concat(Encoding.UTF8.GetBytes(sb.ToString())).ToArray();
            var fileName = $"Family_Finance_Backup_{DateTime.Now:yyyyMMdd_HHmmss}.csv";
            return File(bytes, "text/csv; charset=utf-8", fileName);
        }

        // PDF EXPORT (.pdf) - Executive Printable Document + Lossless Re-Import Payload
        public IActionResult ExportPdf()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null) return RedirectToAction("Login", "Account");

            var data = FetchFamilyData(familyDbId.Value);

            var totalIncome = data.Incomes.Sum(i => i.Amount);
            var totalExpense = data.Expenses.Sum(e => e.Amount);
            var netBalance = totalIncome - totalExpense;
            var udharLene = data.Udhar.Where(u => u.Type == "Lene Hai" && u.Status == "Pending").Sum(u => u.RemainingAmount);
            var udharDene = data.Udhar.Where(u => u.Type == "Dene Hai" && u.Status == "Pending").Sum(u => u.RemainingAmount);
            var totalSavings = data.SavingsGoals.Sum(s => s.CurrentAmount);

            var document = Document.Create(container =>
            {
                container.Page(page =>
                {
                    page.Size(PageSizes.A4.Landscape());
                    page.Margin(20);
                    page.PageColor(Colors.White);
                    page.DefaultTextStyle(x => x.FontSize(9).FontFamily("Segoe UI", "Arial"));

                    // Header
                    page.Header().Column(col =>
                    {
                        col.Item().Row(row =>
                        {
                            row.RelativeItem().Column(titleCol =>
                            {
                                titleCol.Item().Text("HOMELEDGER - OFFICIAL FINANCIAL DOSSIER").FontSize(16).Bold().FontColor("#0f172a");
                                var headName = data.Members.FirstOrDefault(m => m.Relation == "Self" || m.Relation == "Head")?.MemberName ?? data.Members.FirstOrDefault()?.MemberName ?? data.Family?.FamilyName ?? "Family Head";
                                titleCol.Item().Text($"Family: {data.Family?.FamilyName ?? "Family Portal"} | Head: {headName}").FontSize(10).FontColor("#475569");
                            });

                            row.ConstantItem(220).AlignRight().Column(metaCol =>
                            {
                                metaCol.Item().Text($"Export Date: {DateTime.Now:dd MMM yyyy, hh:mm tt}").FontSize(8.5f).FontColor("#64748b");
                                metaCol.Item().Text("VERIFIED COMPLETE SYSTEM BACKUP").FontSize(8.5f).Bold().FontColor("#10b981");
                            });
                        });

                        col.Item().PaddingVertical(8).LineHorizontal(1).LineColor("#cbd5e1");

                        // KPI Cards Ribbon
                        col.Item().Row(r =>
                        {
                            r.RelativeItem().Border(1).BorderColor("#e2e8f0").Padding(6).Column(c =>
                            {
                                c.Item().Text("TOTAL INCOME").FontSize(7.5f).Bold().FontColor("#64748b");
                                c.Item().Text($"₹{totalIncome:N2}").FontSize(11).Bold().FontColor("#10b981");
                            });
                            r.RelativeItem().Border(1).BorderColor("#e2e8f0").Padding(6).Column(c =>
                            {
                                c.Item().Text("TOTAL EXPENSES").FontSize(7.5f).Bold().FontColor("#64748b");
                                c.Item().Text($"₹{totalExpense:N2}").FontSize(11).Bold().FontColor("#f43f5e");
                            });
                            r.RelativeItem().Border(1).BorderColor("#e2e8f0").Padding(6).Column(c =>
                            {
                                c.Item().Text("NET BALANCE").FontSize(7.5f).Bold().FontColor("#64748b");
                                c.Item().Text($"₹{netBalance:N2}").FontSize(11).Bold().FontColor("#0ea5e9");
                            });
                            r.RelativeItem().Border(1).BorderColor("#e2e8f0").Padding(6).Column(c =>
                            {
                                c.Item().Text("UDHAR TO RECEIVE").FontSize(7.5f).Bold().FontColor("#64748b");
                                c.Item().Text($"₹{udharLene:N2}").FontSize(11).Bold().FontColor("#0284c7");
                            });
                            r.RelativeItem().Border(1).BorderColor("#e2e8f0").Padding(6).Column(c =>
                            {
                                c.Item().Text("UDHAR TO PAY").FontSize(7.5f).Bold().FontColor("#64748b");
                                c.Item().Text($"₹{udharDene:N2}").FontSize(11).Bold().FontColor("#d97706");
                            });
                            r.RelativeItem().Border(1).BorderColor("#e2e8f0").Padding(6).Column(c =>
                            {
                                c.Item().Text("TOTAL SAVINGS").FontSize(7.5f).Bold().FontColor("#64748b");
                                c.Item().Text($"₹{totalSavings:N2}").FontSize(11).Bold().FontColor("#6366f1");
                            });
                        });

                        col.Item().PaddingBottom(10);
                    });

                    // Body
                    page.Content().Column(col =>
                    {
                        // 1. Members
                        col.Item().Text("1. REGISTERED FAMILY MEMBERS").FontSize(10).Bold().FontColor("#1e293b");
                        col.Item().Table(t =>
                        {
                            t.ColumnsDefinition(c =>
                            {
                                c.RelativeColumn(2);
                                c.RelativeColumn(2);
                                c.RelativeColumn(3);
                            });
                            t.Header(h =>
                            {
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Member Name").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Relation").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Mobile Number").Bold();
                            });
                            foreach (var m in data.Members)
                            {
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(m.MemberName);
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(m.Relation);
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(m.Mobile ?? "-");
                            }
                        });

                        col.Item().PaddingVertical(10);

                        // 2. Udhar Ledger
                        col.Item().Text("2. BILATERAL UDHAR & CREDIT LEDGER").FontSize(10).Bold().FontColor("#1e293b");
                        col.Item().Table(t =>
                        {
                            t.ColumnsDefinition(c =>
                            {
                                c.ConstantColumn(65);
                                c.RelativeColumn(2);
                                c.RelativeColumn(1.5f);
                                c.RelativeColumn(1.2f);
                                c.RelativeColumn(1.2f);
                                c.RelativeColumn(1.2f);
                                c.RelativeColumn(1.2f);
                                c.RelativeColumn(1f);
                                c.RelativeColumn(3);
                            });
                            t.Header(h =>
                            {
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Date").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Person / Store").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Member").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Type").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Principal").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Repaid").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Remaining").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Status").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Reason / Notes").Bold();
                            });
                            foreach (var u in data.Udhar)
                            {
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(u.Date.ToString("dd MMM yyyy"));
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(u.PersonName).Bold();
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(u.MemberName ?? "-");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(u.Type).FontColor(u.Type == "Lene Hai" ? "#0284c7" : "#d97706");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text($"₹{u.Amount:N2}");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text($"₹{u.PaidAmount:N2}").FontColor("#10b981");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text($"₹{u.RemainingAmount:N2}").Bold();
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(u.Status).FontColor(u.Status == "Completed" ? "#10b981" : "#f43f5e");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(u.Reason ?? "-");
                            }
                        });

                        col.Item().PaddingVertical(10);

                        // 3. Savings Goals
                        col.Item().Text("3. SAVINGS GOALS PROGRESSION").FontSize(10).Bold().FontColor("#1e293b");
                        col.Item().Table(t =>
                        {
                            t.ColumnsDefinition(c =>
                            {
                                c.RelativeColumn(3);
                                c.RelativeColumn(1.5f);
                                c.RelativeColumn(1.5f);
                                c.ConstantColumn(80);
                                c.RelativeColumn(3);
                            });
                            t.Header(h =>
                            {
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Goal Title").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Target (₹)").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Saved (₹)").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Target Date").Bold();
                                h.Cell().Background("#f1f5f9").Padding(4).Text("Description").Bold();
                            });
                            foreach (var s in data.SavingsGoals)
                            {
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(s.GoalName).Bold();
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text($"₹{s.TargetAmount:N2}");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text($"₹{s.CurrentAmount:N2}").FontColor("#10b981");
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(s.TargetDate.ToString("dd MMM yyyy"));
                                t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(3).Text(s.Description ?? "-");
                            }
                        });

                        col.Item().PaddingVertical(10);

                        // 4. Incomes & Expenses Split Tables
                        col.Item().Row(r =>
                        {
                            // Incomes column
                            r.RelativeItem().Column(ic =>
                            {
                                ic.Item().Text($"4. INCOMES ({data.Incomes.Count} Records)").FontSize(10).Bold().FontColor("#10b981");
                                ic.Item().Table(t =>
                                {
                                    t.ColumnsDefinition(c =>
                                    {
                                        c.ConstantColumn(60);
                                        c.RelativeColumn(1.5f);
                                        c.RelativeColumn(1.5f);
                                        c.RelativeColumn(1.2f);
                                    });
                                    t.Header(h =>
                                    {
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Date").Bold();
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Member").Bold();
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Source").Bold();
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Amount").Bold();
                                    });
                                    foreach (var inc in data.Incomes.Take(50))
                                    {
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text(inc.Date.ToString("dd/MM/yy"));
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text(inc.MemberName);
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text(inc.Source);
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text($"₹{inc.Amount:N0}").Bold().FontColor("#10b981");
                                    }
                                });
                            });

                            r.ConstantItem(15);

                            // Expenses column
                            r.RelativeItem().Column(ec =>
                            {
                                ec.Item().Text($"5. EXPENSES ({data.Expenses.Count} Records)").FontSize(10).Bold().FontColor("#f43f5e");
                                ec.Item().Table(t =>
                                {
                                    t.ColumnsDefinition(c =>
                                    {
                                        c.ConstantColumn(60);
                                        c.RelativeColumn(1.5f);
                                        c.RelativeColumn(1.5f);
                                        c.RelativeColumn(1.2f);
                                    });
                                    t.Header(h =>
                                    {
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Date").Bold();
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Member").Bold();
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Category").Bold();
                                        h.Cell().Background("#f1f5f9").Padding(3).Text("Amount").Bold();
                                    });
                                    foreach (var exp in data.Expenses.Take(50))
                                    {
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text(exp.Date.ToString("dd/MM/yy"));
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text(exp.MemberName);
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text(exp.Category);
                                        t.Cell().BorderBottom(0.5f).BorderColor("#e2e8f0").Padding(2.5f).Text($"₹{exp.Amount:N0}").Bold().FontColor("#f43f5e");
                                    }
                                });
                            });
                        });
                    });

                    // Footer
                    page.Footer().Row(r =>
                    {
                        r.RelativeItem().Text("CONFIDENTIAL & AUDIT READY - HomeLedger Family Portal").FontSize(8).FontColor("#94a3b8");
                        r.RelativeItem().AlignRight().Text(x =>
                        {
                            x.Span("Page ");
                            x.CurrentPageNumber();
                            x.Span(" of ");
                            x.TotalPages();
                        });
                    });
                });
            });

            var pdfBytes = document.GeneratePdf();

            // CRITICAL FEATURE: Embed lossless Base64 JSON payload in trailer so this PDF can be re-imported!
            var backupJson = JsonSerializer.Serialize(data, new JsonSerializerOptions
            {
                WriteIndented = false,
                ReferenceHandler = ReferenceHandler.IgnoreCycles
            });
            var base64Json = Convert.ToBase64String(Encoding.UTF8.GetBytes(backupJson));
            var trailer = $"\n%%HOMELEDGER_DATA_START%%\n{base64Json}\n%%HOMELEDGER_DATA_END%%\n";
            var trailerBytes = Encoding.UTF8.GetBytes(trailer);

            var combinedBytes = new byte[pdfBytes.Length + trailerBytes.Length];
            Buffer.BlockCopy(pdfBytes, 0, combinedBytes, 0, pdfBytes.Length);
            Buffer.BlockCopy(trailerBytes, 0, combinedBytes, pdfBytes.Length, trailerBytes.Length);

            var fileName = $"Family_Finance_Dossier_{DateTime.Now:yyyyMMdd_HHmmss}.pdf";
            return File(combinedBytes, "application/pdf", fileName);
        }

        // JSON EXPORT (.json) - Legacy & Direct Raw
        public IActionResult ExportBackup()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null) return RedirectToAction("Login", "Account");

            var data = FetchFamilyData(familyDbId.Value);
            var json = JsonSerializer.Serialize(data, new JsonSerializerOptions
            {
                WriteIndented = true,
                ReferenceHandler = ReferenceHandler.IgnoreCycles
            });

            var bytes = Encoding.UTF8.GetBytes(json);
            var fileName = $"Family_Finance_Backup_{DateTime.Now:yyyyMMdd_HHmmss}.json";
            return File(bytes, "application/json", fileName);
        }

        #endregion

        #region 2. UNIVERSAL IMPORT METHOD (Excel, CSV, PDF, JSON)

        [HttpPost]
        public IActionResult ImportBackup(IFormFile backupFile)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null) return RedirectToAction("Login", "Account");

            if (backupFile == null || backupFile.Length == 0)
            {
                TempData["Error"] = "Kripya upload karne ke liye file select karein (.xlsx, .csv, .pdf, ya .json).";
                return RedirectToAction("Index");
            }

            var extension = Path.GetExtension(backupFile.FileName).ToLowerInvariant();

            using var transaction = _context.Database.BeginTransaction();
            try
            {
                int membersAdded = 0, incomesAdded = 0, expensesAdded = 0, udharAdded = 0, goalsAdded = 0, categoriesAdded = 0, budgetsAdded = 0;

                // 1. EXCEL IMPORT (.xlsx)
                if (extension == ".xlsx")
                {
                    using var stream = backupFile.OpenReadStream();
                    using var workbook = new XLWorkbook(stream);

                    // Import Members
                    if (workbook.TryGetWorksheet("Members", out var wsMembers))
                    {
                        var rows = wsMembers.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var name = r.Cell(1).GetString().Trim();
                            var relation = r.Cell(2).GetString().Trim();
                            var mobile = r.Cell(3).GetString().Trim();

                            if (!string.IsNullOrEmpty(name))
                            {
                                var existing = _context.Members.FirstOrDefault(m => m.FamilyId == familyDbId.Value && m.MemberName.ToLower() == name.ToLower());
                                if (existing == null)
                                {
                                    _context.Members.Add(new Member
                                    {
                                        FamilyId = familyDbId.Value,
                                        MemberName = name,
                                        Relation = string.IsNullOrEmpty(relation) ? "Member" : relation,
                                        Mobile = mobile,
                                        Password = BCrypt.Net.BCrypt.HashPassword("123456")
                                    });
                                    membersAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }

                    // Import Incomes
                    if (workbook.TryGetWorksheet("Incomes", out var wsIncomes))
                    {
                        var rows = wsIncomes.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var dateStr = r.Cell(1).GetString().Trim();
                            var member = r.Cell(2).GetString().Trim();
                            var source = r.Cell(3).GetString().Trim();
                            var amount = ParseDecimal(r.Cell(4).GetString());
                            var desc = r.Cell(5).GetString().Trim();

                            if (amount > 0 && !string.IsNullOrEmpty(source))
                            {
                                DateTime date = ParseDate(dateStr);
                                var existing = _context.Incomes.FirstOrDefault(i => i.FamilyId == familyDbId.Value && i.Date.Date == date.Date && i.Amount == amount && i.Source.ToLower() == source.ToLower() && i.MemberName.ToLower() == member.ToLower());
                                if (existing == null)
                                {
                                    _context.Incomes.Add(new Income
                                    {
                                        FamilyId = familyDbId.Value,
                                        MemberName = string.IsNullOrEmpty(member) ? "Father" : member,
                                        Source = source,
                                        Amount = amount,
                                        Date = date,
                                        Description = string.IsNullOrEmpty(desc) ? null : desc
                                    });
                                    incomesAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }

                    // Import Expenses
                    if (workbook.TryGetWorksheet("Expenses", out var wsExpenses))
                    {
                        var rows = wsExpenses.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var dateStr = r.Cell(1).GetString().Trim();
                            var member = r.Cell(2).GetString().Trim();
                            var category = r.Cell(3).GetString().Trim();
                            var amount = ParseDecimal(r.Cell(4).GetString());
                            var desc = r.Cell(5).GetString().Trim();

                            if (amount > 0 && !string.IsNullOrEmpty(category))
                            {
                                DateTime date = ParseDate(dateStr);
                                var existing = _context.Expenses.FirstOrDefault(e => e.FamilyId == familyDbId.Value && e.Date.Date == date.Date && e.Amount == amount && e.Category.ToLower() == category.ToLower() && e.MemberName.ToLower() == member.ToLower());
                                if (existing == null)
                                {
                                    _context.Expenses.Add(new Expense
                                    {
                                        FamilyId = familyDbId.Value,
                                        MemberName = string.IsNullOrEmpty(member) ? "Father" : member,
                                        Category = category,
                                        Amount = amount,
                                        Date = date,
                                        Description = string.IsNullOrEmpty(desc) ? null : desc
                                    });
                                    expensesAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }

                    // Import Udhar
                    if (workbook.TryGetWorksheet("Udhar", out var wsUdhar))
                    {
                        var rows = wsUdhar.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var dateStr = r.Cell(1).GetString().Trim();
                            var person = r.Cell(2).GetString().Trim();
                            var member = r.Cell(3).GetString().Trim();
                            var type = r.Cell(4).GetString().Trim();
                            var totalAmount = ParseDecimal(r.Cell(5).GetString());
                            var paidAmount = ParseDecimal(r.Cell(6).GetString());
                            var status = r.Cell(8).GetString().Trim();
                            var reason = r.Cell(9).GetString().Trim();

                            if (totalAmount > 0 && !string.IsNullOrEmpty(person))
                            {
                                DateTime date = ParseDate(dateStr);
                                if (string.IsNullOrEmpty(type)) type = "Dene Hai";
                                var remaining = Math.Max(0, totalAmount - paidAmount);
                                if (string.IsNullOrEmpty(status)) status = remaining <= 0 ? "Completed" : "Pending";

                                var existing = _context.Udhar.FirstOrDefault(u => u.FamilyId == familyDbId.Value && u.PersonName.ToLower() == person.ToLower() && u.Type == type && u.Amount == totalAmount && u.Date.Date == date.Date);
                                if (existing == null)
                                {
                                    _context.Udhar.Add(new Udhar
                                    {
                                        FamilyId = familyDbId.Value,
                                        PersonName = person,
                                        MemberName = string.IsNullOrEmpty(member) ? "Father" : member,
                                        Type = type,
                                        Amount = totalAmount,
                                        PaidAmount = paidAmount,
                                        RemainingAmount = remaining,
                                        Status = status,
                                        Reason = string.IsNullOrEmpty(reason) ? null : reason,
                                        Date = date
                                    });
                                    udharAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }

                    // Import Savings Goals
                    if (workbook.TryGetWorksheet("SavingsGoals", out var wsSavings))
                    {
                        var rows = wsSavings.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var goalName = r.Cell(1).GetString().Trim();
                            var target = ParseDecimal(r.Cell(2).GetString());
                            var current = ParseDecimal(r.Cell(3).GetString());
                            var dateStr = r.Cell(4).GetString().Trim();
                            var desc = r.Cell(5).GetString().Trim();

                            if (!string.IsNullOrEmpty(goalName) && target > 0)
                            {
                                var existing = _context.SavingsGoals.FirstOrDefault(s => s.FamilyId == familyDbId.Value && s.GoalName.ToLower() == goalName.ToLower());
                                if (existing == null)
                                {
                                    _context.SavingsGoals.Add(new SavingsGoal
                                    {
                                        FamilyId = familyDbId.Value,
                                        GoalName = goalName,
                                        TargetAmount = target,
                                        CurrentAmount = current,
                                        TargetDate = ParseDate(dateStr),
                                        Description = string.IsNullOrEmpty(desc) ? null : desc
                                    });
                                    goalsAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }

                    // Import Categories
                    if (workbook.TryGetWorksheet("Categories", out var wsCats))
                    {
                        var rows = wsCats.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var cName = r.Cell(1).GetString().Trim();
                            var cType = r.Cell(2).GetString().Trim();
                            var icon = r.Cell(3).GetString().Trim();

                            if (!string.IsNullOrEmpty(cName))
                            {
                                var existing = _context.Categories.FirstOrDefault(c => c.FamilyId == familyDbId.Value && c.Name.ToLower() == cName.ToLower() && c.Type.ToLower() == cType.ToLower());
                                if (existing == null)
                                {
                                    _context.Categories.Add(new Category
                                    {
                                        FamilyId = familyDbId.Value,
                                        Name = cName,
                                        Type = string.IsNullOrEmpty(cType) ? "Expense" : cType,
                                        Icon = string.IsNullOrEmpty(icon) ? "fa-tag" : icon
                                    });
                                    categoriesAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }

                    // Import Budgets
                    if (workbook.TryGetWorksheet("Budgets", out var wsBudgets))
                    {
                        var rows = wsBudgets.RangeUsed().RowsUsed().Skip(1);
                        foreach (var r in rows)
                        {
                            var bCategory = r.Cell(1).GetString().Trim();
                            var bMonth = r.Cell(2).GetString().Trim();
                            var bAmount = ParseDecimal(r.Cell(3).GetString());

                            if (!string.IsNullOrEmpty(bCategory) && bAmount > 0)
                            {
                                var existing = _context.Budgets.FirstOrDefault(b => b.FamilyId == familyDbId.Value && b.Category.ToLower() == bCategory.ToLower() && b.Month == bMonth);
                                if (existing == null)
                                {
                                    _context.Budgets.Add(new Budget
                                    {
                                        FamilyId = familyDbId.Value,
                                        Category = bCategory,
                                        Month = string.IsNullOrEmpty(bMonth) ? DateTime.Now.ToString("yyyy-MM") : bMonth,
                                        Amount = bAmount
                                    });
                                    budgetsAdded++;
                                }
                            }
                        }
                        _context.SaveChanges();
                    }
                }
                // 2. CSV IMPORT (.csv)
                else if (extension == ".csv")
                {
                    using var reader = new StreamReader(backupFile.OpenReadStream(), Encoding.UTF8);
                    string? line;
                    bool isHeader = true;

                    while ((line = reader.ReadLine()) != null)
                    {
                        if (string.IsNullOrWhiteSpace(line)) continue;
                        if (isHeader) { isHeader = false; continue; }

                        var cols = ParseCsvLine(line);
                        if (cols.Count < 5) continue;

                        var recordType = cols[0].ToUpperInvariant();
                        var dateStr = cols.Count > 1 ? cols[1] : "";
                        var name = cols.Count > 2 ? cols[2] : "";
                        var member = cols.Count > 3 ? cols[3] : "";
                        var catOrSource = cols.Count > 4 ? cols[4] : "";
                        var typeOrRel = cols.Count > 5 ? cols[5] : "";
                        var amount = cols.Count > 6 ? ParseDecimal(cols[6]) : 0;
                        var secAmount = cols.Count > 7 ? ParseDecimal(cols[7]) : 0;
                        var remAmount = cols.Count > 8 ? ParseDecimal(cols[8]) : 0;
                        var status = cols.Count > 9 ? cols[9] : "";
                        var targetDateStr = cols.Count > 10 ? cols[10] : "";
                        var descOrReason = cols.Count > 11 ? cols[11] : "";

                        DateTime date = ParseDate(dateStr);

                        if (recordType == "MEMBER" && !string.IsNullOrEmpty(name))
                        {
                            var existing = _context.Members.FirstOrDefault(m => m.FamilyId == familyDbId.Value && m.MemberName.ToLower() == name.ToLower());
                            if (existing == null)
                            {
                                _context.Members.Add(new Member
                                {
                                    FamilyId = familyDbId.Value,
                                    MemberName = name,
                                    Relation = string.IsNullOrEmpty(typeOrRel) ? "Member" : typeOrRel,
                                    Mobile = descOrReason,
                                    Password = BCrypt.Net.BCrypt.HashPassword("123456")
                                });
                                membersAdded++;
                            }
                        }
                        else if (recordType == "INCOME" && amount > 0)
                        {
                            var existing = _context.Incomes.FirstOrDefault(i => i.FamilyId == familyDbId.Value && i.Date.Date == date.Date && i.Amount == amount && i.Source.ToLower() == catOrSource.ToLower());
                            if (existing == null)
                            {
                                _context.Incomes.Add(new Income
                                {
                                    FamilyId = familyDbId.Value,
                                    MemberName = string.IsNullOrEmpty(member) ? "Father" : member,
                                    Source = string.IsNullOrEmpty(catOrSource) ? "Income" : catOrSource,
                                    Amount = amount,
                                    Date = date,
                                    Description = string.IsNullOrEmpty(descOrReason) ? null : descOrReason
                                });
                                incomesAdded++;
                            }
                        }
                        else if (recordType == "EXPENSE" && amount > 0)
                        {
                            var existing = _context.Expenses.FirstOrDefault(e => e.FamilyId == familyDbId.Value && e.Date.Date == date.Date && e.Amount == amount && e.Category.ToLower() == catOrSource.ToLower());
                            if (existing == null)
                            {
                                _context.Expenses.Add(new Expense
                                {
                                    FamilyId = familyDbId.Value,
                                    MemberName = string.IsNullOrEmpty(member) ? "Father" : member,
                                    Category = string.IsNullOrEmpty(catOrSource) ? "General" : catOrSource,
                                    Amount = amount,
                                    Date = date,
                                    Description = string.IsNullOrEmpty(descOrReason) ? null : descOrReason
                                });
                                expensesAdded++;
                            }
                        }
                        else if (recordType == "UDHAR" && amount > 0)
                        {
                            var udharType = string.IsNullOrEmpty(typeOrRel) ? "Dene Hai" : typeOrRel;
                            var remaining = remAmount > 0 ? remAmount : Math.Max(0, amount - secAmount);
                            var udharStatus = !string.IsNullOrEmpty(status) ? status : (remaining <= 0 ? "Completed" : "Pending");

                            var existing = _context.Udhar.FirstOrDefault(u => u.FamilyId == familyDbId.Value && u.PersonName.ToLower() == name.ToLower() && u.Type == udharType && u.Amount == amount && u.Date.Date == date.Date);
                            if (existing == null)
                            {
                                _context.Udhar.Add(new Udhar
                                {
                                    FamilyId = familyDbId.Value,
                                    PersonName = name,
                                    MemberName = string.IsNullOrEmpty(member) ? "Father" : member,
                                    Type = udharType,
                                    Amount = amount,
                                    PaidAmount = secAmount,
                                    RemainingAmount = remaining,
                                    Status = udharStatus,
                                    Reason = string.IsNullOrEmpty(descOrReason) ? null : descOrReason,
                                    Date = date
                                });
                                udharAdded++;
                            }
                        }
                        else if (recordType == "SAVINGS_GOAL" && amount > 0)
                        {
                            var existing = _context.SavingsGoals.FirstOrDefault(s => s.FamilyId == familyDbId.Value && s.GoalName.ToLower() == name.ToLower());
                            if (existing == null)
                            {
                                _context.SavingsGoals.Add(new SavingsGoal
                                {
                                    FamilyId = familyDbId.Value,
                                    GoalName = name,
                                    TargetAmount = amount,
                                    CurrentAmount = secAmount,
                                    TargetDate = ParseDate(targetDateStr),
                                    Description = string.IsNullOrEmpty(descOrReason) ? null : descOrReason
                                });
                                goalsAdded++;
                            }
                        }
                        else if (recordType == "CATEGORY" && !string.IsNullOrEmpty(name))
                        {
                            var existing = _context.Categories.FirstOrDefault(c => c.FamilyId == familyDbId.Value && c.Name.ToLower() == name.ToLower() && c.Type.ToLower() == typeOrRel.ToLower());
                            if (existing == null)
                            {
                                _context.Categories.Add(new Category
                                {
                                    FamilyId = familyDbId.Value,
                                    Name = name,
                                    Type = string.IsNullOrEmpty(typeOrRel) ? "Expense" : typeOrRel,
                                    Icon = string.IsNullOrEmpty(descOrReason) ? "fa-tag" : descOrReason
                                });
                                categoriesAdded++;
                            }
                        }
                        else if (recordType == "BUDGET" && amount > 0)
                        {
                            var existing = _context.Budgets.FirstOrDefault(b => b.FamilyId == familyDbId.Value && b.Category.ToLower() == name.ToLower() && b.Month == catOrSource);
                            if (existing == null)
                            {
                                _context.Budgets.Add(new Budget
                                {
                                    FamilyId = familyDbId.Value,
                                    Category = name,
                                    Month = string.IsNullOrEmpty(catOrSource) ? DateTime.Now.ToString("yyyy-MM") : catOrSource,
                                    Amount = amount
                                });
                                budgetsAdded++;
                            }
                        }
                    }
                    _context.SaveChanges();
                }
                // 3. PDF IMPORT (.pdf) - Extracts Embedded Lossless Base64 JSON
                else if (extension == ".pdf")
                {
                    using var ms = new MemoryStream();
                    backupFile.CopyTo(ms);
                    var fileBytes = ms.ToArray();
                    var fileText = Encoding.UTF8.GetString(fileBytes);

                    int startMarker = fileText.IndexOf("%%HOMELEDGER_DATA_START%%");
                    int endMarker = fileText.IndexOf("%%HOMELEDGER_DATA_END%%");

                    if (startMarker == -1 || endMarker == -1 || endMarker <= startMarker)
                    {
                        TempData["Error"] = "Yeh PDF HomeLedger verified backup format me nahi hai ya iska data stream corrupted hai. Kripya HomeLedger se export ki hui PDF upload karein.";
                        return RedirectToAction("Index");
                    }

                    var base64 = fileText.Substring(startMarker + "%%HOMELEDGER_DATA_START%%".Length, endMarker - (startMarker + "%%HOMELEDGER_DATA_START%%".Length)).Trim();
                    var jsonBytes = Convert.FromBase64String(base64);
                    var json = Encoding.UTF8.GetString(jsonBytes);

                    var result = ImportFromJson(json, familyDbId.Value);
                    membersAdded = result.members;
                    incomesAdded = result.incomes;
                    expensesAdded = result.expenses;
                    udharAdded = result.udhar;
                    goalsAdded = result.goals;
                    categoriesAdded = result.categories;
                    budgetsAdded = result.budgets;
                }
                // 4. JSON IMPORT (.json)
                else if (extension == ".json")
                {
                    using var reader = new StreamReader(backupFile.OpenReadStream(), Encoding.UTF8);
                    var json = reader.ReadToEnd();
                    var result = ImportFromJson(json, familyDbId.Value);
                    membersAdded = result.members;
                    incomesAdded = result.incomes;
                    expensesAdded = result.expenses;
                    udharAdded = result.udhar;
                    goalsAdded = result.goals;
                    categoriesAdded = result.categories;
                    budgetsAdded = result.budgets;
                }
                else
                {
                    TempData["Error"] = "Unsupported file format. Kripya .xlsx, .csv, .pdf, ya .json file upload karein.";
                    return RedirectToAction("Index");
                }

                transaction.Commit();

                TempData["Success"] = $"✓ Backup safely imported from {extension.ToUpper()}! Restored: {membersAdded} Members, {incomesAdded} Incomes, {expensesAdded} Expenses, {udharAdded} Udhar records, {goalsAdded} Savings Goals, {categoriesAdded} Categories, {budgetsAdded} Budgets.";
            }
            catch (Exception ex)
            {
                transaction.Rollback();
                TempData["Error"] = $"Error importing backup: {ex.Message}";
            }

            return RedirectToAction("Index");
        }

        private (int members, int incomes, int expenses, int udhar, int goals, int categories, int budgets) ImportFromJson(string json, int familyId)
        {
            int membersAdded = 0, incomesAdded = 0, expensesAdded = 0, udharAdded = 0, goalsAdded = 0, categoriesAdded = 0, budgetsAdded = 0;
            using var doc = JsonDocument.Parse(json);
            var root = doc.RootElement;

            // Members
            if (root.TryGetProperty("Members", out var members))
            {
                foreach (var m in members.EnumerateArray())
                {
                    var name = m.GetProperty("MemberName").GetString() ?? "";
                    var rel = m.TryGetProperty("Relation", out var r) ? r.GetString() ?? "Member" : "Member";
                    var mob = m.TryGetProperty("Mobile", out var mb) ? mb.GetString() : null;

                    if (!string.IsNullOrEmpty(name))
                    {
                        var existing = _context.Members.FirstOrDefault(x => x.FamilyId == familyId && x.MemberName.ToLower() == name.ToLower());
                        if (existing == null)
                        {
                            _context.Members.Add(new Member
                            {
                                FamilyId = familyId,
                                MemberName = name,
                                Relation = rel,
                                Mobile = mob,
                                Password = BCrypt.Net.BCrypt.HashPassword("123456")
                            });
                            membersAdded++;
                        }
                    }
                }
                _context.SaveChanges();
            }

            // Incomes
            if (root.TryGetProperty("Incomes", out var incomes))
            {
                foreach (var i in incomes.EnumerateArray())
                {
                    var src = i.GetProperty("Source").GetString() ?? "";
                    var amt = i.GetProperty("Amount").GetDecimal();
                    var dt = i.GetProperty("Date").GetDateTime();
                    var mem = i.TryGetProperty("MemberName", out var mn) ? mn.GetString() ?? "Father" : "Father";
                    var desc = i.TryGetProperty("Description", out var ds) ? ds.GetString() : null;

                    var existing = _context.Incomes.FirstOrDefault(x => x.FamilyId == familyId && x.Date.Date == dt.Date && x.Amount == amt && x.Source.ToLower() == src.ToLower());
                    if (existing == null)
                    {
                        _context.Incomes.Add(new Income
                        {
                            FamilyId = familyId,
                            Source = src,
                            Amount = amt,
                            Date = dt,
                            MemberName = mem,
                            Description = desc
                        });
                        incomesAdded++;
                    }
                }
                _context.SaveChanges();
            }

            // Expenses
            if (root.TryGetProperty("Expenses", out var expenses))
            {
                foreach (var e in expenses.EnumerateArray())
                {
                    var cat = e.GetProperty("Category").GetString() ?? "";
                    var amt = e.GetProperty("Amount").GetDecimal();
                    var dt = e.GetProperty("Date").GetDateTime();
                    var mem = e.TryGetProperty("MemberName", out var mn) ? mn.GetString() ?? "Father" : "Father";
                    var desc = e.TryGetProperty("Description", out var ds) ? ds.GetString() : null;

                    var existing = _context.Expenses.FirstOrDefault(x => x.FamilyId == familyId && x.Date.Date == dt.Date && x.Amount == amt && x.Category.ToLower() == cat.ToLower());
                    if (existing == null)
                    {
                        _context.Expenses.Add(new Expense
                        {
                            FamilyId = familyId,
                            Category = cat,
                            Amount = amt,
                            Date = dt,
                            MemberName = mem,
                            Description = desc
                        });
                        expensesAdded++;
                    }
                }
                _context.SaveChanges();
            }

            // Udhar
            if (root.TryGetProperty("Udhar", out var udhar))
            {
                foreach (var u in udhar.EnumerateArray())
                {
                    var person = u.GetProperty("PersonName").GetString() ?? "";
                    var type = u.GetProperty("Type").GetString() ?? "Dene Hai";
                    var amt = u.GetProperty("Amount").GetDecimal();
                    var paid = u.TryGetProperty("PaidAmount", out var pa) ? pa.GetDecimal() : 0;
                    var rem = u.TryGetProperty("RemainingAmount", out var ra) ? ra.GetDecimal() : Math.Max(0, amt - paid);
                    var dt = u.GetProperty("Date").GetDateTime();
                    var mem = u.TryGetProperty("MemberName", out var mn) ? mn.GetString() ?? "Father" : "Father";
                    var status = u.TryGetProperty("Status", out var st) ? st.GetString() ?? "Pending" : "Pending";
                    var reason = u.TryGetProperty("Reason", out var rs) ? rs.GetString() : null;

                    var existing = _context.Udhar.FirstOrDefault(x => x.FamilyId == familyId && x.PersonName.ToLower() == person.ToLower() && x.Type == type && x.Amount == amt && x.Date.Date == dt.Date);
                    if (existing == null)
                    {
                        _context.Udhar.Add(new Udhar
                        {
                            FamilyId = familyId,
                            PersonName = person,
                            Type = type,
                            Amount = amt,
                            PaidAmount = paid,
                            RemainingAmount = rem,
                            Date = dt,
                            MemberName = mem,
                            Status = status,
                            Reason = reason
                        });
                        udharAdded++;
                    }
                }
                _context.SaveChanges();
            }

            // Savings Goals
            if (root.TryGetProperty("SavingsGoals", out var goals))
            {
                foreach (var g in goals.EnumerateArray())
                {
                    var gName = g.GetProperty("GoalName").GetString() ?? "";
                    var target = g.GetProperty("TargetAmount").GetDecimal();
                    var curr = g.TryGetProperty("CurrentAmount", out var ca) ? ca.GetDecimal() : 0;
                    var targetDate = g.GetProperty("TargetDate").GetDateTime();
                    var desc = g.TryGetProperty("Description", out var ds) ? ds.GetString() : null;

                    var existing = _context.SavingsGoals.FirstOrDefault(x => x.FamilyId == familyId && x.GoalName.ToLower() == gName.ToLower());
                    if (existing == null)
                    {
                        _context.SavingsGoals.Add(new SavingsGoal
                        {
                            FamilyId = familyId,
                            GoalName = gName,
                            TargetAmount = target,
                            CurrentAmount = curr,
                            TargetDate = targetDate,
                            Description = desc
                        });
                        goalsAdded++;
                    }
                }
                _context.SaveChanges();
            }

            // Categories
            if (root.TryGetProperty("Categories", out var cats))
            {
                foreach (var c in cats.EnumerateArray())
                {
                    var cName = c.GetProperty("Name").GetString() ?? "";
                    var cType = c.GetProperty("Type").GetString() ?? "Expense";
                    var icon = c.TryGetProperty("Icon", out var ic) ? ic.GetString() : "fa-tag";

                    var existing = _context.Categories.FirstOrDefault(x => x.FamilyId == familyId && x.Name.ToLower() == cName.ToLower() && x.Type.ToLower() == cType.ToLower());
                    if (existing == null)
                    {
                        _context.Categories.Add(new Category
                        {
                            FamilyId = familyId,
                            Name = cName,
                            Type = cType,
                            Icon = icon
                        });
                        categoriesAdded++;
                    }
                }
                _context.SaveChanges();
            }

            // Budgets
            if (root.TryGetProperty("Budgets", out var bgts))
            {
                foreach (var b in bgts.EnumerateArray())
                {
                    var cat = b.GetProperty("Category").GetString() ?? "";
                    var mth = b.GetProperty("Month").GetString() ?? "";
                    var amt = b.GetProperty("Amount").GetDecimal();

                    var existing = _context.Budgets.FirstOrDefault(x => x.FamilyId == familyId && x.Category.ToLower() == cat.ToLower() && x.Month == mth);
                    if (existing == null)
                    {
                        _context.Budgets.Add(new Budget
                        {
                            FamilyId = familyId,
                            Category = cat,
                            Month = mth,
                            Amount = amt
                        });
                        budgetsAdded++;
                    }
                }
                _context.SaveChanges();
            }

            return (membersAdded, incomesAdded, expensesAdded, udharAdded, goalsAdded, categoriesAdded, budgetsAdded);
        }

        #endregion

        #region Helper Methods

        private FamilyBackupPayload FetchFamilyData(int familyId)
        {
            return new FamilyBackupPayload
            {
                ExportDate = DateTime.Now,
                FamilyId = familyId,
                Family = _context.Families.AsNoTracking().FirstOrDefault(f => f.Id == familyId),
                Members = _context.Members.AsNoTracking().Where(m => m.FamilyId == familyId).ToList(),
                Incomes = _context.Incomes.AsNoTracking().Where(i => i.FamilyId == familyId).OrderByDescending(i => i.Date).ToList(),
                Expenses = _context.Expenses.AsNoTracking().Where(e => e.FamilyId == familyId).OrderByDescending(e => e.Date).ToList(),
                Udhar = _context.Udhar.AsNoTracking().Where(u => u.FamilyId == familyId).OrderByDescending(u => u.Date).ToList(),
                SavingsGoals = _context.SavingsGoals.AsNoTracking().Where(s => s.FamilyId == familyId).ToList(),
                Budgets = _context.Budgets.AsNoTracking().Where(b => b.FamilyId == familyId).ToList(),
                Reminders = _context.Reminders.AsNoTracking().Where(r => r.FamilyId == familyId).ToList(),
                Categories = _context.Categories.AsNoTracking().Where(c => c.FamilyId == familyId).ToList(),
                RecurringExpenses = _context.RecurringExpenses.AsNoTracking().Where(r => r.FamilyId == familyId).ToList(),
                RecurringIncomes = _context.RecurringIncomes.AsNoTracking().Where(r => r.FamilyId == familyId).ToList()
            };
        }

        private static void AddHeaders(IXLWorksheet sheet, string[] headers)
        {
            for (int i = 0; i < headers.Length; i++)
            {
                var cell = sheet.Cell(1, i + 1);
                cell.Value = headers[i];
                cell.Style.Font.Bold = true;
                cell.Style.Fill.BackgroundColor = XLColor.FromHtml("#1e293b");
                cell.Style.Font.FontColor = XLColor.White;
                cell.Style.Alignment.Horizontal = XLAlignmentHorizontalValues.Center;
            }
        }

        private static string Escape(string? val)
        {
            if (string.IsNullOrEmpty(val)) return "\"\"";
            return "\"" + val.Replace("\"", "\"\"") + "\"";
        }

        private static List<string> ParseCsvLine(string line)
        {
            var list = new List<string>();
            if (string.IsNullOrEmpty(line)) return list;

            bool inQuotes = false;
            var sb = new StringBuilder();

            for (int i = 0; i < line.Length; i++)
            {
                char c = line[i];
                if (c == '\"')
                {
                    if (inQuotes && i + 1 < line.Length && line[i + 1] == '\"')
                    {
                        sb.Append('\"');
                        i++;
                    }
                    else
                    {
                        inQuotes = !inQuotes;
                    }
                }
                else if (c == ',' && !inQuotes)
                {
                    list.Add(sb.ToString().Trim());
                    sb.Clear();
                }
                else
                {
                    sb.Append(c);
                }
            }
            list.Add(sb.ToString().Trim());
            return list;
        }

        private static decimal ParseDecimal(string? str)
        {
            if (string.IsNullOrWhiteSpace(str)) return 0;
            str = str.Replace("₹", "").Replace(",", "").Trim();
            if (decimal.TryParse(str, NumberStyles.Any, CultureInfo.InvariantCulture, out var val))
            {
                return val;
            }
            if (decimal.TryParse(str, NumberStyles.Any, CultureInfo.CurrentCulture, out var valLocal))
            {
                return valLocal;
            }
            return 0;
        }

        private static DateTime ParseDate(string? str)
        {
            if (string.IsNullOrWhiteSpace(str)) return DateTime.Today;
            if (DateTime.TryParse(str, out var dt))
            {
                return dt;
            }
            return DateTime.Today;
        }

        #endregion
    }

    public class FamilyBackupPayload
    {
        public DateTime ExportDate { get; set; } = DateTime.Now;
        public int FamilyId { get; set; }
        public Family? Family { get; set; }
        public List<Member> Members { get; set; } = new();
        public List<Income> Incomes { get; set; } = new();
        public List<Expense> Expenses { get; set; } = new();
        public List<Udhar> Udhar { get; set; } = new();
        public List<SavingsGoal> SavingsGoals { get; set; } = new();
        public List<Budget> Budgets { get; set; } = new();
        public List<Reminder> Reminders { get; set; } = new();
        public List<Category> Categories { get; set; } = new();
        public List<RecurringExpense> RecurringExpenses { get; set; } = new();
        public List<RecurringIncome> RecurringIncomes { get; set; } = new();
    }
}
