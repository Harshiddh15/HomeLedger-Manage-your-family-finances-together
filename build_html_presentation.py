import os

html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Family Finance Management System (HomeLedger) — Project Presentation</title>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    :root {
        --bg-dark: #0b111e;
        --card-bg: #121a2a;
        --card-border: #263652;
        --cyan: #00e5ff;
        --green: #00e676;
        --red: #ff5252;
        --amber: #ffb300;
        --purple: #7c4dff;
        --text-white: #f0f6fc;
        --text-muted: #8c96a2;
        --text-light-cyan: #b4f5ff;
        --font-mono: 'Consolas', 'JetBrains Mono', 'Courier New', monospace;
        --font-sans: 'Segoe UI', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
        user-select: none;
    }

    body {
        background: var(--bg-dark);
        color: var(--text-white);
        font-family: var(--font-sans);
        overflow: hidden;
        height: 100vh;
        width: 100vw;
        display: flex;
        flex-direction: column;
    }

    /* Top Progress & Status Bar */
    .top-bar {
        height: 48px;
        background: rgba(14, 21, 35, 0.95);
        border-bottom: 1px solid var(--card-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 28px;
        z-index: 100;
    }

    .project-tag {
        font-family: var(--font-mono);
        font-size: 13px;
        font-weight: 700;
        color: var(--cyan);
        letter-spacing: 1px;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .progress-track {
        flex: 1;
        max-width: 450px;
        height: 4px;
        background: rgba(255, 255, 255, 0.1);
        border-radius: 2px;
        margin: 0 24px;
        overflow: hidden;
    }

    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, var(--cyan), var(--green));
        width: 7.14%;
        transition: width 0.4s ease;
    }

    .slide-counter {
        font-family: var(--font-mono);
        font-size: 13px;
        color: var(--text-muted);
    }

    /* Deck Viewport */
    .deck-container {
        flex: 1;
        position: relative;
        overflow: hidden;
        perspective: 1200px;
    }

    .slide {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        padding: 24px 44px 75px 44px;
        display: flex;
        flex-direction: column;
        opacity: 0;
        visibility: hidden;
        transform: scale(0.96) translateY(20px);
        transition: all 0.45s cubic-bezier(0.25, 1, 0.5, 1);
        overflow-y: auto;
    }

    .slide.active {
        opacity: 1;
        visibility: visible;
        transform: scale(1) translateY(0);
    }

    .slide.exit-left {
        opacity: 0;
        visibility: hidden;
        transform: scale(0.94) translateX(-50px);
    }

    /* Slide Header */
    .slide-header {
        margin-bottom: 18px;
        border-bottom: 2px solid var(--cyan);
        padding-bottom: 10px;
        position: relative;
    }

    .slide-category {
        font-family: var(--font-mono);
        font-size: 12px;
        font-weight: 700;
        color: var(--cyan);
        letter-spacing: 1.5px;
        margin-bottom: 3px;
    }

    .slide-title {
        font-size: 26px;
        font-weight: 700;
        color: var(--text-white);
        letter-spacing: 0.3px;
    }

    .slide-subtitle {
        font-size: 13.5px;
        color: var(--text-muted);
        font-style: italic;
        margin-top: 4px;
    }

    /* Card Utilities */
    .card {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        border-radius: 8px;
        padding: 20px;
        position: relative;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }

    .card:hover {
        border-color: var(--cyan);
        transform: translateY(-2px);
    }

    .card-cyan { border-color: var(--cyan); }
    .card-green { border-color: var(--green); }
    .card-red { border-color: var(--red); }
    .card-amber { border-color: var(--amber); }
    .card-purple { border-color: var(--purple); }

    .tag-badge {
        font-family: var(--font-mono);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 6px;
        display: inline-block;
    }

    .headline {
        font-size: 15px;
        font-weight: 700;
        color: var(--text-white);
        margin-bottom: 10px;
    }

    .bullet-list {
        list-style: none;
        display: flex;
        flex-direction: column;
        gap: 8px;
    }

    .bullet-list li {
        font-size: 13px;
        color: var(--text-muted);
        line-height: 1.5;
        position: relative;
        padding-left: 16px;
    }

    .bullet-list li::before {
        content: "•";
        position: absolute;
        left: 0;
        color: var(--cyan);
        font-weight: bold;
    }

    .grid-2 {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
    }

    .grid-3 {
        display: grid;
        grid-template-columns: 1fr 1fr 1fr;
        gap: 20px;
    }

    .grid-4 {
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 18px;
    }

    /* Screenshot presentation */
    .shot-frame {
        background: #000;
        border: 1px solid var(--card-border);
        border-radius: 6px;
        overflow: hidden;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
        display: flex;
        flex-direction: column;
    }

    .shot-frame img {
        width: 100%;
        height: auto;
        display: block;
        border-radius: 6px 6px 0 0;
    }

    /* Bottom Control Bar */
    .nav-bar {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        height: 52px;
        background: rgba(11, 17, 30, 0.95);
        border-top: 1px solid var(--card-border);
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
        z-index: 100;
        backdrop-filter: blur(8px);
    }

    .nav-btn {
        background: var(--card-bg);
        border: 1px solid var(--card-border);
        color: var(--text-white);
        font-family: var(--font-sans);
        font-size: 13px;
        font-weight: 600;
        padding: 7px 16px;
        border-radius: 6px;
        cursor: pointer;
        display: flex;
        align-items: center;
        gap: 8px;
        transition: all 0.2s ease;
    }

    .nav-btn:hover {
        background: var(--cyan);
        color: #000;
        border-color: var(--cyan);
    }

    .keys-hint {
        font-family: var(--font-mono);
        font-size: 12px;
        color: var(--text-muted);
        display: flex;
        gap: 16px;
    }

    .kbd {
        background: rgba(255, 255, 255, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.2);
        color: var(--cyan);
    }

    /* Custom Scrollbar */
    ::-webkit-scrollbar { width: 6px; height: 6px; }
    ::-webkit-scrollbar-track { background: var(--bg-dark); }
    ::-webkit-scrollbar-thumb { background: var(--card-border); border-radius: 3px; }
    ::-webkit-scrollbar-thumb:hover { background: var(--cyan); }
</style>
</head>
<body>

<!-- Top HUD Bar -->
<div class="top-bar">
    <div class="project-tag">
        <i class="fa-solid fa-layer-group"></i>
        <span>HOMELEDGER // PROJECT PRESENTATION</span>
    </div>
    <div class="progress-track">
        <div class="progress-fill" id="progressFill"></div>
    </div>
    <div class="slide-counter" id="slideCounter">SLIDE 01 / 14</div>
</div>

<!-- Slide Container -->
<div class="deck-container">

    <!-- ========================================== -->
    <!-- SLIDE 0: TITLE & ARCHITECTURE OVERVIEW -->
    <!-- ========================================== -->
    <div class="slide active">
        <div class="card card-cyan" style="height: 100%; display: flex; flex-direction: column; justify-content: space-between; padding: 32px 40px;">
            <div style="display: flex; justify-content: space-between; align-items: flex-start;">
                <div>
                    <div style="font-family: var(--font-mono); font-size: 12px; color: var(--cyan); font-weight: 700; letter-spacing: 1.5px; margin-bottom: 8px;">
                        CORE TECHNOLOGIES USED
                    </div>
                    <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-muted); line-height: 1.8;">
                        • Framework:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: var(--text-white);">ASP.NET Core 10.0 MVC (C#)</strong><br>
                        • Database:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: var(--text-white);">MySQL Server (Port 3306)</strong><br>
                        • ORM Tool:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: var(--text-white);">Entity Framework Core 9.0</strong><br>
                        • Security:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: var(--text-white);">BCrypt Password Hashing & Role Login</strong><br>
                        • Reports:&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<strong style="color: var(--text-white);">QuestPDF (PDF) & CSV Export</strong><br>
                        • User Interface:&nbsp;&nbsp;<strong style="color: var(--text-white);">Modern Responsive Theme (Bootstrap 5.3)</strong>
                    </div>
                </div>
                <div style="display: flex; flex-direction: column; align-items: flex-end; gap: 12px;">
                    <div style="display: flex; gap: 16px; align-items: center;">
                        <img src="report_assets/image1.png" alt="Navgujarat College Logo" style="height: 60px; object-fit: contain;">
                        <img src="report_assets/image2.jpeg" alt="Gujarat University Logo" style="height: 60px; object-fit: contain; border-radius: 4px;">
                    </div>
                    <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700; letter-spacing: 1px;">
                        ACADEMIC YEAR • 2026–2027
                    </div>
                </div>
            </div>

            <div style="text-align: center; margin: 24px 0; border-top: 1px solid var(--card-border); border-bottom: 1px solid var(--card-border); padding: 26px 0;">
                <h1 style="font-size: 46px; font-weight: 800; color: var(--cyan); letter-spacing: 1px; margin-bottom: 8px;">
                    HomeLedger
                </h1>
                <p style="font-size: 17px; color: var(--text-light-cyan); font-weight: 400;">
                    A Web Application for Managing Family Income, Expenses, and Savings Together
                </p>
            </div>

            <div class="card" style="background: rgba(14, 21, 35, 0.9); border-color: var(--card-border); padding: 18px 24px;">
                <div style="font-family: var(--font-mono); font-size: 11px; color: var(--amber); font-weight: 700; letter-spacing: 1.5px; margin-bottom: 8px;">
                    PROJECT PRESENTATION DETAILS
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; font-family: var(--font-mono); font-size: 12.5px; color: var(--text-white);">
                    <div>
                        <span style="color: var(--text-muted);">Presented By:</span> <strong>Harshiddh Rana</strong><br>
                        <span style="color: var(--text-muted);">Department:</span> BCA (Honours) Sem 7<br>
                        <span style="color: var(--text-muted);">Institution:</span> Navgujarat BCA College, Gandhinagar
                    </div>
                    <div>
                        <span style="color: var(--text-muted);">Project Guide:</span> <strong>Prof. Anjali Nimavat (Assistant Professor)</strong><br>
                        <span style="color: var(--text-muted);">In-Charge:</span> Prof. DevrajSinh Jadav (Principal In-Charge)<br>
                        <span style="color: var(--text-muted);">Affiliated To:</span> Gujarat University, Ahmedabad
                    </div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 1: 01 / HOUSEHOLD CHALLENGES -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">01 / HOUSEHOLD CHALLENGES</div>
            <div class="slide-title">Common Financial Problems in Families</div>
            <div class="slide-subtitle">Why managing family money is difficult without a centralized system:</div>
        </div>
        <div class="grid-3" style="flex: 1;">
            <div class="card card-red">
                <span class="tag-badge" style="color: var(--red);">[ 01 / SCATTERED MONEY ]</span>
                <div class="headline">Multiple Earners & No Common View</div>
                <ul class="bullet-list">
                    <li>Family members earn separately (jobs, business) but do not share one single dashboard.</li>
                    <li>Head of the family cannot see total money left at the end of the month.</li>
                    <li>Cash spending and online UPI payments easily get forgotten without daily tracking.</li>
                </ul>
            </div>
            <div class="card card-amber">
                <span class="tag-badge" style="color: var(--amber);">[ 02 / UNNOTICED OVERSPENDING ]</span>
                <div class="headline">No Budget Limits or Warnings</div>
                <ul class="bullet-list">
                    <li>Daily expenses (groceries, bills, shopping) happen without monthly category limits.</li>
                    <li>Families only realize they overspent after their bank balance is almost finished.</li>
                    <li>No visual warning bars to alert family members when limits are reached.</li>
                </ul>
            </div>
            <div class="card card-cyan">
                <span class="tag-badge" style="color: var(--cyan);">[ 03 / LOANS & UDHAR ]</span>
                <div class="headline">Forgotten Loans & Unclear Records</div>
                <ul class="bullet-list">
                    <li>Money given to friends ('Lene Hai') or borrowed ('Dene Hai') is kept in diary or memory.</li>
                    <li>Partial repayments are easily forgotten, creating confusion and awkward disputes.</li>
                    <li>No proof or history of who paid how much and on what date.</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 2: 02 / THE HOMELEDGER PARADIGM -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">02 / THE HOMELEDGER PARADIGM</div>
            <div class="slide-title">The Solution: What is HomeLedger?</div>
            <div class="slide-subtitle">One simple website to track all family income, expenses, and debts in one place.</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1.4fr; gap: 24px; flex: 1;">
            <div class="card card-cyan" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--cyan);">MAIN HIGHLIGHTS</span>
                    <div class="headline" style="font-size: 18px; margin-bottom: 12px;">Built for Indian Families</div>
                    <p style="font-size: 13.5px; color: var(--text-muted); line-height: 1.6; margin-bottom: 20px;">
                        HomeLedger replaces messy diaries and scattered excel sheets with a clean, easy-to-use website. It brings all earning family members together to record transactions, sets monthly budget limits, tracks informal loans (Udhar), and keeps data safe with simple 1-click backups.
                    </p>
                </div>
                <div style="display: flex; flex-direction: column; gap: 12px;">
                    <div style="font-family: var(--font-mono); font-size: 13px; color: var(--green);">
                        <strong>★ 100%</strong> — <span style="color: var(--text-white);">Full Visibility of Family Money</span>
                    </div>
                    <div style="font-family: var(--font-mono); font-size: 13px; color: var(--green);">
                        <strong>★ 14</strong> — <span style="color: var(--text-white);">Easy and Useful Modules</span>
                    </div>
                    <div style="font-family: var(--font-mono); font-size: 13px; color: var(--green);">
                        <strong>★ 0-Loss</strong> — <span style="color: var(--text-white);">Safe JSON Database Backup & Restore</span>
                    </div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 16px;">
                <div class="card card-cyan">
                    <span class="tag-badge" style="color: var(--cyan);">[ FAMILY COLLABORATION ]</span>
                    <div class="headline">Multi-User Family Access</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Admin (Head of Family) manages budgets and members. Other family members log their own daily expenses and earnings.
                    </p>
                </div>
                <div class="card card-green">
                    <span class="tag-badge" style="color: var(--green);">[ AUTOMATED BILLS ]</span>
                    <div class="headline">Fixed Incomes & Monthly Bills</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Automatically adds monthly salary and regular bills (like WiFi, electricity, tuition fees) on their set due dates.
                    </p>
                </div>
                <div class="card card-amber">
                    <span class="tag-badge" style="color: var(--amber);">[ UDHAR TRACKER ]</span>
                    <div class="headline">Simple Loan & Debt Tracker</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Clear tracking of money given to others ('Lene Hai') and money borrowed ('Dene Hai') with payment history and proofs.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 3: 03 / OBJECTIVES & SCOPE -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">03 / OBJECTIVES & SCOPE</div>
            <div class="slide-title">Main Objectives of the Project</div>
            <div class="slide-subtitle">What we want to achieve with this system:</div>
        </div>
        <div class="grid-2" style="flex: 1;">
            <div class="card card-cyan">
                <span class="tag-badge" style="color: var(--cyan);">[ GOAL 01 ]</span>
                <div class="headline" style="font-size: 17px;">All Family Money in One Place</div>
                <p style="font-size: 13.5px; color: var(--text-muted); line-height: 1.6;">
                    Combine different bank accounts, cash, and incomes into a single simple dashboard so everyone knows the total balance.
                </p>
            </div>
            <div class="card card-green">
                <span class="tag-badge" style="color: var(--green);">[ GOAL 02 ]</span>
                <div class="headline" style="font-size: 17px;">Control Monthly Expenses</div>
                <p style="font-size: 13.5px; color: var(--text-muted); line-height: 1.6;">
                    Set monthly spending limits for categories like Food, Utilities, and Shopping with progress bars to stop overspending.
                </p>
            </div>
            <div class="card card-amber">
                <span class="tag-badge" style="color: var(--amber);">[ GOAL 03 ]</span>
                <div class="headline" style="font-size: 17px;">Track Loans and Udhar Easily</div>
                <p style="font-size: 13.5px; color: var(--text-muted); line-height: 1.6;">
                    Keep clear records of money borrowed or lent with person name, dates, notes, and partial payments history.
                </p>
            </div>
            <div class="card card-purple">
                <span class="tag-badge" style="color: var(--purple);">[ GOAL 04 ]</span>
                <div class="headline" style="font-size: 17px;">Easy Reports & Safe Backups</div>
                <p style="font-size: 13.5px; color: var(--text-muted); line-height: 1.6;">
                    Download clean PDF and CSV reports for any month, and backup all family data with a single click.
                </p>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 4: 04 / ARCHITECTURE & STACK -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">04 / ARCHITECTURE & STACK</div>
            <div class="slide-title">System Architecture (3-Tier MVC Design)</div>
            <div class="slide-subtitle">How the system is structured using standard 3-tier MVC architecture:</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 16px; flex: 1;">
            <div class="card card-cyan">
                <span class="tag-badge" style="color: var(--cyan);">[ 1. USER INTERFACE TIER ] • Frontend (What the User Sees)</span>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px; font-size: 13px;">
                    <div><strong style="color: var(--text-white);">• Technologies:</strong> <span style="color: var(--text-muted);">Razor Views (.cshtml), HTML5, CSS3, JavaScript, jQuery</span></div>
                    <div><strong style="color: var(--text-white);">• Styling:</strong> <span style="color: var(--text-muted);">Bootstrap 5.3 framework with custom dark theme</span></div>
                    <div><strong style="color: var(--text-white);">• Responsiveness:</strong> <span style="color: var(--text-muted);">Works smoothly on mobile phones, tablets, and desktop computers</span></div>
                    <div><strong style="color: var(--text-white);">• Interactivity:</strong> <span style="color: var(--text-muted);">Easy modals, quick search filters, and smooth buttons</span></div>
                </div>
            </div>
            <div class="card card-green">
                <span class="tag-badge" style="color: var(--green);">[ 2. BUSINESS LOGIC TIER ] • Backend C# Controllers & Business Rules</span>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px; font-size: 13px;">
                    <div><strong style="color: var(--text-white);">• Core Logic:</strong> <span style="color: var(--text-muted);">Controllers handle Income, Expenses, Budgets, Loans, and Reports</span></div>
                    <div><strong style="color: var(--text-white);">• Calculations:</strong> <span style="color: var(--text-muted);">Calculates real-time balances and checks if monthly budget limits are crossed</span></div>
                    <div><strong style="color: var(--text-white);">• User Security:</strong> <span style="color: var(--text-muted);">BCrypt password hashing and Anti-Forgery tokens protect against attacks</span></div>
                    <div><strong style="color: var(--text-white);">• Clean Code:</strong> <span style="color: var(--text-muted);">Follows Model-View-Controller (MVC) and Dependency Injection design</span></div>
                </div>
            </div>
            <div class="card card-purple">
                <span class="tag-badge" style="color: var(--purple);">[ 3. DATABASE TIER ] • Data Storage & Backup Engine</span>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 12px; margin-top: 8px; font-size: 13px;">
                    <div><strong style="color: var(--text-white);">• Database:</strong> <span style="color: var(--text-muted);">MySQL Server (Port 3306) with 11 relational tables</span></div>
                    <div><strong style="color: var(--text-white);">• ORM Tool:</strong> <span style="color: var(--text-muted);">Entity Framework Core (Pomelo) for easy database operations in C#</span></div>
                    <div><strong style="color: var(--text-white);">• Session State:</strong> <span style="color: var(--text-muted);">Encrypted session cookies keep user logged in securely</span></div>
                    <div><strong style="color: var(--text-white);">• Backup Engine:</strong> <span style="color: var(--text-muted);">Exports all database tables into a single JSON file for safe recovery</span></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 5: 05 / FUNCTIONAL MODULES -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">05 / FUNCTIONAL MODULES</div>
            <div class="slide-title">Core System Modules Overview (14 Modules)</div>
            <div class="slide-subtitle">Complete list of all 14 features developed in this project:</div>
        </div>
        <div class="grid-2" style="gap: 12px; flex: 1;">
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--cyan); margin-bottom: 2px;">[ MODULE M1 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">User Login & Roles:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Secure login for Admin and Family Members using BCrypt hashing.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--green); margin-bottom: 2px;">[ MODULE M2 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Main Dashboard:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Shows total balance, income, expenses, and loans at a glance.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--amber); margin-bottom: 2px;">[ MODULE M3 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Family Members:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Add and manage family members with relationships (Head, Wife, Son).</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--purple); margin-bottom: 2px;">[ MODULE M4 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Income Management:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Record salary, rental income, and gifts with PDF and CSV export.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--red); margin-bottom: 2px;">[ MODULE M5 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Expense Tracking:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Record daily expenses with category, date, and receipt notes.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--cyan); margin-bottom: 2px;">[ MODULE M6 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Categories:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Custom categories with colors and icons for easy sorting.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--green); margin-bottom: 2px;">[ MODULE M7 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Monthly Budgets:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Set spending limits with progress bars to prevent overspending.</span>
                </div>
            </div>
            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--amber); margin-bottom: 2px;">[ MODULE M8 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Recurring Incomes:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Automatically adds fixed incomes like monthly salary on set days.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--red); margin-bottom: 2px;">[ MODULE M9 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Recurring Bills:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Automatically tracks regular bills like WiFi, electricity, tuition fees.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--purple); margin-bottom: 2px;">[ MODULE M10 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Savings Goals:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Set target amounts like Emergency Fund or Vacation with progress %.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--cyan); margin-bottom: 2px;">[ MODULE M11 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Udhar (Debt) Ledger:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Track 'Lene Hai' and 'Dene Hai' with partial payments.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--green); margin-bottom: 2px;">[ MODULE M12 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Bill Reminders:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Alerts for upcoming due dates so late payment penalties are avoided.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--amber); margin-bottom: 2px;">[ MODULE M13 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Reports & Analysis:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Monthly breakdown charts and annual cashflow summaries.</span>
                </div>
                <div class="card" style="padding: 10px 14px;">
                    <span class="tag-badge" style="color: var(--purple); margin-bottom: 2px;">[ MODULE M14 ]</span>
                    <strong style="color: var(--text-white); font-size: 13px;">Database Backup:</strong>
                    <span style="color: var(--text-muted); font-size: 12.5px;">Single-click JSON backup and instant restore feature.</span>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 6: 06 / MULTI-MEMBER ROLES & SECURITY -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">06 / MULTI-MEMBER ROLES & SECURITY</div>
            <div class="slide-title">Multi-User Access & Security Steps</div>
            <div class="slide-subtitle">How family members use the system safely and privately:</div>
        </div>
        <div class="grid-4" style="flex: 1;">
            <div class="card card-cyan" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--cyan);">[ STEP 01 ]</span>
                    <div class="headline">Family Registration</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        The head of the family creates an account with Family Name, a unique Family ID, and master password.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700;">
                    ✔ Outcome: Family Account Ready
                </div>
            </div>
            <div class="card card-green" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--green);">[ STEP 02 ]</span>
                    <div class="headline">Add Family Members</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        The Admin adds other family members (Self, Wife, Son, Daughter) with their names and contact details.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700;">
                    ✔ Outcome: Profiles Created
                </div>
            </div>
            <div class="card card-amber" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--amber);">[ STEP 03 ]</span>
                    <div class="headline">Separate Logins</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Admin logs in for full control; other family members log in to record their individual expenses and earnings.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700;">
                    ✔ Outcome: Organized & Private
                </div>
            </div>
            <div class="card card-purple" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--purple);">[ STEP 04 ]</span>
                    <div class="headline">Password Safety</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Passwords are securely encrypted with BCrypt; session cookies keep user data protected at all times.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700;">
                    ✔ Outcome: 100% Safe Data
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 7: 07 / BUDGET & CASHFLOW ENGINE -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">07 / BUDGET & CASHFLOW ENGINE</div>
            <div class="slide-title">Smart Budgeting & Automated Bills</div>
            <div class="slide-subtitle">Helping families save money and pay bills on time:</div>
        </div>
        <div class="grid-3" style="flex: 1;">
            <div class="card card-cyan">
                <span class="tag-badge" style="color: var(--cyan);">[ AUTOMATIC INCOMES & BILLS ]</span>
                <div class="headline">Recurring Transactions</div>
                <ul class="bullet-list">
                    <li>Automatically records monthly salary on payment day without manual typing.</li>
                    <li>Sets reminders and records regular bills like WiFi, electricity, and school fees.</li>
                    <li>Saves time and prevents missing payment deadlines.</li>
                </ul>
            </div>
            <div class="card card-green">
                <span class="tag-badge" style="color: var(--green);">[ MONTHLY BUDGET LIMITS ]</span>
                <div class="headline">Category Spending Caps</div>
                <ul class="bullet-list">
                    <li>Set monthly spending limits for each category (e.g. Groceries ₹10,000, Dining ₹3,000).</li>
                    <li>Color-coded progress bars show how much budget has been used so far.</li>
                    <li>Gives clear visual warning before a family member exceeds the limit.</li>
                </ul>
            </div>
            <div class="card card-purple">
                <span class="tag-badge" style="color: var(--purple);">[ SAVINGS GOALS ]</span>
                <div class="headline">Saving for Future Targets</div>
                <ul class="bullet-list">
                    <li>Create goals like 'Emergency Fund' or 'New Vehicle'.</li>
                    <li>Displays clear progress bar showing how much is saved and how much is left.</li>
                    <li>Encourages family members to save money together for big milestones.</li>
                </ul>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 8: 08 / BILATERAL UDHAR & DEBT WORKFLOW -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">08 / BILATERAL UDHAR & DEBT WORKFLOW</div>
            <div class="slide-title">Udhar (Loan) Management Workflow</div>
            <div class="slide-subtitle">A simple 4-step process to track money given to or borrowed from others:</div>
        </div>
        <div class="grid-4" style="flex: 1;">
            <div class="card card-amber" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--amber);">[ STEP 1 ]</span>
                    <div class="headline">Add Loan Entry</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Enter the person's name, choose 'Lene Hai' (Receivable) or 'Dene Hai' (Payable), and enter the amount.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 11.5px; color: var(--amber); font-weight: 700;">
                    ✔ Status: Loan Recorded
                </div>
            </div>
            <div class="card card-cyan" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--cyan);">[ STEP 2 ]</span>
                    <div class="headline">Add Notes & Proof</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Write the reason for the loan (e.g. medical emergency) and optionally upload receipt image.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 11.5px; color: var(--cyan); font-weight: 700;">
                    ✔ Status: Proof Attached
                </div>
            </div>
            <div class="card card-green" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--green);">[ STEP 3 ]</span>
                    <div class="headline">Record Repayments</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Easily record partial payments whenever money is returned; remaining balance updates automatically.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 11.5px; color: var(--green); font-weight: 700;">
                    ✔ Status: Balance Updated
                </div>
            </div>
            <div class="card card-purple" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--purple);">[ STEP 4 ]</span>
                    <div class="headline">Mark Completed</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        When the remaining amount reaches ₹0, the loan status automatically changes from 'Pending' to 'Completed'.
                    </p>
                </div>
                <div style="font-family: var(--font-mono); font-size: 11.5px; color: var(--purple); font-weight: 700;">
                    ✔ Status: Fully Settled
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 9: 09 / OPERATIONAL INTERFACE (DASHBOARD & INCOME) -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">09 / OPERATIONAL INTERFACE</div>
            <div class="slide-title">System Screenshots: Dashboard & Income</div>
            <div class="slide-subtitle">Modern dark user interface designed for easy everyday use:</div>
        </div>
        <div class="grid-2" style="flex: 1;">
            <div class="card card-cyan" style="padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
                <div class="shot-frame">
                    <img src="report_assets/screenshots/05_dashboard.png" alt="Main Financial Dashboard">
                </div>
                <div style="margin-top: 12px;">
                    <div style="font-family: var(--font-mono); font-size: 12px; color: var(--cyan); font-weight: 700; margin-bottom: 4px;">
                        FIGURE 9.1: MAIN FINANCIAL DASHBOARD
                    </div>
                    <p style="font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
                        Displays 5 summary cards: Current Balance, Total Income, Total Expenses, Money to Receive, and Money to Pay, along with recent activity stream.
                    </p>
                </div>
            </div>
            <div class="card card-green" style="padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
                <div class="shot-frame">
                    <img src="report_assets/screenshots/06_income_list.png" alt="Income Management Page">
                </div>
                <div style="margin-top: 12px;">
                    <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700; margin-bottom: 4px;">
                        FIGURE 9.2: INCOME MANAGEMENT PAGE
                    </div>
                    <p style="font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
                        Clean table showing all income records with member name, search filter, and quick buttons to export PDF and CSV reports.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 10: 10 / OPERATIONAL INTERFACE (EXPENSE & UDHAR) -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">10 / OPERATIONAL INTERFACE</div>
            <div class="slide-title">System Screenshots: Expenses & Udhar</div>
            <div class="slide-subtitle">Clear screens for tracking daily spending and friendly loans:</div>
        </div>
        <div class="grid-2" style="flex: 1;">
            <div class="card card-red" style="padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
                <div class="shot-frame">
                    <img src="report_assets/screenshots/08_expense_list.png" alt="Expense Tracking Page">
                </div>
                <div style="margin-top: 12px;">
                    <div style="font-family: var(--font-mono); font-size: 12px; color: var(--red); font-weight: 700; margin-bottom: 4px;">
                        FIGURE 10.1: EXPENSE TRACKING PAGE
                    </div>
                    <p style="font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
                        Lists all daily expenses with category badges, notes, and instant balance updates when a new expense is saved.
                    </p>
                </div>
            </div>
            <div class="card card-amber" style="padding: 16px; display: flex; flex-direction: column; justify-content: space-between;">
                <div class="shot-frame">
                    <img src="report_assets/screenshots/20_udhar_list.png" alt="Udhar (Loan) Ledger Page">
                </div>
                <div style="margin-top: 12px;">
                    <div style="font-family: var(--font-mono); font-size: 12px; color: var(--amber); font-weight: 700; margin-bottom: 4px;">
                        FIGURE 10.2: UDHAR (LOAN) LEDGER PAGE
                    </div>
                    <p style="font-size: 12.5px; color: var(--text-muted); line-height: 1.5;">
                        Shows pending loans with clear green and red badges for 'Lene Hai' vs 'Dene Hai' and remaining amounts.
                    </p>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 11: 11 / EVALUATION & FEASIBILITY -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">11 / EVALUATION & FEASIBILITY</div>
            <div class="slide-title">Feasibility Study & Current Limitations</div>
            <div class="slide-subtitle">Why this project is practical and areas for future improvement:</div>
        </div>
        <div style="display: flex; flex-direction: column; gap: 18px; flex: 1;">
            <div class="card card-green">
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--green); font-weight: 700; letter-spacing: 1px; margin-bottom: 8px;">
                    FEASIBILITY STUDY VALIDATION
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
                    <div><strong style="color: var(--text-white);">✔ Technical Feasibility:</strong> <span style="color: var(--text-muted);">Built with ASP.NET Core MVC and MySQL. Runs fast, reliable, and error-free on any Windows or Linux computer.</span></div>
                    <div><strong style="color: var(--text-white);">✔ Economic Feasibility:</strong> <span style="color: var(--text-muted);">Zero licensing costs because only open-source software (Free .NET SDK, MySQL Community) is used. Saves money for families.</span></div>
                    <div><strong style="color: var(--text-white);">✔ Operational Feasibility:</strong> <span style="color: var(--text-muted);">Very simple user interface that any family member can learn to use in just 5 minutes without any special training.</span></div>
                </div>
            </div>
            <div class="card card-red">
                <div style="font-family: var(--font-mono); font-size: 12px; color: var(--red); font-weight: 700; letter-spacing: 1px; margin-bottom: 8px;">
                    CURRENT PROJECT LIMITATIONS
                </div>
                <div style="display: flex; flex-direction: column; gap: 8px; font-size: 13px;">
                    <div><strong style="color: var(--text-white);">⚠ Manual Bank Entry:</strong> <span style="color: var(--text-muted);">Users enter transactions manually. Direct bank API link is not connected yet to keep it simple and free.</span></div>
                    <div><strong style="color: var(--text-white);">⚠ Single Currency (INR):</strong> <span style="color: var(--text-muted);">System currently works with Indian Rupees (₹); foreign currency conversion can be added in future versions.</span></div>
                    <div><strong style="color: var(--text-white);">⚠ Requires Server Connection:</strong> <span style="color: var(--text-muted);">Must be opened through browser connected to the local or cloud web server.</span></div>
                    <div><strong style="color: var(--text-white);">⚠ Photo Proofs are Manual:</strong> <span style="color: var(--text-muted);">Receipts are uploaded as images; automated receipt text scanner (OCR) is planned for next update.</span></div>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 12: 12 / STRATEGIC ROADMAP -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">12 / STRATEGIC ROADMAP</div>
            <div class="slide-title">Future Scope & Enhancements</div>
            <div class="slide-subtitle">Features planned to make HomeLedger even more powerful in future versions:</div>
        </div>
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px; flex: 1;">
            <div class="card card-cyan" style="display: flex; flex-direction: column; justify-content: space-between;">
                <div>
                    <span class="tag-badge" style="color: var(--cyan);">🌟 MAIN FUTURE FEATURE</span>
                    <div class="headline" style="font-size: 18px; margin-bottom: 14px;">AI Financial Assistant & Spend Prediction</div>
                    <div style="display: flex; flex-direction: column; gap: 12px; font-size: 13px;">
                        <div>
                            <strong style="color: var(--text-white);">• Balance Prediction:</strong>
                            <p style="color: var(--text-muted); margin-top: 2px;">Predicts how much money will remain at month-end based on past spending habits.</p>
                        </div>
                        <div>
                            <strong style="color: var(--text-white);">• Spending Alerts:</strong>
                            <p style="color: var(--text-muted); margin-top: 2px;">Automatically alerts if extra money is being spent on shopping or food.</p>
                        </div>
                        <div>
                            <strong style="color: var(--text-white);">• Smart Saving Tips:</strong>
                            <p style="color: var(--text-muted); margin-top: 2px;">Gives useful suggestions to help the family save an extra 10% to 20% every month.</p>
                        </div>
                    </div>
                </div>
            </div>

            <div style="display: flex; flex-direction: column; gap: 10px;">
                <div class="card card-green" style="padding: 12px 16px;">
                    <span class="tag-badge" style="color: var(--green); margin-bottom: 2px;">[ MOBILE APP ]</span>
                    <div class="headline" style="font-size: 13px; margin-bottom: 2px;">Android & iOS App</div>
                    <p style="font-size: 12px; color: var(--text-muted);">Dedicated mobile app for quick expense logging on smartphones.</p>
                </div>
                <div class="card card-amber" style="padding: 12px 16px;">
                    <span class="tag-badge" style="color: var(--amber); margin-bottom: 2px;">[ BANK & UPI SYNC ]</span>
                    <div class="headline" style="font-size: 13px; margin-bottom: 2px;">Direct Bank Account Sync</div>
                    <p style="font-size: 12px; color: var(--text-muted);">Connect directly with UPI and bank statements for automatic data entry.</p>
                </div>
                <div class="card card-purple" style="padding: 12px 16px;">
                    <span class="tag-badge" style="color: var(--purple); margin-bottom: 2px;">[ BILL SCANNER ]</span>
                    <div class="headline" style="font-size: 13px; margin-bottom: 2px;">Smart Receipt Scanner (OCR)</div>
                    <p style="font-size: 12px; color: var(--text-muted);">Take a photo of grocery bill and let system read the amount automatically.</p>
                </div>
                <div class="card card-cyan" style="padding: 12px 16px;">
                    <span class="tag-badge" style="color: var(--cyan); margin-bottom: 2px;">[ WHATSAPP ALERTS ]</span>
                    <div class="headline" style="font-size: 13px; margin-bottom: 2px;">WhatsApp Bill Reminders</div>
                    <p style="font-size: 12px; color: var(--text-muted);">Send bill payment reminders and budget warnings directly on WhatsApp.</p>
                </div>
            </div>
        </div>
    </div>

    <!-- ========================================== -->
    <!-- SLIDE 13: 13 / SUMMARY & CONCLUSION -->
    <!-- ========================================== -->
    <div class="slide">
        <div class="slide-header">
            <div class="slide-category">13 / SUMMARY & CONCLUSION</div>
            <div class="slide-title">Summary & Conclusion</div>
            <div class="slide-subtitle">How HomeLedger helps modern families achieve financial peace of mind:</div>
        </div>
        <div style="display: flex; flex-direction: column; justify-content: space-between; flex: 1;">
            <div class="grid-3">
                <div class="card card-cyan">
                    <span class="tag-badge" style="color: var(--cyan);">[ BETTER SAVINGS ]</span>
                    <div class="headline">Smart Money Habits</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Helps families save regularly by setting clear budgets and cutting down unnecessary expenses.
                    </p>
                </div>
                <div class="card card-green">
                    <span class="tag-badge" style="color: var(--green);">[ NO CONFUSION ]</span>
                    <div class="headline">Peaceful Family Finances</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Multi-member logins and clear loan tracking remove arguments about who spent what and who owes money.
                    </p>
                </div>
                <div class="card card-purple">
                    <span class="tag-badge" style="color: var(--purple);">[ SAFE & RELIABLE ]</span>
                    <div class="headline">Never Lose Financial Data</div>
                    <p style="font-size: 13px; color: var(--text-muted); line-height: 1.5;">
                        Built on solid .NET architecture with easy 1-click database backups to keep family records safe forever.
                    </p>
                </div>
            </div>

            <div class="card card-cyan" style="background: rgba(14, 21, 35, 0.95); text-align: center; padding: 22px; margin-top: 18px;">
                <h2 style="font-size: 26px; font-weight: 800; color: var(--cyan); letter-spacing: 1px; margin-bottom: 8px;">
                    THANK YOU • QUESTIONS & DISCUSSION
                </h2>
                <div style="font-family: var(--font-mono); font-size: 13px; color: var(--text-white); line-height: 1.6;">
                    Family Finance Management System (HomeLedger) | ASP.NET Core 10.0 MVC | MySQL<br>
                    Presented By: <strong>Harshiddh Rana</strong> | Project Guide: <strong>Prof. Anjali Nimavat</strong> | Navgujarat BCA College, Gandhinagar
                </div>
            </div>
        </div>
    </div>

</div>

<!-- Bottom Navigation Bar -->
<div class="nav-bar">
    <div style="display: flex; gap: 12px;">
        <button class="nav-btn" onclick="prevSlide()"><i class="fa-solid fa-arrow-left"></i> Previous</button>
        <button class="nav-btn" onclick="nextSlide()">Next <i class="fa-solid fa-arrow-right"></i></button>
    </div>

    <div class="keys-hint">
        <span><span class="kbd">←</span> / <span class="kbd">→</span> or <span class="kbd">SPACE</span> to Navigate</span>
        <span><span class="kbd">F</span> Fullscreen</span>
    </div>

    <div>
        <button class="nav-btn" onclick="toggleFullscreen()"><i class="fa-solid fa-expand"></i> Fullscreen</button>
    </div>
</div>

<script>
    let currentSlide = 1;
    const totalSlides = 14;

    function updateSlide() {
        document.querySelectorAll('.slide').forEach((slide, idx) => {
            slide.classList.remove('active', 'exit-left');
            if (idx + 1 === currentSlide) {
                slide.classList.add('active');
            } else if (idx + 1 < currentSlide) {
                slide.classList.add('exit-left');
            }
        });

        // Update progress bar
        const progressPercent = (currentSlide / totalSlides) * 100;
        document.getElementById('progressFill').style.width = progressPercent + '%';

        // Update counter
        const pad = (n) => n < 10 ? '0' + n : n;
        document.getElementById('slideCounter').innerText = `SLIDE ${pad(currentSlide)} / ${totalSlides}`;
    }

    function nextSlide() {
        if (currentSlide < totalSlides) {
            currentSlide++;
            updateSlide();
        }
    }

    function prevSlide() {
        if (currentSlide > 1) {
            currentSlide--;
            updateSlide();
        }
    }

    // Keyboard navigation
    document.addEventListener('keydown', (e) => {
        if (e.key === 'ArrowRight' || e.key === ' ' || e.key === 'PageDown') {
            nextSlide();
        } else if (e.key === 'ArrowLeft' || e.key === 'PageUp') {
            prevSlide();
        } else if (e.key === 'f' || e.key === 'F') {
            toggleFullscreen();
        }
    });

    function toggleFullscreen() {
        if (!document.fullscreenElement) {
            document.documentElement.requestFullscreen().catch(() => {});
        } else {
            if (document.exitFullscreen) {
                document.exitFullscreen();
            }
        }
    }
</script>

</body>
</html>
'''

with open(r"c:\Users\Rana Harshiddh\Desktop\Family-Finance-Management-main\Family_Finance_Management_Presentation.html", "w", encoding="utf-8") as f:
    f.write(html_content)

print("Simplified Family_Finance_Management_Presentation.html created successfully!")
