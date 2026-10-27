import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml

def create_deck():
    prs = pptx.Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Theme colors matching modern dark HUD style
    BG_DARK = RGBColor(11, 17, 30)          # #0B111E
    CARD_BG = RGBColor(18, 26, 42)          # #121A2A
    CARD_BORDER = RGBColor(38, 54, 82)      # #263652
    CYAN_ACCENT = RGBColor(0, 229, 255)     # #00E5FF
    GREEN_ACCENT = RGBColor(0, 230, 118)    # #00E676
    RED_ACCENT = RGBColor(255, 82, 82)      # #FF5252
    AMBER_ACCENT = RGBColor(255, 179, 0)    # #FFB300
    PURPLE_ACCENT = RGBColor(124, 77, 255)  # #7C4DFF
    TEXT_WHITE = RGBColor(240, 246, 252)    # #F0F6FC
    TEXT_MUTED = RGBColor(140, 150, 162)    # #8C96A2
    TEXT_LIGHT_CYAN = RGBColor(180, 245, 255)

    def add_fade_transition(slide):
        xml = parse_xml(
            '<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="med">'
            '<p:fade/>'
            '</p:transition>'
        )
        slide._element.append(xml)

    def set_bg(slide):
        bg = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid()
        bg.fill.fore_color.rgb = BG_DARK
        bg.line.fill.background()
        return bg

    def add_header(slide, title, category_tag):
        # Category Tag
        tb_tag = slide.shapes.add_textbox(Inches(0.8), Inches(0.35), Inches(11.5), Inches(0.3))
        tf_t = tb_tag.text_frame
        tf_t.word_wrap = True
        tf_t.margin_left = tf_t.margin_top = tf_t.margin_right = tf_t.margin_bottom = 0
        p_t = tf_t.paragraphs[0]
        r_t = p_t.add_run()
        r_t.text = category_tag.upper()
        r_t.font.name = "Consolas"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = CYAN_ACCENT

        # Title
        tb_title = slide.shapes.add_textbox(Inches(0.8), Inches(0.65), Inches(11.5), Inches(0.55))
        tf = tb_title.text_frame
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title
        r.font.name = "Segoe UI"
        r.font.size = Pt(21)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        # Accent Line
        line = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), Inches(1.25), Inches(11.733), Inches(0.025))
        line.fill.solid()
        line.fill.fore_color.rgb = CYAN_ACCENT
        line.line.fill.background()

    def add_card(slide, left, top, width, height, bg_color=CARD_BG, border_color=CARD_BORDER, border_width=1):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        if border_color:
            card.line.color.rgb = border_color
            card.line.width = Pt(border_width)
        else:
            card.line.fill.background()
        return card

    # =========================================================================
    # SLIDE 0: TITLE & ARCHITECTURE SLIDE
    # =========================================================================
    s0 = prs.slides.add_slide(blank_layout)
    set_bg(s0)
    add_fade_transition(s0)

    # Master border box
    add_card(s0, Inches(0.8), Inches(0.6), Inches(11.733), Inches(6.3), bg_color=CARD_BG, border_color=CYAN_ACCENT, border_width=1.5)

    # Top Left: Core Tech Stack
    tb_arch = s0.shapes.add_textbox(Inches(1.2), Inches(0.9), Inches(6.0), Inches(2.2))
    tf_a = tb_arch.text_frame
    tf_a.word_wrap = True
    p = tf_a.paragraphs[0]
    r = p.add_run()
    r.text = "CORE TECHNOLOGIES USED\n"
    r.font.name = "Consolas"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = CYAN_ACCENT

    specs = (
        "• Framework:       ASP.NET Core 10.0 MVC (C#)\n"
        "• Database:        MySQL Server (Port 3306)\n"
        "• ORM Tool:        Entity Framework Core 9.0\n"
        "• Security:        BCrypt Password Hashing & Role Login\n"
        "• Reports:         QuestPDF (PDF) & CSV Export\n"
        "• User Interface:  Modern Responsive Theme (Bootstrap 5.3)"
    )
    p_sp = tf_a.add_paragraph()
    r_sp = p_sp.add_run()
    r_sp.text = specs
    r_sp.font.name = "Consolas"
    r_sp.font.size = Pt(10)
    r_sp.font.color.rgb = TEXT_WHITE

    # Top Right: Logos & Academic Year Tag
    if os.path.exists("report_assets/image1.png"):
        s0.shapes.add_picture("report_assets/image1.png", Inches(10.0), Inches(0.9), width=Inches(1.0))
    if os.path.exists("report_assets/image2.jpeg"):
        s0.shapes.add_picture("report_assets/image2.jpeg", Inches(11.2), Inches(0.9), width=Inches(0.95))

    tb_yr = s0.shapes.add_textbox(Inches(7.8), Inches(2.0), Inches(4.3), Inches(0.5))
    p_yr = tb_yr.text_frame.paragraphs[0]
    p_yr.alignment = PP_ALIGN.RIGHT
    r = p_yr.add_run()
    r.text = "ACADEMIC YEAR • 2026–2027"
    r.font.name = "Consolas"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = GREEN_ACCENT

    # Center Divider
    div = s0.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.2), Inches(3.2), Inches(10.933), Inches(0.02))
    div.fill.solid()
    div.fill.fore_color.rgb = CARD_BORDER
    div.line.fill.background()

    # Center: Title
    tb_title = s0.shapes.add_textbox(Inches(1.2), Inches(3.4), Inches(10.933), Inches(1.6))
    tf_t = tb_title.text_frame
    tf_t.word_wrap = True

    p = tf_t.paragraphs[0]
    r = p.add_run()
    r.text = "HomeLedger\n"
    r.font.name = "Segoe UI"
    r.font.size = Pt(36)
    r.font.bold = True
    r.font.color.rgb = CYAN_ACCENT

    p_sub = tf_t.add_paragraph()
    r_sub = p_sub.add_run()
    r_sub.text = "A Web Application for Managing Family Income, Expenses, and Savings Together"
    r_sub.font.name = "Segoe UI"
    r_sub.font.size = Pt(15)
    r_sub.font.color.rgb = TEXT_LIGHT_CYAN

    # Bottom: Project Presentation Details Card
    add_card(s0, Inches(1.2), Inches(5.1), Inches(10.933), Inches(1.5), bg_color=RGBColor(14, 21, 35), border_color=CARD_BORDER)
    tb_pres = s0.shapes.add_textbox(Inches(1.5), Inches(5.2), Inches(10.3), Inches(1.3))
    tf_p = tb_pres.text_frame
    tf_p.word_wrap = True
    
    p = tf_p.paragraphs[0]
    r = p.add_run()
    r.text = "PROJECT PRESENTATION DETAILS\n"
    r.font.name = "Consolas"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = AMBER_ACCENT

    p_info = tf_p.add_paragraph()
    r = p_info.add_run()
    r.text = (
        "Presented By:   Harshiddh Rana                                            Project Guide:  Prof. Anjali Nimavat (Assistant Professor)\n"
        "Department:     BCA (Honours) Sem 7                                       In-Charge:      Prof. DevrajSinh Jadav (Principal In-Charge)\n"
        "Institution:    Navgujarat BCA College, Gandhinagar                       Affiliated To:  Gujarat University, Ahmedabad"
    )
    r.font.name = "Consolas"
    r.font.size = Pt(9.5)
    r.font.color.rgb = TEXT_WHITE

    # =========================================================================
    # SLIDE 1: 01 / HOUSEHOLD CHALLENGES
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    add_fade_transition(s1)
    add_header(s1, "Common Financial Problems in Families", "01 / HOUSEHOLD CHALLENGES")

    tb_sub = s1.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Why managing family money is difficult without a centralized system:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    cards_s1 = [
        (
            "[ 01 / SCATTERED MONEY ]",
            "Multiple Earners & No Common View",
            [
                "Family members earn separately (jobs, business) but do not share one single dashboard.",
                "Head of the family cannot see total money left at the end of the month.",
                "Cash spending and online UPI payments easily get forgotten without daily tracking."
            ],
            RED_ACCENT
        ),
        (
            "[ 02 / UNNOTICED OVERSPENDING ]",
            "No Budget Limits or Warnings",
            [
                "Daily expenses (groceries, bills, shopping) happen without monthly category limits.",
                "Families only realize they overspent after their bank balance is almost finished.",
                "No visual warning bars to alert family members when limits are reached."
            ],
            AMBER_ACCENT
        ),
        (
            "[ 03 / LOANS & UDHAR ]",
            "Forgotten Loans & Unclear Records",
            [
                "Money given to friends ('Lene Hai') or borrowed ('Dene Hai') is kept in diary or memory.",
                "Partial repayments are easily forgotten, creating confusion and awkward disputes.",
                "No proof or history of who paid how much and on what date."
            ],
            CYAN_ACCENT
        )
    ]

    for i, (tag, headline, bullets, acc) in enumerate(cards_s1):
        left = Inches(0.8 + i * 3.95)
        top = Inches(1.8)
        add_card(s1, left, top, Inches(3.8), Inches(5.1), bg_color=CARD_BG, border_color=acc, border_width=1)

        tb = s1.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.4), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p_tag = tf.paragraphs[0]
        r = p_tag.add_run()
        r.text = tag + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = acc

        p_head = tf.add_paragraph()
        r = p_head.add_run()
        r.text = headline + "\n"
        r.font.name = "Segoe UI"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(8)
            r = p_b.add_run()
            r.text = "• " + b
            r.font.name = "Segoe UI"
            r.font.size = Pt(10.5)
            r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 2: 02 / THE HOMELEDGER PARADIGM
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_bg(s2)
    add_fade_transition(s2)
    add_header(s2, "The Solution: What is HomeLedger?", "02 / THE HOMELEDGER PARADIGM")

    tb_sub = s2.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "One simple website to track all family income, expenses, and debts in one place."
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    # Left Strategic Pillars Card
    add_card(s2, Inches(0.8), Inches(1.8), Inches(4.8), Inches(5.1), bg_color=CARD_BG, border_color=CYAN_ACCENT, border_width=1.5)
    tb_pil = s2.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(4.3), Inches(4.7))
    tf_p = tb_pil.text_frame
    tf_p.word_wrap = True

    p = tf_p.paragraphs[0]
    r = p.add_run()
    r.text = "MAIN HIGHLIGHTS\n"
    r.font.name = "Consolas"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CYAN_ACCENT

    p_h = tf_p.add_paragraph()
    r = p_h.add_run()
    r.text = "Built for Indian Families\n"
    r.font.name = "Segoe UI"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = TEXT_WHITE

    p_body = tf_p.add_paragraph()
    p_body.space_before = Pt(8)
    r = p_body.add_run()
    r.text = (
        "HomeLedger replaces messy diaries and scattered excel sheets with a clean, easy-to-use website. "
        "It brings all earning family members together to record transactions, sets monthly budget limits, "
        "tracks informal loans (Udhar), and keeps data safe with simple 1-click backups."
    )
    r.font.name = "Segoe UI"
    r.font.size = Pt(10.5)
    r.font.color.rgb = TEXT_MUTED

    stats = [
        ("★ 100%", "Full Visibility of Family Money"),
        ("★ 14", "Easy and Useful Modules"),
        ("★ 0-Loss", "Safe JSON Database Backup & Restore")
    ]
    for s_val, s_lbl in stats:
        p_st = tf_p.add_paragraph()
        p_st.space_before = Pt(8)
        r = p_st.add_run()
        r.text = f"{s_val} — "
        r.font.name = "Consolas"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = GREEN_ACCENT
        r_l = p_st.add_run()
        r_l.text = s_lbl
        r_l.font.name = "Segoe UI"
        r_l.font.size = Pt(10.5)
        r_l.font.color.rgb = TEXT_WHITE

    # Right 3 Pillars
    pillars_r = [
        (
            "[ FAMILY COLLABORATION ]",
            "Multi-User Family Access",
            "Admin (Head of Family) manages budgets and members. Other family members log their own daily expenses and earnings.",
            CYAN_ACCENT
        ),
        (
            "[ AUTOMATED BILLS ]",
            "Fixed Incomes & Monthly Bills",
            "Automatically adds monthly salary and regular bills (like WiFi, electricity, tuition fees) on their set due dates.",
            GREEN_ACCENT
        ),
        (
            "[ UDHAR TRACKER ]",
            "Simple Loan & Debt Tracker",
            "Clear tracking of money given to others ('Lene Hai') and money borrowed ('Dene Hai') with payment history and proofs.",
            AMBER_ACCENT
        )
    ]

    for i, (tag, title, desc, acc) in enumerate(pillars_r):
        top = Inches(1.8 + i * 1.72)
        add_card(s2, Inches(5.9), top, Inches(6.633), Inches(1.58), bg_color=CARD_BG, border_color=acc, border_width=1)
        tb = s2.shapes.add_textbox(Inches(6.1), top + Inches(0.12), Inches(6.2), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "  "
        r.font.name = "Consolas"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = acc

        r_t = p.add_run()
        r_t.text = title + "\n"
        r_t.font.name = "Segoe UI"
        r_t.font.size = Pt(12.5)
        r_t.font.bold = True
        r_t.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(4)
        r = p_d.add_run()
        r.text = desc
        r.font.name = "Segoe UI"
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 3: 03 / OBJECTIVES & SCOPE
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_bg(s3)
    add_fade_transition(s3)
    add_header(s3, "Main Objectives of the Project", "03 / OBJECTIVES & SCOPE")

    tb_sub = s3.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "What we want to achieve with this system:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    goals = [
        (
            "[ GOAL 01 ]",
            "All Family Money in One Place",
            "Combine different bank accounts, cash, and incomes into a single simple dashboard so everyone knows the total balance.",
            CYAN_ACCENT
        ),
        (
            "[ GOAL 02 ]",
            "Control Monthly Expenses",
            "Set monthly spending limits for categories like Food, Utilities, and Shopping with progress bars to stop overspending.",
            GREEN_ACCENT
        ),
        (
            "[ GOAL 03 ]",
            "Track Loans and Udhar Easily",
            "Keep clear records of money borrowed or lent with person name, dates, notes, and partial payments history.",
            AMBER_ACCENT
        ),
        (
            "[ GOAL 04 ]",
            "Easy Reports & Safe Backups",
            "Download clean PDF and CSV reports for any month, and backup all family data with a single click.",
            PURPLE_ACCENT
        )
    ]

    for i, (tag, title, desc, acc) in enumerate(goals):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.8 + row * 2.6)

        add_card(s3, left, top, Inches(5.75), Inches(2.4), bg_color=CARD_BG, border_color=acc, border_width=1)
        tb = s3.shapes.add_textbox(left + Inches(0.25), top + Inches(0.2), Inches(5.25), Inches(2.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = acc

        p_t = tf.add_paragraph()
        r = p_t.add_run()
        r.text = title + "\n"
        r.font.name = "Segoe UI"
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(6)
        r = p_d.add_run()
        r.text = desc
        r.font.name = "Segoe UI"
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 4: 04 / ARCHITECTURE & STACK
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_bg(s4)
    add_fade_transition(s4)
    add_header(s4, "System Architecture (3-Tier MVC Design)", "04 / ARCHITECTURE & STACK")

    tb_sub = s4.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "How the system is structured using standard 3-tier MVC architecture:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    tiers = [
        (
            "[ 1. USER INTERFACE TIER ]  •  Frontend (What the User Sees)",
            [
                ("• Technologies:", "Razor Views (.cshtml), HTML5, CSS3, JavaScript, jQuery"),
                ("• Styling:", "Bootstrap 5.3 framework with custom dark HUD cyberpunk theme"),
                ("• Responsiveness:", "Works smoothly on mobile phones, tablets, and desktop computers")
            ],
            CYAN_ACCENT
        ),
        (
            "[ 2. BUSINESS LOGIC TIER ]  •  Backend C# Controllers & Business Rules",
            [
                ("• Core Logic:", "Controllers handle Income, Expenses, Budgets, Loans, and Reports"),
                ("• Calculations:", "Calculates real-time balances and checks if monthly budget limits are crossed"),
                ("• User Security:", "BCrypt password hashing and Anti-Forgery tokens protect against attacks")
            ],
            GREEN_ACCENT
        ),
        (
            "[ 3. DATABASE TIER ]  •  Data Storage & Backup Engine",
            [
                ("• Database:", "MySQL Server (Port 3306) with 11 relational tables"),
                ("• ORM Tool:", "Entity Framework Core (Pomelo) for easy database operations in C#"),
                ("• Backup Engine:", "Exports all database tables into a single JSON file for safe recovery")
            ],
            PURPLE_ACCENT
        )
    ]

    for i, (title, items, acc) in enumerate(tiers):
        top = Inches(1.8 + i * 1.72)
        add_card(s4, Inches(0.8), top, Inches(11.733), Inches(1.58), bg_color=CARD_BG, border_color=acc, border_width=1)
        tb = s4.shapes.add_textbox(Inches(1.05), top + Inches(0.12), Inches(11.2), Inches(1.35))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = title + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = acc

        for lbl, val in items:
            p_i = tf.add_paragraph()
            p_i.space_before = Pt(2)
            r_l = p_i.add_run()
            r_l.text = lbl + "  "
            r_l.font.name = "Segoe UI"
            r_l.font.size = Pt(10)
            r_l.font.bold = True
            r_l.font.color.rgb = TEXT_WHITE
            r_v = p_i.add_run()
            r_v.text = val
            r_v.font.name = "Segoe UI"
            r_v.font.size = Pt(10)
            r_v.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 5: 05 / FUNCTIONAL MODULES
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_bg(s5)
    add_fade_transition(s5)
    add_header(s5, "Core System Modules Overview (14 Modules)", "05 / FUNCTIONAL MODULES")

    tb_sub = s5.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Complete list of all 14 features developed in this project:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    mod_list = [
        ("[ MODULE M1 ]", "User Login & Roles", "Secure login for Admin and Family Members using BCrypt hashing.", CYAN_ACCENT),
        ("[ MODULE M2 ]", "Main Dashboard", "Shows total balance, income, expenses, and loans at a glance.", GREEN_ACCENT),
        ("[ MODULE M3 ]", "Family Members", "Add and manage family members with relationships (Head, Wife, Son).", AMBER_ACCENT),
        ("[ MODULE M4 ]", "Income Management", "Record salary, rental income, and gifts with PDF and CSV export.", PURPLE_ACCENT),
        ("[ MODULE M5 ]", "Expense Tracking", "Record daily expenses with category, date, and receipt notes.", RED_ACCENT),
        ("[ MODULE M6 ]", "Categories", "Custom categories with colors and icons for easy sorting.", CYAN_ACCENT),
        ("[ MODULE M7 ]", "Monthly Budgets", "Set spending limits with progress bars to prevent overspending.", GREEN_ACCENT),
        ("[ MODULE M8 ]", "Recurring Incomes", "Automatically adds fixed incomes like monthly salary on set days.", AMBER_ACCENT),
        ("[ MODULE M9 ]", "Recurring Bills", "Automatically tracks regular bills like WiFi, electricity, tuition fees.", RED_ACCENT),
        ("[ MODULE M10 ]", "Savings Goals", "Set target amounts like Emergency Fund or Vacation with progress %.", PURPLE_ACCENT),
        ("[ MODULE M11 ]", "Udhar (Debt) Ledger", "Track 'Lene Hai' and 'Dene Hai' with partial payments.", CYAN_ACCENT),
        ("[ MODULE M12 ]", "Bill Reminders", "Alerts for upcoming due dates so late payment penalties are avoided.", GREEN_ACCENT),
        ("[ MODULE M13 ]", "Reports & Analysis", "Monthly breakdown charts and annual cashflow summaries.", AMBER_ACCENT),
        ("[ MODULE M14 ]", "Database Backup", "Single-click JSON backup and instant restore feature.", PURPLE_ACCENT)
    ]

    for i, (tag, title, desc, acc) in enumerate(mod_list):
        col = i % 2
        row = i // 2
        left = Inches(0.8 + col * 5.95)
        top = Inches(1.8 + row * 0.73)

        add_card(s5, left, top, Inches(5.75), Inches(0.68), bg_color=CARD_BG, border_color=CARD_BORDER)
        tb = s5.shapes.add_textbox(left + Inches(0.15), top + Inches(0.04), Inches(5.45), Inches(0.6))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + " "
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = acc

        r_t = p.add_run()
        r_t.text = title + ": "
        r_t.font.name = "Segoe UI"
        r_t.font.size = Pt(10)
        r_t.font.bold = True
        r_t.font.color.rgb = TEXT_WHITE

        r_d = p.add_run()
        r_d.text = desc
        r_d.font.name = "Segoe UI"
        r_d.font.size = Pt(9.5)
        r_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 6: 06 / MULTI-MEMBER ROLES & SECURITY
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_bg(s6)
    add_fade_transition(s6)
    add_header(s6, "Multi-User Access & Security Steps", "06 / MULTI-MEMBER ROLES & SECURITY")

    tb_sub = s6.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "How family members use the system safely and privately:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    steps_s6 = [
        (
            "[ STEP 01 ]",
            "Family Registration",
            "The head of the family creates an account with Family Name, a unique Family ID, and master password.",
            "✔ Outcome: Family Account Ready",
            CYAN_ACCENT
        ),
        (
            "[ STEP 02 ]",
            "Add Family Members",
            "The Admin adds other family members (Self, Wife, Son, Daughter) with their names and contact details.",
            "✔ Outcome: Profiles Created",
            GREEN_ACCENT
        ),
        (
            "[ STEP 03 ]",
            "Separate Logins",
            "Admin logs in for full control; other family members log in to record their individual expenses and earnings.",
            "✔ Outcome: Organized & Private",
            AMBER_ACCENT
        ),
        (
            "[ STEP 04 ]",
            "Password Safety",
            "Passwords are securely encrypted with BCrypt; session cookies keep user data protected at all times.",
            "✔ Outcome: 100% Safe Data",
            PURPLE_ACCENT
        )
    ]

    for i, (tag, title, desc, outc, acc) in enumerate(steps_s6):
        left = Inches(0.8 + i * 2.95)
        top = Inches(1.8)
        add_card(s6, left, top, Inches(2.8), Inches(5.1), bg_color=CARD_BG, border_color=acc, border_width=1)

        tb = s6.shapes.add_textbox(left + Inches(0.18), top + Inches(0.2), Inches(2.44), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = acc

        p_t = tf.add_paragraph()
        r = p_t.add_run()
        r.text = title + "\n"
        r.font.name = "Segoe UI"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(10)
        r = p_d.add_run()
        r.text = desc
        r.font.name = "Segoe UI"
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_MUTED

        p_o = tf.add_paragraph()
        p_o.space_before = Pt(20)
        r = p_o.add_run()
        r.text = outc
        r.font.name = "Consolas"
        r.font.size = Pt(10)
        r.font.bold = True
        r.font.color.rgb = GREEN_ACCENT

    # =========================================================================
    # SLIDE 7: 07 / BUDGET & CASHFLOW ENGINE
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_bg(s7)
    add_fade_transition(s7)
    add_header(s7, "Smart Budgeting & Automated Bills", "07 / BUDGET & CASHFLOW ENGINE")

    tb_sub = s7.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Helping families save money and pay bills on time:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    cards_s7 = [
        (
            "[ AUTOMATIC INCOMES & BILLS ]",
            "Recurring Transactions",
            [
                "Automatically records monthly salary on payment day without manual typing.",
                "Sets reminders and records regular bills like WiFi, electricity, and school fees.",
                "Saves time and prevents missing payment deadlines."
            ],
            CYAN_ACCENT
        ),
        (
            "[ MONTHLY BUDGET LIMITS ]",
            "Category Spending Caps",
            [
                "Set monthly spending limits for each category (e.g. Groceries ₹10,000, Dining ₹3,000).",
                "Color-coded progress bars show how much budget has been used so far.",
                "Gives clear visual warning before a family member exceeds the limit."
            ],
            GREEN_ACCENT
        ),
        (
            "[ SAVINGS GOALS ]",
            "Saving for Future Targets",
            [
                "Create goals like 'Emergency Fund' or 'New Vehicle'.",
                "Displays clear progress bar showing how much is saved and how much is left.",
                "Encourages family members to save money together for big milestones."
            ],
            PURPLE_ACCENT
        )
    ]

    for i, (tag, title, bullets, acc) in enumerate(cards_s7):
        left = Inches(0.8 + i * 3.95)
        top = Inches(1.8)
        add_card(s7, left, top, Inches(3.8), Inches(5.1), bg_color=CARD_BG, border_color=acc, border_width=1)

        tb = s7.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.4), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = acc

        p_t = tf.add_paragraph()
        r = p_t.add_run()
        r.text = title + "\n"
        r.font.name = "Segoe UI"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        for b in bullets:
            p_b = tf.add_paragraph()
            p_b.space_before = Pt(8)
            r = p_b.add_run()
            r.text = "• " + b
            r.font.name = "Segoe UI"
            r.font.size = Pt(10.5)
            r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 8: 08 / BILATERAL UDHAR & DEBT WORKFLOW
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_bg(s8)
    add_fade_transition(s8)
    add_header(s8, "Udhar (Loan) Management Workflow", "08 / BILATERAL UDHAR & DEBT WORKFLOW")

    tb_sub = s8.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "A simple 4-step process to track money given to or borrowed from others:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    phases = [
        (
            "[ STEP 1 ]",
            "Add Loan Entry",
            "Enter the person's name, choose 'Lene Hai' (Receivable) or 'Dene Hai' (Payable), and enter the amount.",
            "✔ Status: Loan Recorded",
            AMBER_ACCENT
        ),
        (
            "[ STEP 2 ]",
            "Add Notes & Proof",
            "Write the reason for the loan (e.g. medical emergency) and optionally upload receipt image.",
            "✔ Status: Proof Attached",
            CYAN_ACCENT
        ),
        (
            "[ STEP 3 ]",
            "Record Repayments",
            "Easily record partial payments whenever money is returned; remaining balance updates automatically.",
            "✔ Status: Balance Updated",
            GREEN_ACCENT
        ),
        (
            "[ STEP 4 ]",
            "Mark Completed",
            "When the remaining amount reaches ₹0, the loan status automatically changes from 'Pending' to 'Completed'.",
            "✔ Status: Fully Settled",
            PURPLE_ACCENT
        )
    ]

    for i, (tag, title, desc, sec, acc) in enumerate(phases):
        left = Inches(0.8 + i * 2.95)
        top = Inches(1.8)
        add_card(s8, left, top, Inches(2.8), Inches(5.1), bg_color=CARD_BG, border_color=acc, border_width=1)

        tb = s8.shapes.add_textbox(left + Inches(0.18), top + Inches(0.2), Inches(2.44), Inches(4.7))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = acc

        p_t = tf.add_paragraph()
        r = p_t.add_run()
        r.text = title + "\n"
        r.font.name = "Segoe UI"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(10)
        r = p_d.add_run()
        r.text = desc
        r.font.name = "Segoe UI"
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_MUTED

        p_s = tf.add_paragraph()
        p_s.space_before = Pt(20)
        r = p_s.add_run()
        r.text = sec
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = acc

    # =========================================================================
    # SLIDE 9: 09 / OPERATIONAL INTERFACE (DASHBOARD & INCOMES)
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_bg(s9)
    add_fade_transition(s9)
    add_header(s9, "System Screenshots: Dashboard & Income", "09 / OPERATIONAL INTERFACE")

    tb_sub = s9.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Modern dark user interface designed for easy everyday use:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    # Left: Dashboard Screenshot
    add_card(s9, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=CARD_BG, border_color=CYAN_ACCENT, border_width=1)
    if os.path.exists("report_assets/screenshots/05_dashboard.png"):
        s9.shapes.add_picture("report_assets/screenshots/05_dashboard.png", Inches(0.95), Inches(1.95), width=Inches(5.45))
    
    tb_c1 = s9.shapes.add_textbox(Inches(0.95), Inches(5.35), Inches(5.45), Inches(1.4))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "FIGURE 9.1: MAIN FINANCIAL DASHBOARD\n"
    r.font.name = "Consolas"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = CYAN_ACCENT
    r_d = p.add_run()
    r_d.text = "Displays 5 summary cards: Current Balance, Total Income, Total Expenses, Money to Receive, and Money to Pay, along with recent activity stream."
    r_d.font.name = "Segoe UI"
    r_d.font.size = Pt(9.5)
    r_d.font.color.rgb = TEXT_MUTED

    # Right: Income Screenshot
    add_card(s9, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=CARD_BG, border_color=GREEN_ACCENT, border_width=1)
    if os.path.exists("report_assets/screenshots/06_income_list.png"):
        s9.shapes.add_picture("report_assets/screenshots/06_income_list.png", Inches(6.9), Inches(1.95), width=Inches(5.45))
    
    tb_c2 = s9.shapes.add_textbox(Inches(6.9), Inches(5.35), Inches(5.45), Inches(1.4))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    r = p.add_run()
    r.text = "FIGURE 9.2: INCOME MANAGEMENT PAGE\n"
    r.font.name = "Consolas"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = GREEN_ACCENT
    r_d = p.add_run()
    r_d.text = "Clean table showing all income records with member name, search filter, and quick buttons to export PDF and CSV reports."
    r_d.font.name = "Segoe UI"
    r_d.font.size = Pt(9.5)
    r_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 10: 10 / OPERATIONAL INTERFACE (EXPENSES, BUDGETS & SAVINGS)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_bg(s10)
    add_fade_transition(s10)
    add_header(s10, "System Screenshots: Expenses & Udhar", "10 / OPERATIONAL INTERFACE")

    tb_sub = s10.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Clear screens for tracking daily spending and friendly loans:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    # Left: Expense Screenshot
    add_card(s10, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=CARD_BG, border_color=RED_ACCENT, border_width=1)
    if os.path.exists("report_assets/screenshots/08_expense_list.png"):
        s10.shapes.add_picture("report_assets/screenshots/08_expense_list.png", Inches(0.95), Inches(1.95), width=Inches(5.45))
    
    tb_c1 = s10.shapes.add_textbox(Inches(0.95), Inches(5.35), Inches(5.45), Inches(1.4))
    tf1 = tb_c1.text_frame
    tf1.word_wrap = True
    p = tf1.paragraphs[0]
    r = p.add_run()
    r.text = "FIGURE 10.1: EXPENSE TRACKING PAGE\n"
    r.font.name = "Consolas"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = RED_ACCENT
    r_d = p.add_run()
    r_d.text = "Lists all daily expenses with category badges, notes, and instant balance updates when a new expense is saved."
    r_d.font.name = "Segoe UI"
    r_d.font.size = Pt(9.5)
    r_d.font.color.rgb = TEXT_MUTED

    # Right: Udhar Screenshot
    add_card(s10, Inches(6.75), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=CARD_BG, border_color=AMBER_ACCENT, border_width=1)
    if os.path.exists("report_assets/screenshots/20_udhar_list.png"):
        s10.shapes.add_picture("report_assets/screenshots/20_udhar_list.png", Inches(6.9), Inches(1.95), width=Inches(5.45))
    
    tb_c2 = s10.shapes.add_textbox(Inches(6.9), Inches(5.35), Inches(5.45), Inches(1.4))
    tf2 = tb_c2.text_frame
    tf2.word_wrap = True
    p = tf2.paragraphs[0]
    r = p.add_run()
    r.text = "FIGURE 10.2: UDHAR (LOAN) LEDGER PAGE\n"
    r.font.name = "Consolas"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = AMBER_ACCENT
    r_d = p.add_run()
    r_d.text = "Shows pending loans with clear green and red badges for 'Lene Hai' vs 'Dene Hai' and remaining amounts."
    r_d.font.name = "Segoe UI"
    r_d.font.size = Pt(9.5)
    r_d.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 11: 11 / EVALUATION & FEASIBILITY
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_bg(s11)
    add_fade_transition(s11)
    add_header(s11, "Feasibility Study & Current Limitations", "11 / EVALUATION & FEASIBILITY")

    tb_sub = s11.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Why this project is practical and areas for future improvement:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    # Top: Feasibility Validation Card
    add_card(s11, Inches(0.8), Inches(1.8), Inches(11.733), Inches(2.3), bg_color=CARD_BG, border_color=GREEN_ACCENT, border_width=1)
    tb_fv = s11.shapes.add_textbox(Inches(1.05), Inches(1.95), Inches(11.2), Inches(2.0))
    tf_f = tb_fv.text_frame
    tf_f.word_wrap = True

    p = tf_f.paragraphs[0]
    r = p.add_run()
    r.text = "FEASIBILITY STUDY VALIDATION\n"
    r.font.name = "Consolas"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = GREEN_ACCENT

    f_items = [
        ("✔ Technical Feasibility:", "Built with ASP.NET Core MVC and MySQL. Runs fast, reliable, and error-free on any Windows or Linux computer."),
        ("✔ Economic Feasibility:", "Zero licensing costs because only open-source software (Free .NET SDK, MySQL Community) is used. Saves money for families."),
        ("✔ Operational Feasibility:", "Very simple user interface that any family member can learn to use in just 5 minutes without any special training.")
    ]
    for lbl, val in f_items:
        p_i = tf_f.add_paragraph()
        p_i.space_before = Pt(4)
        r_l = p_i.add_run()
        r_l.text = lbl + "   "
        r_l.font.name = "Segoe UI"
        r_l.font.size = Pt(10)
        r_l.font.bold = True
        r_l.font.color.rgb = TEXT_WHITE
        r_v = p_i.add_run()
        r_v.text = val
        r_v.font.name = "Segoe UI"
        r_v.font.size = Pt(10)
        r_v.font.color.rgb = TEXT_MUTED

    # Bottom: Operational Limitations Card
    add_card(s11, Inches(0.8), Inches(4.3), Inches(11.733), Inches(2.6), bg_color=CARD_BG, border_color=RED_ACCENT, border_width=1)
    tb_lim = s11.shapes.add_textbox(Inches(1.05), Inches(4.45), Inches(11.2), Inches(2.3))
    tf_l = tb_lim.text_frame
    tf_l.word_wrap = True

    p = tf_l.paragraphs[0]
    r = p.add_run()
    r.text = "CURRENT PROJECT LIMITATIONS\n"
    r.font.name = "Consolas"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = RED_ACCENT

    l_items = [
        ("⚠ Manual Bank Entry:", "Users enter transactions manually. Direct bank API link is not connected yet to keep it simple and free."),
        ("⚠ Single Currency (INR):", "System currently works with Indian Rupees (₹); foreign currency conversion can be added in future versions."),
        ("⚠ Requires Server Connection:", "Must be opened through browser connected to the local or cloud web server."),
        ("⚠ Photo Proofs are Manual:", "Receipts are uploaded as images; automated receipt text scanner (OCR) is planned for next update.")
    ]
    for lbl, val in l_items:
        p_i = tf_l.add_paragraph()
        p_i.space_before = Pt(4)
        r_l = p_i.add_run()
        r_l.text = lbl + "   "
        r_l.font.name = "Segoe UI"
        r_l.font.size = Pt(10)
        r_l.font.bold = True
        r_l.font.color.rgb = TEXT_WHITE
        r_v = p_i.add_run()
        r_v.text = val
        r_v.font.name = "Segoe UI"
        r_v.font.size = Pt(10)
        r_v.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 12: 12 / STRATEGIC ROADMAP
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_bg(s12)
    add_fade_transition(s12)
    add_header(s12, "Future Scope & Enhancements", "12 / STRATEGIC ROADMAP")

    tb_sub = s12.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "Features planned to make HomeLedger even more powerful in future versions:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    # Left: Flagship AI Innovation Card
    add_card(s12, Inches(0.8), Inches(1.8), Inches(5.75), Inches(5.1), bg_color=CARD_BG, border_color=CYAN_ACCENT, border_width=1.5)
    tb_ai = s12.shapes.add_textbox(Inches(1.05), Inches(2.0), Inches(5.25), Inches(4.7))
    tf_ai = tb_ai.text_frame
    tf_ai.word_wrap = True

    p = tf_ai.paragraphs[0]
    r = p.add_run()
    r.text = "🌟 MAIN FUTURE FEATURE\n"
    r.font.name = "Consolas"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = CYAN_ACCENT

    p_t = tf_ai.add_paragraph()
    r = p_t.add_run()
    r.text = "AI Financial Assistant & Spend Prediction\n"
    r.font.name = "Segoe UI"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = TEXT_WHITE

    ai_bullets = [
        ("• Balance Prediction:", "Predicts how much money will remain at month-end based on past spending habits."),
        ("• Spending Alerts:", "Automatically alerts if extra money is being spent on shopping or food."),
        ("• Smart Saving Tips:", "Gives useful suggestions to help the family save an extra 10% to 20% every month.")
    ]
    for lbl, val in ai_bullets:
        p_b = tf_ai.add_paragraph()
        p_b.space_before = Pt(8)
        r = p_b.add_run()
        r.text = lbl + " "
        r.font.name = "Segoe UI"
        r.font.size = Pt(10.5)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE
        r_v = p_b.add_run()
        r_v.text = val
        r_v.font.name = "Segoe UI"
        r_v.font.size = Pt(10)
        r_v.font.color.rgb = TEXT_MUTED

    # Right: 4 Enhancement Pillars
    futs = [
        ("[ MOBILE APP ]", "Android & iOS App", "Dedicated mobile app for quick expense logging on smartphones.", GREEN_ACCENT),
        ("[ BANK & UPI SYNC ]", "Direct Bank Account Sync", "Connect directly with UPI and bank statements for automatic data entry.", AMBER_ACCENT),
        ("[ BILL SCANNER ]", "Smart Receipt Scanner (OCR)", "Take a photo of grocery bill and let system read the amount automatically.", PURPLE_ACCENT),
        ("[ WHATSAPP ALERTS ]", "WhatsApp Bill Reminders", "Send bill payment reminders and budget warnings directly on WhatsApp.", CYAN_ACCENT)
    ]

    for i, (tag, title, desc, acc) in enumerate(futs):
        top = Inches(1.8 + i * 1.28)
        add_card(s12, Inches(6.75), top, Inches(5.75), Inches(1.18), bg_color=CARD_BG, border_color=acc, border_width=1)
        tb = s12.shapes.add_textbox(Inches(6.95), top + Inches(0.08), Inches(5.35), Inches(1.0))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + " "
        r.font.name = "Consolas"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = acc
        r_t = p.add_run()
        r_t.text = title + "\n"
        r_t.font.name = "Segoe UI"
        r_t.font.size = Pt(11)
        r_t.font.bold = True
        r_t.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(3)
        r = p_d.add_run()
        r.text = desc
        r.font.name = "Segoe UI"
        r.font.size = Pt(9.5)
        r.font.color.rgb = TEXT_MUTED

    # =========================================================================
    # SLIDE 13: 13 / SUMMARY & CONCLUSION
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_bg(s13)
    add_fade_transition(s13)
    add_header(s13, "Summary & Conclusion", "13 / SUMMARY & CONCLUSION")

    tb_sub = s13.shapes.add_textbox(Inches(0.8), Inches(1.35), Inches(11.733), Inches(0.35))
    p = tb_sub.text_frame.paragraphs[0]
    r = p.add_run()
    r.text = "How HomeLedger helps modern families achieve financial peace of mind:"
    r.font.name = "Segoe UI"
    r.font.size = Pt(11)
    r.font.italic = True
    r.font.color.rgb = TEXT_MUTED

    pillars_s13 = [
        (
            "[ BETTER SAVINGS ]",
            "Smart Money Habits",
            "Helps families save regularly by setting clear budgets and cutting down unnecessary expenses.",
            CYAN_ACCENT
        ),
        (
            "[ NO CONFUSION ]",
            "Peaceful Family Finances",
            "Multi-member logins and clear loan tracking remove arguments about who spent what and who owes money.",
            GREEN_ACCENT
        ),
        (
            "[ SAFE & RELIABLE ]",
            "Never Lose Financial Data",
            "Built on solid .NET architecture with easy 1-click database backups to keep family records safe forever.",
            PURPLE_ACCENT
        )
    ]

    for i, (tag, title, desc, acc) in enumerate(pillars_s13):
        left = Inches(0.8 + i * 3.95)
        top = Inches(1.8)
        add_card(s13, left, top, Inches(3.8), Inches(3.3), bg_color=CARD_BG, border_color=acc, border_width=1)
        tb = s13.shapes.add_textbox(left + Inches(0.2), top + Inches(0.2), Inches(3.4), Inches(2.9))
        tf = tb.text_frame
        tf.word_wrap = True

        p = tf.paragraphs[0]
        r = p.add_run()
        r.text = tag + "\n"
        r.font.name = "Consolas"
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = acc

        p_t = tf.add_paragraph()
        r = p_t.add_run()
        r.text = title + "\n"
        r.font.name = "Segoe UI"
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = TEXT_WHITE

        p_d = tf.add_paragraph()
        p_d.space_before = Pt(8)
        r = p_d.add_run()
        r.text = desc
        r.font.name = "Segoe UI"
        r.font.size = Pt(10.5)
        r.font.color.rgb = TEXT_MUTED

    # Bottom Thank You Banner
    add_card(s13, Inches(0.8), Inches(5.3), Inches(11.733), Inches(1.6), bg_color=RGBColor(14, 21, 35), border_color=CYAN_ACCENT, border_width=1.5)
    tb_ty = s13.shapes.add_textbox(Inches(1.0), Inches(5.4), Inches(11.3), Inches(1.4))
    tf_ty = tb_ty.text_frame
    tf_ty.word_wrap = True

    p = tf_ty.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run()
    r.text = "THANK YOU  •  QUESTIONS & DISCUSSION\n"
    r.font.name = "Segoe UI"
    r.font.size = Pt(18)
    r.font.bold = True
    r.font.color.rgb = CYAN_ACCENT

    p_dt = tf_ty.add_paragraph()
    p_dt.alignment = PP_ALIGN.CENTER
    r_dt = p_dt.add_run()
    r_dt.text = (
        "Family Finance Management System (HomeLedger)  |  ASP.NET Core 10.0 MVC  |  MySQL\n"
        "Presented By: Harshiddh Rana  |  Project Guide: Prof. Anjali Nimavat  |  Navgujarat BCA College, Gandhinagar"
    )
    r_dt.font.name = "Consolas"
    r_dt.font.size = Pt(10.5)
    r_dt.font.color.rgb = TEXT_WHITE

    # Save
    out_pptx = r"c:\Users\Rana Harshiddh\Desktop\Family-Finance-Management-main\Family_Finance_Management_Presentation.pptx"
    out_pptx_simple = r"c:\Users\Rana Harshiddh\Desktop\Family-Finance-Management-main\Family_Finance_Management_Simple_Presentation.pptx"
    
    saved_paths = []
    try:
        prs.save(out_pptx)
        saved_paths.append(out_pptx)
        print(f"Saved successfully to: {out_pptx}")
    except PermissionError:
        print(f"Notice: {out_pptx} is currently open in PowerPoint.")
    
    try:
        prs.save(out_pptx_simple)
        saved_paths.append(out_pptx_simple)
        print(f"Saved successfully to: {out_pptx_simple}")
    except Exception as e:
        print(f"Error saving to {out_pptx_simple}: {e}")

    print(f"Simplified PPTX presentations generated: {saved_paths}")

if __name__ == "__main__":
    create_deck()
