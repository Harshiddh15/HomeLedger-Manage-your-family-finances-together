import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.options import Options

tree_lines = [
    ("Family_Finance_Management/", ""),
    ("|-- Controllers/", "# Controller Layer (Request Orchestration & Business Logic)"),
    ("|   |-- AccountController.cs", "# Dual Authentication (Admin/Member), Registration & Password Reset"),
    ("|   |-- HomeController.cs", "# Executive Overview Dashboard & Real-Time Financial KPIs"),
    ("|   |-- MemberController.cs", "# Family Member Profiles, Relations & Access Credentials"),
    ("|   |-- IncomeController.cs", "# Inflow Ledger, Earnings History, CSV & QuestPDF Export"),
    ("|   |-- ExpenseController.cs", "# Outflow Tracker, Category Allocation, CSV & QuestPDF Export"),
    ("|   |-- CategoryController.cs", "# Financial Taxonomies, Visual Color Badges & Icons"),
    ("|   |-- BudgetController.cs", "# Monthly Category Spending Limits & Real-Time Limit Enforcement"),
    ("|   |-- RecurringIncomeController.cs", "# Automated Scheduled Inflows (Salaries, Rental Yields)"),
    ("|   |-- RecurringExpenseController.cs", "# Automated Scheduled Outflows (Bills, Subscriptions)"),
    ("|   |-- SavingsGoalController.cs", "# Milestone Wealth Accumulation, Target Dates & Progress Additions"),
    ("|   |-- UdharController.cs", "# Informal Debt Ledger ('Lene Hai' vs 'Dene Hai' & Partial Repayments)"),
    ("|   |-- ReminderController.cs", "# Event-Driven Due Date Calendar Alerts for Utilities & Bills"),
    ("|   |-- ReportController.cs", "# Monthly Breakdown Reports, Annual Cash Flow & Analytics Hub"),
    ("|   +-- BackupController.cs", "# Full Database JSON Snapshot Export & Disaster Restore"),
    ("|-- Models/", "# Model Layer (Domain Entities & ViewModels)"),
    ("|   |-- Family.cs", "# Master Household Entity & Cryptographic Authentication Hash"),
    ("|   |-- Member.cs", "# Family Member Details, Household Relation & Individual Role"),
    ("|   |-- Income.cs", "# Inflow Transaction Record Schema & Member Attribution"),
    ("|   |-- Expense.cs", "# Expenditure Schema, Category Binding & Purchase Notes"),
    ("|   |-- Category.cs", "# Financial Category Taxonomy with Color Markers & Icons"),
    ("|   |-- Budget.cs", "# Category-Specific Monthly Expenditure Caps (YYYY-MM)"),
    ("|   |-- RecurringIncome.cs", "# Scheduled Periodic Earnings Rules & Execution Day"),
    ("|   |-- RecurringExpense.cs", "# Scheduled Periodic Outflows Rules & Frequency Cycle"),
    ("|   |-- SavingsGoal.cs", "# Target Capital Goals, Accumulated Balances & Deadlines"),
    ("|   |-- Udhar.cs", "# Bilateral Debt Schema (Principal, Paid, Remaining, Status)"),
    ("|   |-- Reminder.cs", "# Financial Event Due Date Reminder Schema"),
    ("|   |-- DashboardViewModel.cs", "# Multi-Card KPI Aggregates & Recent Transactions ViewModel"),
    ("|   |-- MonthlyReportViewModel.cs", "# Category Breakdown Percentages & Financial Summary ViewModel"),
    ("|   +-- ErrorViewModel.cs", "# System Exception Diagnostics & HTTP Error State Binding"),
    ("|-- Views/", "# View Layer (Razor .cshtml Dynamic Presentation Templates)"),
    ("|   |-- Account/", "# Login.cshtml, MemberLogin.cshtml, Register.cshtml, ForgotPassword.cshtml"),
    ("|   |-- Home/", "# Dashboard.cshtml, Index.cshtml, Privacy.cshtml"),
    ("|   |-- Member/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- Income/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- Expense/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- Category/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- Budget/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- RecurringIncome/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- RecurringExpense/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- SavingsGoal/", "# Index.cshtml, Create.cshtml, Edit.cshtml, AddAmount.cshtml, Delete.cshtml"),
    ("|   |-- Udhar/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- Reminder/", "# Index.cshtml, Create.cshtml, Edit.cshtml, Delete.cshtml"),
    ("|   |-- Report/", "# Index.cshtml, MonthlyReport.cshtml, YearlyReport.cshtml"),
    ("|   |-- Backup/", "# Index.cshtml (JSON Export & Single-Click Restore)"),
    ("|   +-- Shared/", "# _Layout.cshtml (HUD Admin Master Theme), _ValidationScriptsPartial.cshtml"),
    ("|-- Data/", "# Data Persistence & ORM Infrastructure"),
    ("|   |-- AppDbContext.cs", "# EF Core DbContext, Relational Mappings & MySQL Provider"),
    ("|   +-- Migrations/", "# Automated Database Migration History & Schema Snapshots"),
    ("|-- wwwroot/", "# Static Client-Side Web Assets & Styling"),
    ("|   |-- css/", "# site.css (Custom HUD Admin Cyberpunk Dark UI Theme)"),
    ("|   |-- js/", "# site.js (Search Filters, Real-Time Computations & Event Handlers)"),
    ("|   +-- lib/", "# Client Libraries (Bootstrap 5, jQuery 3.6 & Validation)"),
    ("|-- appsettings.json", "# Database Connection Strings (MySQL) & Logging Configuration"),
    ("|-- Program.cs", "# Application Entry Point, DI Container & Middleware Pipeline"),
    ("+-- FinanceManagementNet.csproj", "# .NET 10.0 Project File & NuGet Dependencies")
]

# Calculate max length of left side to align comments cleanly
max_left = max(len(left) for left, right in tree_lines if right) + 3

html_lines = []
for left, right in tree_lines:
    if right:
        padding = " " * (max_left - len(left))
        # escape html
        left_esc = left.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        right_esc = right.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        line_html = f'<span class="tree-text">{left_esc}</span><span class="tree-space">{padding}</span><span class="tree-comment">{right_esc}</span>'
    else:
        left_esc = left.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        line_html = f'<span class="tree-root">{left_esc}</span>'
    html_lines.append(line_html)

content = "\n".join(html_lines)

html = f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
    body {{
        margin: 0;
        padding: 0;
        background-color: #161616;
        display: inline-block;
    }}
    .terminal-container {{
        background-color: #161616;
        color: #e6edf3;
        font-family: 'Consolas', 'Courier New', 'Fira Code', monospace;
        font-size: 13.5px;
        line-height: 1.45;
        padding: 24px 28px;
        white-space: pre;
        box-sizing: border-box;
        letter-spacing: 0.2px;
    }}
    .tree-root {{
        color: #58a6ff;
        font-weight: bold;
    }}
    .tree-text {{
        color: #f0f6fc;
    }}
    .tree-comment {{
        color: #8b949e;
        font-style: normal;
    }}
</style>
</head>
<body>
<div class="terminal-container" id="terminal">{content}</div>
</body>
</html>
"""

html_path = os.path.abspath("tree_view.html")
with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)

print("Generated tree_view.html")

# Capture screenshot with Selenium Edge
options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1400,3000")
options.add_argument("--hide-scrollbars")
driver = webdriver.Edge(options=options)

driver.get(f"file:///{html_path.replace(os.sep, '/')}")
time.sleep(1)

terminal = driver.find_element(By.ID, "terminal")
out_png1 = os.path.abspath("folder_structure.png")
out_png2 = os.path.abspath("report_assets/folder_structure.png")
os.makedirs("report_assets", exist_ok=True)

terminal.screenshot(out_png1)
terminal.screenshot(out_png2)

driver.quit()
print("Captured folder_structure.png successfully with all lines!")
