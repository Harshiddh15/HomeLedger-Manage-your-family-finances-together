using FinanceManagementNet.Data;
using FinanceManagementNet.Models;
using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using System.Text.Json;
using System.Text.Json.Serialization;

namespace FinanceManagementNet.Controllers
{
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

            return View();
        }

        public IActionResult ExportBackup()
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            var backupData = new
            {
                ExportDate = DateTime.Now,
                FamilyId = familyDbId.Value,
                Family = _context.Families.AsNoTracking().FirstOrDefault(f => f.Id == familyDbId.Value),
                Members = _context.Members.AsNoTracking().Where(m => m.FamilyId == familyDbId.Value).ToList(),
                Incomes = _context.Incomes.AsNoTracking().Where(i => i.FamilyId == familyDbId.Value).ToList(),
                Expenses = _context.Expenses.AsNoTracking().Where(e => e.FamilyId == familyDbId.Value).ToList(),
                Udhar = _context.Udhar.AsNoTracking().Where(u => u.FamilyId == familyDbId.Value).ToList(),
                Reminders = _context.Reminders.AsNoTracking().Where(r => r.FamilyId == familyDbId.Value).ToList(),
                Budgets = _context.Budgets.AsNoTracking().Where(b => b.FamilyId == familyDbId.Value).ToList(),
                SavingsGoals = _context.SavingsGoals.AsNoTracking().Where(s => s.FamilyId == familyDbId.Value).ToList(),
                RecurringExpenses = _context.RecurringExpenses.AsNoTracking().Where(r => r.FamilyId == familyDbId.Value).ToList(),
                RecurringIncomes = _context.RecurringIncomes.AsNoTracking().Where(r => r.FamilyId == familyDbId.Value).ToList(),
                Categories = _context.Categories.AsNoTracking().Where(c => c.FamilyId == familyDbId.Value).ToList()
            };

            var json = JsonSerializer.Serialize(backupData, new JsonSerializerOptions
            {
                WriteIndented = true,
                ReferenceHandler = ReferenceHandler.IgnoreCycles
            });

            var bytes = System.Text.Encoding.UTF8.GetBytes(json);
            var fileName = $"backup_{DateTime.Now:yyyyMMdd_HHmmss}.json";

            return File(bytes, "application/json", fileName);
        }

        [HttpPost]
        public IActionResult ImportBackup(IFormFile backupFile)
        {
            var familyDbId = HttpContext.Session.GetInt32("FamilyDbId");
            if (familyDbId == null)
            {
                return RedirectToAction("Login", "Account");
            }

            if (backupFile == null || backupFile.Length == 0)
            {
                TempData["Error"] = "Please select a backup file to import.";
                return RedirectToAction("Index");
            }

            try
            {
                using (var reader = new StreamReader(backupFile.OpenReadStream()))
                {
                    var json = reader.ReadToEnd();
                    var backupData = JsonSerializer.Deserialize<JsonElement>(json);

                    // Import Categories
                    if (backupData.TryGetProperty("Categories", out var categories))
                    {
                        foreach (var category in categories.EnumerateArray())
                        {
                            var existingCategory = _context.Categories.FirstOrDefault(c => c.Id == category.GetProperty("Id").GetInt32());
                            if (existingCategory == null)
                            {
                                var newCategory = new Category
                                {
                                    Id = category.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    Name = category.GetProperty("Name").GetString() ?? "",
                                    Type = category.GetProperty("Type").GetString() ?? "",
                                    Icon = category.TryGetProperty("Icon", out var icon) ? icon.GetString() : null,
                                    Color = category.TryGetProperty("Color", out var color) ? color.GetString() : null
                                };
                                _context.Categories.Add(newCategory);
                            }
                        }
                    }

                    // Import Members
                    if (backupData.TryGetProperty("Members", out var members))
                    {
                        foreach (var member in members.EnumerateArray())
                        {
                            var existingMember = _context.Members.FirstOrDefault(m => m.Id == member.GetProperty("Id").GetInt32());
                            if (existingMember == null)
                            {
                                var newMember = new Member
                                {
                                    Id = member.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    MemberName = member.GetProperty("MemberName").GetString() ?? "",
                                    Relation = member.GetProperty("Relation").GetString() ?? "",
                                    Mobile = member.TryGetProperty("Mobile", out var mobile) ? mobile.GetString() : null,
                                    ProfileImage = member.TryGetProperty("ProfileImage", out var profile) ? profile.GetString() : null
                                };
                                _context.Members.Add(newMember);
                            }
                        }
                    }

                    // Import Incomes
                    if (backupData.TryGetProperty("Incomes", out var incomes))
                    {
                        foreach (var income in incomes.EnumerateArray())
                        {
                            var existingIncome = _context.Incomes.FirstOrDefault(i => i.Id == income.GetProperty("Id").GetInt32());
                            if (existingIncome == null)
                            {
                                var newIncome = new Income
                                {
                                    Id = income.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    MemberName = income.GetProperty("MemberName").GetString() ?? "",
                                    Amount = income.GetProperty("Amount").GetDecimal(),
                                    Source = income.GetProperty("Source").GetString() ?? "",
                                    Date = income.GetProperty("Date").GetDateTime(),
                                    Description = income.TryGetProperty("Description", out var desc) ? desc.GetString() : null
                                };
                                _context.Incomes.Add(newIncome);
                            }
                        }
                    }

                    // Import Expenses
                    if (backupData.TryGetProperty("Expenses", out var expenses))
                    {
                        foreach (var expense in expenses.EnumerateArray())
                        {
                            var existingExpense = _context.Expenses.FirstOrDefault(e => e.Id == expense.GetProperty("Id").GetInt32());
                            if (existingExpense == null)
                            {
                                var newExpense = new Expense
                                {
                                    Id = expense.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    MemberName = expense.GetProperty("MemberName").GetString() ?? "",
                                    Category = expense.GetProperty("Category").GetString() ?? "",
                                    Amount = expense.GetProperty("Amount").GetDecimal(),
                                    Date = expense.GetProperty("Date").GetDateTime(),
                                    Description = expense.TryGetProperty("Description", out var desc) ? desc.GetString() : null
                                };
                                _context.Expenses.Add(newExpense);
                            }
                        }
                    }

                    // Import Udhar
                    if (backupData.TryGetProperty("Udhar", out var udhar))
                    {
                        foreach (var udharItem in udhar.EnumerateArray())
                        {
                            var existingUdhar = _context.Udhar.FirstOrDefault(u => u.Id == udharItem.GetProperty("Id").GetInt32());
                            if (existingUdhar == null)
                            {
                                var newUdhar = new Udhar
                                {
                                    Id = udharItem.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    PersonName = udharItem.GetProperty("PersonName").GetString() ?? "",
                                    MemberName = udharItem.TryGetProperty("MemberName", out var member) ? member.GetString() : null,
                                    ProofImage = udharItem.TryGetProperty("ProofImage", out var proof) ? proof.GetString() : null,
                                    Type = udharItem.GetProperty("Type").GetString() ?? "",
                                    Amount = udharItem.GetProperty("Amount").GetDecimal(),
                                    PaidAmount = udharItem.GetProperty("PaidAmount").GetDecimal(),
                                    RemainingAmount = udharItem.GetProperty("RemainingAmount").GetDecimal(),
                                    Reason = udharItem.TryGetProperty("Reason", out var reason) ? reason.GetString() : null,
                                    Date = udharItem.GetProperty("Date").GetDateTime(),
                                    Status = udharItem.GetProperty("Status").GetString() ?? "Pending"
                                };
                                _context.Udhar.Add(newUdhar);
                            }
                        }
                    }

                    // Import Reminders
                    if (backupData.TryGetProperty("Reminders", out var reminders))
                    {
                        foreach (var reminder in reminders.EnumerateArray())
                        {
                            var existingReminder = _context.Reminders.FirstOrDefault(r => r.Id == reminder.GetProperty("Id").GetInt32());
                            if (existingReminder == null)
                            {
                                var newReminder = new Reminder
                                {
                                    Id = reminder.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    Title = reminder.GetProperty("Title").GetString() ?? "",
                                    Date = reminder.GetProperty("Date").GetDateTime(),
                                    Description = reminder.TryGetProperty("Description", out var desc) ? desc.GetString() : null
                                };
                                _context.Reminders.Add(newReminder);
                            }
                        }
                    }

                    // Import Budgets
                    if (backupData.TryGetProperty("Budgets", out var budgets))
                    {
                        foreach (var budget in budgets.EnumerateArray())
                        {
                            var existingBudget = _context.Budgets.FirstOrDefault(b => b.Id == budget.GetProperty("Id").GetInt32());
                            if (existingBudget == null)
                            {
                                var newBudget = new Budget
                                {
                                    Id = budget.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    Category = budget.GetProperty("Category").GetString() ?? "",
                                    Amount = budget.GetProperty("Amount").GetDecimal(),
                                    Month = budget.GetProperty("Month").GetString() ?? ""
                                };
                                _context.Budgets.Add(newBudget);
                            }
                        }
                    }

                    // Import Savings Goals
                    if (backupData.TryGetProperty("SavingsGoals", out var savingsGoals))
                    {
                        foreach (var goal in savingsGoals.EnumerateArray())
                        {
                            var existingGoal = _context.SavingsGoals.FirstOrDefault(s => s.Id == goal.GetProperty("Id").GetInt32());
                            if (existingGoal == null)
                            {
                                var newGoal = new SavingsGoal
                                {
                                    Id = goal.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    GoalName = goal.GetProperty("GoalName").GetString() ?? "",
                                    TargetAmount = goal.GetProperty("TargetAmount").GetDecimal(),
                                    CurrentAmount = goal.GetProperty("CurrentAmount").GetDecimal(),
                                    TargetDate = goal.GetProperty("TargetDate").GetDateTime(),
                                    Description = goal.TryGetProperty("Description", out var desc) ? desc.GetString() : null
                                };
                                _context.SavingsGoals.Add(newGoal);
                            }
                        }
                    }

                    // Import Recurring Expenses
                    if (backupData.TryGetProperty("RecurringExpenses", out var recurringExpenses))
                    {
                        foreach (var re in recurringExpenses.EnumerateArray())
                        {
                            var existingRE = _context.RecurringExpenses.FirstOrDefault(r => r.Id == re.GetProperty("Id").GetInt32());
                            if (existingRE == null)
                            {
                                var newRE = new RecurringExpense
                                {
                                    Id = re.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    MemberName = re.GetProperty("MemberName").GetString() ?? "",
                                    Category = re.GetProperty("Category").GetString() ?? "",
                                    Amount = re.GetProperty("Amount").GetDecimal(),
                                    Frequency = re.GetProperty("Frequency").GetString() ?? "",
                                    DayOfMonth = re.GetProperty("DayOfMonth").GetInt32(),
                                    Description = re.TryGetProperty("Description", out var desc) ? desc.GetString() : null,
                                    IsActive = re.GetProperty("IsActive").GetBoolean()
                                };
                                _context.RecurringExpenses.Add(newRE);
                            }
                        }
                    }

                    // Import Recurring Incomes
                    if (backupData.TryGetProperty("RecurringIncomes", out var recurringIncomes))
                    {
                        foreach (var ri in recurringIncomes.EnumerateArray())
                        {
                            var existingRI = _context.RecurringIncomes.FirstOrDefault(r => r.Id == ri.GetProperty("Id").GetInt32());
                            if (existingRI == null)
                            {
                                var newRI = new RecurringIncome
                                {
                                    Id = ri.GetProperty("Id").GetInt32(),
                                    FamilyId = familyDbId.Value,
                                    MemberName = ri.GetProperty("MemberName").GetString() ?? "",
                                    Source = ri.GetProperty("Source").GetString() ?? "",
                                    Amount = ri.GetProperty("Amount").GetDecimal(),
                                    Frequency = ri.GetProperty("Frequency").GetString() ?? "",
                                    DayOfMonth = ri.GetProperty("DayOfMonth").GetInt32(),
                                    Description = ri.TryGetProperty("Description", out var desc) ? desc.GetString() : null,
                                    IsActive = ri.GetProperty("IsActive").GetBoolean()
                                };
                                _context.RecurringIncomes.Add(newRI);
                            }
                        }
                    }

                    _context.SaveChanges();
                    TempData["Success"] = "Backup imported successfully!";
                }
            }
            catch (Exception ex)
            {
                TempData["Error"] = $"Error importing backup: {ex.Message}";
            }

            return RedirectToAction("Index");
        }
    }
}
