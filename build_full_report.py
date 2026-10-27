import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn
import os

def create_report():
    doc = docx.Document()

    # Define color palette
    COLOR_PRIMARY = RGBColor(27, 54, 93)     # Deep Navy (#1B365D)
    COLOR_SECONDARY = RGBColor(46, 91, 136)  # Steel Blue (#2E5B88)
    COLOR_DARK = RGBColor(34, 34, 34)        # Charcoal (#222222)
    COLOR_MUTED = RGBColor(100, 100, 100)    # Gray (#666666)

    HEX_PRIMARY = "1B365D"
    HEX_SECONDARY = "2E5B88"
    HEX_BG_LIGHT = "F4F7FA"
    HEX_BORDER = "D0D7DE"
    HEX_CALLOUT_BORDER = "008080"

    # Configure header and footer
    section = doc.sections[0]
    section.different_first_page_header_footer = True

    # Running header (pages 2 onwards)
    header = section.header
    p_hdr = header.paragraphs[0]
    p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r_hdr = p_hdr.add_run("Family Finance Management System (HomeLedger) | BCA Project Report")
    r_hdr.font.name = "Calibri"
    r_hdr.font.size = Pt(8.5)
    r_hdr.italic = True
    r_hdr.font.color.rgb = COLOR_MUTED

    # Running footer (pages 2 onwards)
    footer = section.footer
    p_ftr = footer.paragraphs[0]
    p_ftr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    r_ftr_l = p_ftr.add_run("Navgujarat BCA College, Gandhinagar · Gujarat University\t\tPage ")
    r_ftr_l.font.name = "Calibri"
    r_ftr_l.font.size = Pt(8.5)
    r_ftr_l.font.color.rgb = COLOR_MUTED

    # Add PAGE field
    fld_page = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    r_pg = p_ftr.add_run()
    r_pg._r.append(fld_page)
    r_pg.font.name = "Calibri"
    r_pg.font.size = Pt(8.5)
    r_pg.bold = True
    r_pg.font.color.rgb = COLOR_PRIMARY

    r_of = p_ftr.add_run(" of ")
    r_of.font.name = "Calibri"
    r_of.font.size = Pt(8.5)
    r_of.font.color.rgb = COLOR_MUTED

    # Add NUMPAGES field
    fld_numpages = parse_xml(r'<w:fldSimple %s w:instr="NUMPAGES"/>' % nsdecls('w'))
    r_np = p_ftr.add_run()
    r_np._r.append(fld_numpages)
    r_np.font.name = "Calibri"
    r_np.font.size = Pt(8.5)
    r_np.font.color.rgb = COLOR_MUTED

    # Helper functions
    def set_cell_background(cell, hex_color):
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
        cell._tc.get_or_add_tcPr().append(shd)

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def set_table_borders(table, color="D0D7DE", sz="4", val="single"):
        tblPr = table._tbl.tblPr
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr.append(borders)

    def add_p(text, bold=False, italic=False, size=11, color=COLOR_DARK, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=6, line_spacing=1.15):
        p = doc.add_paragraph()
        p.alignment = align
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = line_spacing
        run = p.add_run(text)
        run.bold = bold
        run.italic = italic
        run.font.name = "Calibri"
        run.font.size = Pt(size)
        run.font.color.rgb = color
        return p

    def add_bullet(text, bold_prefix=None, space_after=3):
        p = doc.add_paragraph(style='List Bullet')
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(space_after)
        p.paragraph_format.line_spacing = 1.15
        if bold_prefix:
            run_bp = p.add_run(bold_prefix)
            run_bp.bold = True
            run_bp.font.name = "Calibri"
            run_bp.font.size = Pt(11)
            run_bp.font.color.rgb = COLOR_PRIMARY
        run_txt = p.add_run(text)
        run_txt.font.name = "Calibri"
        run_txt.font.size = Pt(11)
        run_txt.font.color.rgb = COLOR_DARK
        return p

    def add_h1(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(18)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_h2(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(12)
        p.paragraph_format.space_after = Pt(4)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(14)
        run.font.color.rgb = COLOR_SECONDARY
        return p

    def add_h3(text):
        p = doc.add_paragraph()
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p.paragraph_format.space_before = Pt(8)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.keep_with_next = True
        run = p.add_run(text)
        run.bold = True
        run.font.name = "Calibri"
        run.font.size = Pt(12)
        run.font.color.rgb = COLOR_PRIMARY
        return p

    def add_callout(title, text):
        tbl = doc.add_table(rows=1, cols=1)
        tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = tbl.cell(0, 0)
        set_cell_background(cell, HEX_BG_LIGHT)
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        
        tcPr = cell._tc.get_or_add_tcPr()
        borders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'<w:left w:val="single" w:sz="24" w:space="0" w:color="{HEX_CALLOUT_BORDER}"/>'
            f'<w:top w:val="none"/>'
            f'<w:right w:val="none"/>'
            f'<w:bottom w:val="none"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(borders)

        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(4)
        r_title = p.add_run(f"★ {title}\n")
        r_title.bold = True
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(11)
        r_title.font.color.rgb = COLOR_PRIMARY
        
        r_txt = p.add_run(text)
        r_txt.font.name = "Calibri"
        r_txt.font.size = Pt(10.5)
        r_txt.font.color.rgb = COLOR_DARK
        
        # spacer
        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(4)

    def add_custom_table(headers, data, col_widths=None):
        table = doc.add_table(rows=len(data) + 1, cols=len(headers))
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        set_table_borders(table)

        # Header row
        hdr_cells = table.rows[0].cells
        for i, h in enumerate(headers):
            hdr_cells[i].text = h
            set_cell_background(hdr_cells[i], HEX_PRIMARY)
            set_cell_margins(hdr_cells[i], top=100, bottom=100, left=120, right=120)
            p = hdr_cells[i].paragraphs[0]
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
            for r in p.runs:
                r.bold = True
                r.font.name = "Calibri"
                r.font.size = Pt(10)
                r.font.color.rgb = RGBColor(255, 255, 255)

        # Data rows
        for row_idx, row_data in enumerate(data):
            row_cells = table.rows[row_idx + 1].cells
            bg_color = HEX_BG_LIGHT if row_idx % 2 == 1 else "FFFFFF"
            for col_idx, cell_value in enumerate(row_data):
                row_cells[col_idx].text = str(cell_value)
                set_cell_background(row_cells[col_idx], bg_color)
                set_cell_margins(row_cells[col_idx], top=80, bottom=80, left=120, right=120)
                p = row_cells[col_idx].paragraphs[0]
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for r in p.runs:
                    r.font.name = "Calibri"
                    r.font.size = Pt(9.5)
                    r.font.color.rgb = COLOR_DARK

        # Set column widths if provided
        if col_widths:
            for row in table.rows:
                for idx, width in enumerate(col_widths):
                    row.cells[idx].width = Inches(width)

        sp = doc.add_paragraph()
        sp.paragraph_format.space_before = Pt(0)
        sp.paragraph_format.space_after = Pt(4)
        return table

    def add_screenshot_figure(image_path, fig_num, title, route, description):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(10)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.paragraph_format.keep_with_next = True
        
        if os.path.exists(image_path):
            p_img.add_run().add_picture(image_path, width=Inches(5.7))
        else:
            p_img.add_run(f"[Screenshot Placeholder: {image_path}]").bold = True

        p_caption = doc.add_paragraph()
        p_caption.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_caption.paragraph_format.space_before = Pt(2)
        p_caption.paragraph_format.space_after = Pt(4)
        p_caption.paragraph_format.keep_with_next = True
        
        r_fignum = p_caption.add_run(f"Figure {fig_num}: ")
        r_fignum.bold = True
        r_fignum.font.name = "Calibri"
        r_fignum.font.size = Pt(10)
        r_fignum.font.color.rgb = COLOR_PRIMARY
        
        r_title = p_caption.add_run(f"{title} (Route: ")
        r_title.bold = True
        r_title.font.name = "Calibri"
        r_title.font.size = Pt(10)
        r_title.font.color.rgb = COLOR_DARK

        r_route = p_caption.add_run(route)
        r_route.font.name = "Consolas"
        r_route.font.size = Pt(9.5)
        r_route.font.color.rgb = COLOR_SECONDARY

        r_close = p_caption.add_run(")")
        r_close.bold = True
        r_close.font.name = "Calibri"
        r_close.font.size = Pt(10)
        r_close.font.color.rgb = COLOR_DARK

        p_desc = doc.add_paragraph()
        p_desc.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p_desc.paragraph_format.space_before = Pt(0)
        p_desc.paragraph_format.space_after = Pt(12)
        r_desc = p_desc.add_run(description)
        r_desc.font.name = "Calibri"
        r_desc.font.size = Pt(10)
        r_desc.font.color.rgb = COLOR_DARK

    # ==========================================
    # 1. COVER PAGE
    # ==========================================
    add_p("A PROJECT REPORT ON", bold=True, size=15, color=COLOR_SECONDARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=8)
    
    p_title = add_p("FAMILY FINANCE MANAGEMENT SYSTEM\n(HomeLedger)", bold=True, size=22, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)
    
    add_p("Submitted in partial fulfilment of the requirements for the award of the degree of", italic=True, size=12, color=COLOR_MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=4)
    add_p("Bachelor of Computer Applications (Honours)", bold=True, size=14, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=6)
    add_p("Course: Full Stack Web Development Project using ASP.NET Core", bold=True, size=12, color=COLOR_SECONDARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=18)

    # Logos table (2 columns side by side)
    logo_table = doc.add_table(rows=1, cols=2)
    logo_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    c1, c2 = logo_table.rows[0].cells
    c1.width = Inches(2.8)
    c2.width = Inches(2.8)
    
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists("report_assets/image1.png"):
        p1.add_run().add_picture("report_assets/image1.png", width=Inches(1.5))
        
    p2 = c2.paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if os.path.exists("report_assets/image2.jpeg"):
        p2.add_run().add_picture("report_assets/image2.jpeg", width=Inches(1.4))

    # Meta table
    doc.add_paragraph() # spacing
    meta_table = doc.add_table(rows=1, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    mc1, mc2 = meta_table.rows[0].cells
    mc1.width = Inches(2.8)
    mc2.width = Inches(2.8)

    p_pres = mc1.paragraphs[0]
    p_pres.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r = p_pres.add_run("PRESENTED BY:\n")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_PRIMARY
    r_val = p_pres.add_run("Harshiddh Rana\nBCA (Hons.)\nNavgujarat BCA College, Gandhinagar")
    r_val.font.size = Pt(10.5)

    p_sub = mc2.paragraphs[0]
    p_sub.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p_sub.add_run("SUBMITTED TO:\n")
    r.bold = True
    r.font.size = Pt(11)
    r.font.color.rgb = COLOR_PRIMARY
    r_val = p_sub.add_run("Gujarat University\nAhmedabad, Gujarat\nAcademic Year 2026–27")
    r_val.font.size = Pt(10.5)

    add_p("UNDER THE GUIDANCE OF", bold=True, size=11, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=24, space_after=2)
    add_p("Prof. Anjali Nimavat", bold=True, size=12, color=COLOR_DARK, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=2)
    add_p("Assistant Professor, Navgujarat BCA College, Gandhinagar", italic=True, size=11, color=COLOR_MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=0)

    doc.add_page_break()

    # ==========================================
    # 2. COLLEGE CERTIFICATE
    # ==========================================
    cert_logo_tbl = doc.add_table(rows=1, cols=2)
    cert_logo_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cc1, cc2 = cert_logo_tbl.rows[0].cells
    cc1.width = Inches(2.8)
    cc2.width = Inches(2.8)
    p_cl1 = cc1.paragraphs[0]
    p_cl1.alignment = WD_ALIGN_PARAGRAPH.LEFT
    if os.path.exists("report_assets/image1.png"):
        p_cl1.add_run().add_picture("report_assets/image1.png", width=Inches(1.2))
    p_cl2 = cc2.paragraphs[0]
    p_cl2.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    if os.path.exists("report_assets/image2.jpeg"):
        p_cl2.add_run().add_picture("report_assets/image2.jpeg", width=Inches(1.1))

    add_p("Navgujarat BCA College Gandhinagar", bold=True, size=16, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=2)
    add_p("Affiliated to Gujarat University · Ahmedabad, Gujarat", italic=True, size=11, color=COLOR_MUTED, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=14)

    add_p("COLLEGE CERTIFICATE", bold=True, size=16, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=0, space_after=16)

    cert_text = (
        "This is to certify that the project report entitled “Family Finance Management System (HomeLedger)” "
        "is a bonafide record of the work carried out by Harshiddh Rana and submitted to Gujarat University in partial "
        "fulfillment of the requirements for the award of the degree of Bachelor of Computer Applications (Honors) for the course "
        "Full Stack Web Development Project using ASP.NET Core during the academic year 2026–27.\n\n"
        "To the best of our knowledge, this work is original, was carried out at Navgujarat BCA College, Gandhinagar, "
        "under the guidance of Prof. Anjali Nimavat, and has not been submitted in part or in full to any other university or "
        "institution for the award of any degree or diploma."
    )
    add_p(cert_text, size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=24, line_spacing=1.3)

    sig_tbl = doc.add_table(rows=2, cols=3)
    sig_tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_cells = sig_tbl.rows[0].cells
    s_cells[0].width = Inches(2.0)
    s_cells[1].width = Inches(2.0)
    s_cells[2].width = Inches(1.8)

    p_s1 = s_cells[0].paragraphs[0]
    p_s1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s1.add_run("_____________________\n").bold = True
    p_s1.add_run("Prof. Anjali Nimavat\n").bold = True
    p_s1.add_run("Project Guide\nNavgujarat BCA College").font.size = Pt(9.5)

    p_s2 = s_cells[1].paragraphs[0]
    p_s2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s2.add_run("_____________________\n").bold = True
    p_s2.add_run("Prof. DevrajSinh Jadav\n").bold = True
    p_s2.add_run("Principal In-Charge\nNavgujarat BCA College").font.size = Pt(9.5)

    p_s3 = s_cells[2].paragraphs[0]
    p_s3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_s3.add_run("_____________________\n").bold = True
    p_s3.add_run("External Examiner\n").bold = True
    p_s3.add_run("Gujarat University").font.size = Pt(9.5)

    s2_cells = sig_tbl.rows[1].cells
    p_seal = s2_cells[0].paragraphs[0]
    p_seal.add_run("\n\nCollege Seal: [               ]")
    p_dt = s2_cells[2].paragraphs[0]
    p_dt.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_dt.add_run("\n\nPlace: Gandhinagar\nDate:     /     / 2026")

    doc.add_page_break()

    # ==========================================
    # 3. ACKNOWLEDGEMENT
    # ==========================================
    add_p("ACKNOWLEDGEMENT", bold=True, size=16, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=16, space_after=18)

    ack_text = (
        "Completing this project has been a great learning experience for me, and many people helped me along the way. "
        "I would like to thank all of them.\n\n"
        "First, I am thankful to the management of Navgujarat BCA College, Gandhinagar, for providing good laboratory facilities, "
        "library resources and a friendly environment for learning.\n\n"
        "I express my sincere gratitude to Prof. Devrajsinh Jadav, Principal In-Charge, Navgujarat BCA College, Gandhinagar, "
        "for her constant encouragement and for providing all the facilities needed for this project.\n\n"
        "I am deeply thankful to my project guide, Prof. Anjali Nimavat, for his valuable guidance at every stage of this work. "
        "Her suggestions helped to choose the right way to present my results.\n\n"
        "I am also grateful to Gujarat University for including the course Full Stack Web Development Project using ASP.NET Core "
        "in the BCA (Honors) program. This course gave me the chance to build a complete .Net Core project.\n\n"
        "Finally, I thank my family and friends for their support and patience throughout this work."
    )
    add_p(ack_text, size=11.5, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=24, line_spacing=1.3)

    p_stud = doc.add_paragraph()
    p_stud.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_stud.paragraph_format.space_before = Pt(20)
    p_stud.add_run("Harshiddh Rana\n").bold = True
    p_stud.add_run("BCA (Hons.)\nNavgujarat BCA College, Gandhinagar")

    doc.add_page_break()

    # ==========================================
    # 4. INDEX / TABLE OF CONTENTS
    # ==========================================
    add_p("INDEX", bold=True, size=18, color=COLOR_PRIMARY, align=WD_ALIGN_PARAGRAPH.CENTER, space_before=10, space_after=14)

    index_headers = ["Sr. No.", "Topic / Chapter Description", "Page No."]
    index_data = [
        ["--", "College Certificate", "2"],
        ["--", "Acknowledgement", "3"],
        ["--", "Project Abstract & Executive Summary", "5"],
        ["1", "Project Overview & Background", "6"],
        ["2", "Purpose and Scope of the Project", "8"],
        ["3", "Existing System vs. Proposed System", "10"],
        ["4", "Feasibility Study (Technical, Operational, Economic)", "12"],
        ["5", "Hardware and Software Requirement Specification (SRS)", "13"],
        ["6", "Project Architecture & Directory Structure", "15"],
        ["7", "Core Modules & Functional Description", "17"],
        ["8", "Database Design, Schema & Data Dictionary", "19"],
        ["9", "System Screenshots & UI Walkthrough (29 Screens with Details)", "24"],
        ["10", "System Limitations", "39"],
        ["11", "Future Enhancements", "40"],
        ["12", "References & Bibliography", "41"]
    ]
    add_custom_table(index_headers, index_data, col_widths=[0.8, 4.3, 0.9])

    doc.add_page_break()

    # ==========================================
    # 5. ABSTRACT & EXECUTIVE SUMMARY
    # ==========================================
    add_h1("Project Abstract & Executive Summary")
    add_p(
        "The Family Finance Management System (branded as HomeLedger) is an enterprise-grade, responsive full-stack web application "
        "developed using ASP.NET Core 10.0 and Entity Framework Core 9.0 with MySQL/MariaDB database storage. The platform is designed "
        "to solve the critical financial visibility challenges faced by modern joint and nuclear households, where multiple family members "
        "earn, spend, lend, and borrow across multiple disparate channels."
    )
    add_p(
        "Unlike conventional single-user expense tracking apps or error-prone spreadsheet ledgers, HomeLedger implements a centralized "
        "household financial ecosystem. Key functional pillars include role-differentiated access (Household Admin vs. Family Member), "
        "granular Income and Expense management with dynamic CSV and QuestPDF exports, monthly Category-wise Budget tracking with visual "
        "progress bars, automated Recurring Income and Expense scheduling, Goal-oriented Savings trackers, an Udhar (Debt/Loan) register "
        "categorized by 'Lene Hai' (Receivables) and 'Dene Hai' (Payables), due date Payment Reminders, and an automated full-database "
        "JSON Backup and Disaster Recovery engine."
    )
    add_p(
        "The frontend boasts an immersive, high-tech 'HUD Admin' dark-terminal theme styled with JetBrains Mono typography, glowing neon "
        "cyber-notches, and responsive Bootstrap components. HomeLedger delivers complete financial transparency, encourages collaborative "
        "domestic budgeting, and safeguards long-term financial security for the entire family unit."
    )

    add_callout(
        "Key Project Highlights",
        "• Full-Stack Architecture: ASP.NET Core 10.0 MVC + Entity Framework Core 9.0 + Pomelo MySQL.\n"
        "• Multi-Member Collaboration: Single family entity with independent member credentials and activity audit.\n"
        "• Specialized Modules: Udhar (Debt) Ledger, Recurring Transactions, Savings Goals, Bill Due Date Alerts.\n"
        "• Analytical Reporting: Integrated QuestPDF for vector-sharp PDF reports and CSV ledger downloads.\n"
        "• Robust Data Protection: Full JSON database snapshot export and single-click disaster restore."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 1: PROJECT OVERVIEW
    # ==========================================
    add_h1("Chapter 1: Project Overview")
    
    add_h2("1.1 Background & Motivation")
    add_p(
        "In modern households, managing personal and familial finance has evolved from a single breadwinner's pocket diary into a "
        "complex multi-channel operation. Today, households typically comprise multiple earning individuals—parents, spouses, and adult "
        "children—who generate distinct streams of income (salaries, freelancing, rental income, investments) and incur shared expenses "
        "(groceries, school fees, utilities, insurance, maintenance, entertainment)."
    )
    add_p(
        "Despite this complexity, most Indian families continue to manage their money haphazardly: relying on physical notebooks, fragmented "
        "UPI payment histories across multiple banking apps, or sporadic spreadsheets. Consequently, family heads lack real-time visibility "
        "into the collective net balance, overspend without realizing budget limits, forget recurring bill payment deadlines, and lose track "
        "of informal loans and borrowings ('Udhar') given to or taken from relatives and acquaintances."
    )

    add_h2("1.2 Problem Statement")
    add_p("The primary problems identified in contemporary household money management include:")
    add_bullet("Fragmented Financial Records: Transactions are scattered across banking SMS alerts, UPI transaction logs, paper receipts, and mental notes with no central consolidated ledger.")
    add_bullet("Lack of Collaborative Visibility: One member rarely knows the daily expenditures made by another, leading to duplicate purchases and unplanned deficits.")
    add_bullet("Unmonitored Budget Overruns: Absence of real-time category spending alerts means families discover overspending only after savings have depleted.")
    add_bullet("Neglected Debt & Informal Loans (Udhar): Informal debts given to friends or borrowed from colleagues often lack formal documentation, leading to forgotten repayments and financial disputes.")
    add_bullet("Missed Due Date Penalties: Late payment of utility bills, credit card statements, and school fees leads to unnecessary late fees and interest penalties.")
    add_bullet("Data Vulnerability & Loss: Physical paper diaries get misplaced or damaged, and simple spreadsheets lack automated backup mechanisms.")

    add_h2("1.3 Objectives of the Project")
    add_bullet("To develop a centralized, secure, multi-user web portal for holistic family finance tracking using ASP.NET Core.")
    add_bullet("To provide distinct access privileges for Family Administrators (full CRUD, member management, backups) and Family Members (viewing and transaction logging).")
    add_bullet("To implement real-time financial health dashboards displaying Remaining Balance, Total Income, Total Expenses, Receivables, and Payables.")
    add_bullet("To automate recurring transactions such as monthly salaries, broadband plans, rent, and subscriptions.")
    add_bullet("To offer visual goal-oriented savings tracking with progress percentages and milestone completion estimations.")
    add_bullet("To provide an organized Udhar (Debt/Credit) ledger supporting partial payments and transaction proof attachments.")
    add_bullet("To generate printable, vector-sharp financial audit reports (PDF & CSV) using the QuestPDF engine.")
    add_bullet("To build a complete JSON-based database export and import mechanism for zero-loss disaster recovery.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 2: PURPOSE AND SCOPE
    # ==========================================
    add_h1("Chapter 2: Purpose and Scope of the Project")

    add_h2("2.1 Purpose of the Project")
    add_p(
        "The primary purpose of the Family Finance Management System is to eliminate domestic financial ambiguity by providing an intuitive, "
        "secure, and collaborative web environment. It bridges the gap between complex commercial accounting software (which is overly technical "
        "for domestic users) and primitive single-user mobile tracking apps (which cannot accommodate multiple family members contributing to a "
        "common household pool)."
    )

    add_h2("2.2 Scope of the Application")
    add_p("The operational scope encompasses the following core functional areas:")
    add_bullet("Family Unit Account Registration: Self-service registration enabling creation of a unique Family ID and encrypted credentials.")
    add_bullet("Family Member Directory: Enrollment of family members with designated domestic relations (Head, Wife, Son, Daughter, Parent) and contact details.")
    add_bullet("Income & Expense Ledger: Logging monetary inflows and outflows with associated metadata (date, member, category/source, description).")
    add_bullet("Dynamic Financial Categorization: User-defined categorization schema supporting distinct color markers and icon identifiers.")
    add_bullet("Category Budget Caps: Monthly budget threshold configurations with visual tracking against actual expenditures.")
    add_bullet("Recurring Payment Automation: Setup of monthly, quarterly, or annual auto-renewing income and expense streams.")
    add_bullet("Savings Goals Management: Definition of capital targets, deadline tracking, and progressive fund additions.")
    add_bullet("Udhar (Receivables & Payables) Tracking: Bidirectional ledger for tracking loans extended ('Lene Hai') and debts incurred ('Dene Hai').")
    add_bullet("Due Date Reminder System: Calendar-integrated alert register for utility bills, school fees, and statutory obligations.")
    add_bullet("Analytical Reports: Generation of monthly category breakdown summaries and 12-month annual cash flow comparative tables.")
    add_bullet("Data Export & Archival: On-demand export of transaction data to CSV and professional PDF, alongside complete database snapshot backup.")

    add_h2("2.3 Target User Base & Stakeholders")
    add_bullet("Primary Household Heads / Administrators: Managing the macro budget, enrolling members, configuring categories, and overseeing database backups.")
    add_bullet("Earning Family Members: Logging their respective salary or freelance deposits and individual expenditures.")
    add_bullet("Dependent Family Members: Tracking allocated allowances, education expenses, and monitoring shared household savings targets.")

    add_h2("2.4 Boundaries and Assumptions")
    add_p(
        "The system assumes that the hosting environment maintains a stable connection to a MySQL database server and that end-users possess a "
        "modern standards-compliant web browser. The system operates primarily in Indian Rupees (₹) as the base operational currency. Automated "
        "direct bank account scraping is omitted by design to maintain complete user data privacy and eliminate reliance on proprietary banking APIs."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 3: EXISTING VS PROPOSED SYSTEM
    # ==========================================
    add_h1("Chapter 3: Existing System vs. Proposed System")

    add_h2("3.1 Analysis of the Existing System")
    add_p(
        "Currently, most households manage domestic finances through one of three conventional methods: physical paper registers/diaries, "
        "standalone Microsoft Excel spreadsheets, or single-user mobile expense apps. A critical examination reveals severe operational limitations "
        "in all three approaches."
    )

    add_h2("3.2 Limitations of the Existing System")
    add_bullet("Lack of Collaborative Real-Time Synchronization: In a paper ledger or local Excel file, only one individual can record transactions at a time. Other family members remain completely unaware of current balances until manually informed.")
    add_bullet("High Susceptibility to Data Loss: Paper registers suffer from physical deterioration, spills, and accidental loss. Local spreadsheet files are frequently corrupted or lost during hard drive failures.")
    add_bullet("Absence of Automated Recurring Computations: Regular transactions like monthly salaries, rent, and recurring subscriptions require tedious manual re-entry every month.")
    add_bullet("No Built-In Debt ('Udhar') Management: General accounting tools do not cater to the unique domestic concept of tracking informal bilateral loans with friends, neighbors, and relatives.")
    add_bullet("Limited Security & Auditability: Physical notebooks have zero password protection, exposing sensitive family finances to anyone in the household.")

    add_h2("3.3 Proposed System Architecture & Advantages")
    add_p(
        "The proposed Family Finance Management System (HomeLedger) overcomes every limitation of traditional systems by delivering a unified, "
        "secure, cloud-ready web portal built upon ASP.NET Core MVC."
    )

    comp_headers = ["Evaluation Criteria", "Conventional Methods (Paper / Excel)", "Proposed HomeLedger Portal"]
    comp_data = [
        ["Accessibility", "Restricted to a single physical device or paper book.", "Accessible from any desktop, laptop, or mobile browser via HTTP/HTTPS."],
        ["Multi-User Support", "Single user only; no collaborative logging.", "Multi-member support with Admin and Member role differentiation."],
        ["Data Security", "No encryption; plaintext or unencrypted files.", "BCrypt password hashing, session isolation, and secure server-side state."],
        ["Budget Overrun Alerts", "Manual calculation required; easily overlooked.", "Real-time visual progress bars with category budget limit warnings."],
        ["Debt / Udhar Ledger", "Scattered sticky notes or messy notebook margins.", "Dedicated Udhar module tracking 'Lene Hai' vs 'Dene Hai' with partial payments."],
        ["Recurring Automation", "Must be manually re-written each month.", "Automated day-of-month scheduling for recurring earnings and expenses."],
        ["Report Generation", "Tedious manual plotting in Excel.", "One-click QuestPDF report generation and instant CSV spreadsheet download."],
        ["Disaster Recovery", "Zero automated backup; risk of permanent loss.", "Instant full-fidelity JSON database snapshot export and single-click restoration."]
    ]
    add_custom_table(comp_headers, comp_data, col_widths=[1.5, 2.3, 2.7])

    doc.add_page_break()

    # ==========================================
    # CHAPTER 4: FEASIBILITY STUDY
    # ==========================================
    add_h1("Chapter 4: Feasibility Study")

    add_h2("4.1 Technical Feasibility")
    add_p(
        "Technical feasibility evaluates whether the proposed solution can be constructed, deployed, and maintained with currently available "
        "hardware, software, and development expertise. The project leverages Microsoft .NET 10.0 and ASP.NET Core, the premier cross-platform "
        "framework for robust web applications."
    )
    add_bullet("Platform & Framework: ASP.NET Core 10.0 provides asynchronous request handling, built-in dependency injection, and high throughput on Kestrel server.")
    add_bullet("Database Management: MySQL / MariaDB via Pomelo Entity Framework Core 9.0 delivers ACID compliance, automated migrations, and high query performance.")
    add_bullet("Frontend Stack: Standard HTML5, CSS3, JavaScript, jQuery, and Bootstrap 5 require no specialized proprietary client software and execute reliably across all modern web browsers.")
    add_bullet("Conclusion: The project is technically highly feasible with zero dependency on experimental or unverified technologies.")

    add_h2("4.2 Operational Feasibility")
    add_p(
        "Operational feasibility assesses whether the software satisfies user requirements and can be seamlessly adopted into daily family routines. "
        "HomeLedger is deliberately designed with an engaging 'HUD Admin' dark UI theme featuring clear iconographic indicators and intuitive terminology "
        "(such as 'Lene Hai' and 'Dene Hai' for debt tracking). All CRUD workflows follow standardized, self-explanatory conventions with instant feedback "
        "via alert badges, requiring zero prior technical training for family members."
    )

    add_h2("4.3 Economic Feasibility")
    add_p(
        "Economic feasibility assesses the cost-to-benefit ratio of developing and operating the system. Because the entire technology stack "
        "is open-source and free from commercial licensing fees (.NET SDK, MySQL Community Edition, QuestPDF Community, Bootstrap, FontAwesome), "
        "development software costs are ₹0. The application can run on modest existing hardware and can be hosted locally or on economical cloud tiers, "
        "yielding exceptionally high returns in terms of avoided financial waste and eliminated late payment penalties."
    )

    add_h2("4.4 Schedule and Behavioral Feasibility")
    add_p(
        "The project was successfully planned, designed, implemented, and verified within the prescribed academic timeline of the BCA (Honours) curriculum. "
        "User testing confirmed enthusiastic acceptance of the dark-mode cyber interface and collaborative family features."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 5: SRS (REQUIREMENTS)
    # ==========================================
    add_h1("Chapter 5: Hardware and Software Requirement Specification")

    add_h2("5.1 Hardware Requirements")
    add_p("The system is engineered to operate efficiently on standard consumer-grade computing hardware:")

    hw_headers = ["Component", "Development Environment", "Client / End-User Environment"]
    hw_data = [
        ["Processor (CPU)", "Intel Core i3 / AMD Ryzen 3 (Quad Core, 2.4 GHz+)", "Dual Core 1.5 GHz+ (Desktop, Laptop, or Smartphone)"],
        ["System Memory (RAM)", "8 GB DDR4 (16 GB Recommended)", "2 GB RAM minimum (4 GB recommended)"],
        ["Hard Disk Storage", "10 GB free SSD storage space", "500 MB free browser cache space"],
        ["Display Resolution", "1920 × 1080 Full HD monitor", "1024 × 768 minimum (Responsive for mobile screens)"],
        ["Network Interface", "Standard LAN / Wi-Fi adapter (10 Mbps+)", "Standard Internet / Intranet Wi-Fi connection"]
    ]
    add_custom_table(hw_headers, hw_data, col_widths=[1.5, 2.5, 2.5])

    add_h2("5.2 Software Requirements")
    add_p("The software ecosystem consists of robust, widely supported developer tooling and standard web runtimes:")

    sw_headers = ["Software Layer", "Technology / Specification", "Purpose"]
    sw_data = [
        ["Operating System", "Microsoft Windows 10 / 11 (64-bit) / Linux", "Host Operating System for Development & Server"],
        ["Web Framework", "ASP.NET Core 10.0 (C# 13 / .NET 10.0)", "Server-side MVC Web Application Framework"],
        ["Database Engine", "MySQL Server 8.0 / 9.0 (via XAMPP)", "Relational Database Management System"],
        ["ORM", "Entity Framework Core 9.0 (Pomelo MySQL)", "Object-Relational Mapping & Database Migrations"],
        ["Development IDE", "Visual Studio 2022 / Visual Studio Code", "Integrated Development Environment for Coding & Debugging"],
        ["Client Web Browser", "Microsoft Edge, Google Chrome, Mozilla Firefox", "User interface rendering and client-side execution"]
    ]
    add_custom_table(sw_headers, sw_data, col_widths=[1.5, 2.5, 2.5])

    add_h2("5.3 External NuGet Packages and Libraries")
    add_bullet("BCrypt.Net-Next (v4.2.0): Enterprise cryptographic password hashing algorithm with salted key stretching.")
    add_bullet("Pomelo.EntityFrameworkCore.MySql (v9.0.0): Highly optimized MySQL driver for Entity Framework Core.")
    add_bullet("Microsoft.EntityFrameworkCore.Tools (v9.0.0): CLI tooling for scaffolding, snapshot management, and database migrations.")
    add_bullet("QuestPDF (v2026.8.0): High-performance C# library for generating PDF financial statements with vector typography.")
    add_bullet("Bootstrap 5 & FontAwesome 6: Responsive CSS grid system, UI modals, and high-tech vector iconography.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 6: SYSTEM ARCHITECTURE & FOLDER STRUCTURE
    # ==========================================
    add_h1("Chapter 6: System Architecture & Project Folder Structure")

    add_h2("6.1 MVC Architectural Pattern")
    add_p(
        "The Family Finance Management System is constructed using Microsoft's recommended Model-View-Controller (MVC) architectural pattern. "
        "This structural separation of concerns ensures high maintainability, testability, and clean code organization:"
    )
    add_bullet("Model Layer: Represents the core business entities and database tables (Income, Expense, Budget, Udhar, Family, Member, etc.) as strongly-typed C# classes, along with validation attributes.")
    add_bullet("View Layer: Comprises Razor view templates (.cshtml) executing on the server to render interactive HTML, styled with custom HUD Cyberpunk CSS and Bootstrap components.")
    add_bullet("Controller Layer: Handles incoming HTTP requests, enforces session-based authentication, coordinates database operations via AppDbContext, and routes results to appropriate views or file downloads.")

    add_h2("6.2 Project Folder Structure Breakdown")
    add_p("The solution follows a well-organized directory taxonomy within the FinanceManagementNet project:")

    dir_headers = ["Directory / File", "Type", "Detailed Description & Responsibility"]
    dir_data = [
        ["Controllers/", "Folder", "Contains 14 C# Controller classes orchestrating application logic (Account, Home, Income, Expense, Budget, Category, Member, Udhar, Reminder, Report, Backup, etc.)."],
        ["Models/", "Folder", "Houses domain entity definitions (Family, Member, Income, Expense, Budget, SavingsGoal, Udhar, Reminder) and ViewModels (DashboardViewModel, MonthlyReportViewModel)."],
        ["Views/", "Folder", "Contains Razor view subdirectories organized per controller, plus Views/Shared/ for master layouts (_Layout.cshtml) and partial views."],
        ["Data/", "Folder", "Encapsulates AppDbContext.cs, configuring Entity Framework DbSet collections and relational mappings."],
        ["Migrations/", "Folder", "Contains Entity Framework database migration snapshots and SQL schema version tracking scripts."],
        ["wwwroot/css/", "Folder", "Stores static site stylesheets including site.css featuring the custom HUD Admin cyberpunk dark theme."],
        ["wwwroot/js/", "Folder", "Contains client-side JavaScript scripts (site.js) for search filtering and modal interactions."],
        ["wwwroot/lib/", "Folder", "Client-side vendor libraries (Bootstrap 5, jQuery 3.6, jQuery Validation)."],
        ["appsettings.json", "Config", "Application configuration storing the MySQL connection string and logging verbosity settings."],
        ["Program.cs", "Entrypoint", "Main application bootstrapping file configuring DI services, DB context, HTTP pipeline, session, and routing."]
    ]
    add_custom_table(dir_headers, dir_data, col_widths=[1.8, 0.8, 3.9])

    add_h2("6.3 Complete Solution Directory Hierarchy Tree View")
    add_p(
        "Below is the complete architectural directory tree representation of the Family Finance Management System solution, "
        "detailing the functional responsibility and component mapping of every controller, model, view, database context, and asset directory:"
    )

    p_tree_img = doc.add_paragraph()
    p_tree_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tree_img.paragraph_format.space_before = Pt(8)
    p_tree_img.paragraph_format.space_after = Pt(4)
    p_tree_img.paragraph_format.keep_with_next = True
    if os.path.exists("report_assets/folder_structure.png"):
        p_tree_img.add_run().add_picture("report_assets/folder_structure.png", width=Inches(5.7))

    p_tree_cap = doc.add_paragraph()
    p_tree_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tree_cap.paragraph_format.space_before = Pt(2)
    p_tree_cap.paragraph_format.space_after = Pt(12)
    r_c = p_tree_cap.add_run("Figure 6.1: Complete Project Directory Hierarchy & Component Mapping")
    r_c.bold = True
    r_c.font.size = Pt(10)
    r_c.font.color.rgb = COLOR_PRIMARY

    doc.add_page_break()

    # ==========================================
    # CHAPTER 7: CORE MODULES
    # ==========================================
    add_h1("Chapter 7: Core Modules & Functionality")

    add_h2("7.1 Authentication & Profile Module (AccountController)")
    add_p(
        "Provides dual-tabbed authentication for Household Administrators and Family Members. Administrators authenticate using their Family ID "
        "and BCrypt-encrypted password. Members authenticate using their Family ID, Member Name, and assigned password. Features full registration, "
        "password reset via security challenge, and secure session state invalidation upon logout."
    )

    add_h2("7.2 Executive Overview Dashboard (HomeController)")
    add_p(
        "The central control terminal of the application. Dynamically computes and displays five real-time Key Performance Indicators (KPIs): "
        "Remaining Balance, Total Income, Total Expense, To Receive (Lene Hai), and To Pay (Dene Hai). Also displays a real-time stream of the "
        "most recent transactions with badge color indicators and quick action shortcuts."
    )

    add_h2("7.3 Family Member Directory Module (MemberController)")
    add_p(
        "Enables Household Administrators to register, edit, and manage all family members participating in the ledger. Stores member names, "
        "familial relationships (Head, Wife, Son, Daughter, Parent), mobile numbers, profile photos, and independent login credentials."
    )

    add_h2("7.4 Income Ledger Module (IncomeController)")
    add_p(
        "Maintains a comprehensive historical ledger of all incoming funds. Records date, receiving member, income source (Salary, Investment, "
        "Freelance), amount, and detailed description. Features full-text search filtering, record editing, deletion, instant CSV spreadsheet "
        "download, and vector PDF export."
    )

    add_h2("7.5 Expense Tracking Module (ExpenseController)")
    add_p(
        "Tracks all domestic expenditures against customized categories. Features date logging, member attribution, category assignment, "
        "detailed expense notes, instant search, and export to CSV/PDF."
    )

    add_h2("7.6 Financial Categories Console (CategoryController)")
    add_p(
        "Allows customization of the household's financial taxonomy. Supports creating income and expense categories, custom color pickers, "
        "and FontAwesome vector icons to provide vivid visual distinction across dashboards and reports."
    )

    add_h2("7.7 Monthly Budget Planning Module (BudgetController)")
    add_p(
        "Empowers families to enforce fiscal discipline by defining monthly expenditure limits for specific categories (e.g., Groceries: ₹10,000, "
        "Entertainment: ₹5,000). Provides visual progress indicators comparing allocated budgets against actual monthly spend."
    )

    add_h2("7.8 Recurring Income & Expense Automation Modules")
    add_p(
        "Eliminates repetitive monthly data entry by defining automated recurring streams (monthly company salaries, rental yields, broadband subscriptions, "
        "gym memberships, school tuition). Supports customizable frequencies and target billing days."
    )

    add_h2("7.9 Savings Goals & Milestone Tracker (SavingsGoalController)")
    add_p(
        "Motivates long-term wealth accumulation by tracking dedicated savings targets (Emergency Fund, Home Renovation, Vacation). Features target "
        "dates, target capital, incremental fund deposit dialogs ('Add Amount'), and percentage completion progress bars."
    )

    add_h2("7.10 Udhar / Debt & Loan Ledger (UdharController)")
    add_p(
        "A culturally adapted domestic module tracking bilateral loans. Differentiates between money owed to the family ('Lene Hai' / Receivables) "
        "and money borrowed ('Dene Hai' / Payables). Supports recording partial repayments, calculating remaining balances, and tracking clearance status."
    )

    add_h2("7.11 Due Date Reminder Module (ReminderController)")
    add_p(
        "Maintains an interactive calendar of upcoming financial deadlines (utility bills, insurance premiums, SIP dates). Highlights pending "
        "and approaching deadlines to safeguard against penalty fees."
    )

    add_h2("7.12 Analytical Reports & QuestPDF Module (ReportController)")
    add_p(
        "Generates deep financial intelligence including Monthly Breakdown Reports (with category percentage distributions and net balances) "
        "and 12-month Annual Financial Performance Overviews, with on-demand QuestPDF document generation."
    )

    add_h2("7.13 Database Backup & Disaster Recovery (BackupController)")
    add_p(
        "Provides ironclad data resilience. Serializes all 11 database tables belonging to the family into a structured JSON backup file for instant "
        "download. Enables complete single-click database restoration from any previously exported backup file."
    )

    doc.add_page_break()

    # ==========================================
    # CHAPTER 8: DATABASE DESIGN
    # ==========================================
    add_h1("Chapter 8: Database Design, Schema & Data Dictionary")

    add_h2("8.1 Database Architecture Overview")
    add_p(
        "The relational database family_finance is hosted on MySQL/MariaDB and managed via Entity Framework Core 9.0 code-first migrations. "
        "The schema is fully normalized to Third Normal Form (3NF), ensuring data integrity, elimination of update anomalies, and strict family isolation."
    )

    add_h2("8.2 Data Dictionary (Table Specifications)")

    # Table 1: families
    add_h3("Table 8.1: families (Household Master Table)")
    t_fam = [
        ["id", "INT(11)", "NO", "Primary Key (Auto Increment)", "Unique internal family database identifier."],
        ["family_name", "VARCHAR(100)", "NO", "--", "Display name of the household (e.g., 'Rana Family')."],
        ["family_id", "VARCHAR(50)", "NO", "Unique Key", "Alphanumeric unique login username (e.g., 'admin')."],
        ["password", "VARCHAR(255)", "NO", "--", "BCrypt encrypted cryptographic password hash."],
        ["created_at", "DATETIME", "NO", "Default NOW()", "Timestamp of family registration."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_fam, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 2: members
    add_h3("Table 8.2: members (Family Members Table)")
    t_mem = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique identifier for member."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["member_name", "VARCHAR(100)", "NO", "--", "Full name of the family member."],
        ["relation", "VARCHAR(50)", "NO", "--", "Domestic relationship (Head, Wife, Son, etc.)."],
        ["mobile", "VARCHAR(15)", "YES", "--", "Contact mobile telephone number."],
        ["profile_image", "VARCHAR(255)", "YES", "--", "File path or URL of member avatar."],
        ["Password", "VARCHAR(255)", "YES", "--", "Member login password hash."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_mem, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 3: income
    add_h3("Table 8.3: income (Income Ledger Table)")
    t_inc = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique identifier for income record."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["member_name", "VARCHAR(100)", "NO", "--", "Name of earning family member."],
        ["amount", "DECIMAL(10,2)", "NO", "--", "Monetary sum received in INR."],
        ["source", "VARCHAR(100)", "NO", "--", "Source of income (Salary, Consulting, etc.)."],
        ["date", "DATE", "NO", "--", "Transaction execution date."],
        ["description", "TEXT", "YES", "--", "Detailed notes describing the transaction."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_inc, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 4: expenses
    add_h3("Table 8.4: expenses (Expense Tracking Table)")
    t_exp = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique identifier for expense record."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["member_name", "VARCHAR(100)", "NO", "--", "Name of spending family member."],
        ["category", "VARCHAR(50)", "NO", "--", "Category classification (Groceries, etc.)."],
        ["amount", "DECIMAL(10,2)", "NO", "--", "Expenditure amount in INR."],
        ["description", "TEXT", "YES", "--", "Explanatory remarks or vendor details."],
        ["date", "DATE", "NO", "--", "Date of expenditure."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_exp, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 5: budgets
    add_h3("Table 8.5: budgets (Monthly Category Budget Caps)")
    t_bud = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique budget record identifier."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["category", "VARCHAR(50)", "NO", "--", "Budgeted expense category name."],
        ["amount", "DECIMAL(10,2)", "NO", "--", "Allocated spending limit amount."],
        ["month", "VARCHAR(7)", "NO", "--", "Budget target period in 'YYYY-MM' format."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_bud, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 6: savings_goals
    add_h3("Table 8.6: savings_goals (Savings Targets Table)")
    t_sav = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique savings goal identifier."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["goal_name", "VARCHAR(150)", "NO", "--", "Title of savings goal (e.g., Emergency Fund)."],
        ["target_amount", "DECIMAL(10,2)", "NO", "--", "Target financial capital goal in INR."],
        ["current_amount", "DECIMAL(10,2)", "NO", "--", "Currently accumulated funds."],
        ["target_date", "DATE", "NO", "--", "Target completion deadline date."],
        ["description", "LONGTEXT", "YES", "--", "Detailed description of purpose."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_sav, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 7: udhar
    add_h3("Table 8.7: udhar (Debt & Loan Ledger Table)")
    t_udh = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique debt ledger record identifier."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["person_name", "VARCHAR(100)", "NO", "--", "Name of external debtor / creditor."],
        ["member_name", "VARCHAR(100)", "YES", "--", "Family member who transacted."],
        ["type", "ENUM", "NO", "'Lene Hai', 'Dene Hai'", "'Lene Hai' = Receivable; 'Dene Hai' = Payable."],
        ["amount", "DECIMAL(10,2)", "NO", "--", "Original principal debt amount."],
        ["paid_amount", "DECIMAL(10,2)", "YES", "Default 0.00", "Amount paid or recovered to date."],
        ["remaining_amount", "DECIMAL(10,2)", "NO", "--", "Outstanding balance due."],
        ["status", "ENUM", "YES", "'Pending', 'Completed'", "Current debt settlement status."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_udh, [1.2, 1.1, 0.6, 1.6, 2.0])

    # Table 8: reminders
    add_h3("Table 8.8: reminders (Payment Reminders Table)")
    t_rem = [
        ["id", "INT(11)", "NO", "Primary Key", "Unique reminder record identifier."],
        ["family_id", "INT(11)", "NO", "Foreign Key -> families(id)", "Associated family reference."],
        ["title", "VARCHAR(150)", "NO", "--", "Title of bill / event reminder."],
        ["date", "DATE", "NO", "--", "Due date / deadline for payment."],
        ["description", "TEXT", "YES", "--", "Additional payment notes or reference numbers."]
    ]
    add_custom_table(["Field Name", "Data Type", "Null", "Key / Constraint", "Description"], t_rem, [1.2, 1.1, 0.6, 1.6, 2.0])

    doc.add_page_break()

    # ==========================================
    # CHAPTER 9: SCREENSHOTS & UI WALKTHROUGH
    # ==========================================
    add_h1("Chapter 9: System Screenshots & User Interface Walkthrough")
    add_p(
        "This chapter presents high-resolution screenshots of every functional screen within the Family Finance Management System (HomeLedger). "
        "Each screen is captured from the live application running with real household financial data, accompanied by its route identifier, "
        "a structural breakdown of its visual components, and an explanation of the underlying operational workflow."
    )

    # 29 Screenshots
    screens_meta = [
        (
            "report_assets/screenshots/01_login_admin.png",
            "9.1",
            "Household Administrator Authentication Portal",
            "/Account/Login",
            "The primary secure entry point for Family Administrators. The interface features a dark cybernetic HUD card with custom corner notches. "
            "Administrators enter their registered alphanumeric Family ID and password. Clicking 'Login as Admin' verifies credentials against the "
            "database using BCrypt hashing and initializes an authenticated session with administrative privileges. Links for password recovery and "
            "new family registration are conveniently positioned below the form."
        ),
        (
            "report_assets/screenshots/02_login_member.png",
            "9.2",
            "Family Member Dedicated Login Portal",
            "/Account/Login#memberTab",
            "Toggling the 'Member Login' tab transforms the login interface to facilitate independent access for enrolled household members. "
            "In addition to the Family ID, members supply their unique Member Name and private password. This role-differentiated authentication "
            "allows individual members to record transactions without exposing administrative controls such as database backup or member deletion."
        ),
        (
            "report_assets/screenshots/03_register.png",
            "9.3",
            "New Family Account Registration Interface",
            "/Account/Register",
            "Enables new households to onboard onto the HomeLedger platform. The registration form captures the Family Name (e.g., 'Rana Family'), "
            "a globally unique Family ID, and secure password confirmation. Server-side model validation verifies password strength (minimum 6 characters) "
            "and confirms that the chosen Family ID does not conflict with existing records before creating the family database entity."
        ),
        (
            "report_assets/screenshots/04_forgot_password.png",
            "9.4",
            "Family Password Recovery & Reset Interface",
            "/Account/ForgotPassword",
            "A self-service credential recovery workflow. Administrators who forget their access credentials input their Family ID. The system validates "
            "the existence of the household in the database and securely transitions the user to the Reset Password interface where a new cryptographic "
            "password hash can be established."
        ),
        (
            "report_assets/screenshots/05_dashboard.png",
            "9.5",
            "Executive Overview Financial Dashboard",
            "/Home/Dashboard",
            "The primary command center of HomeLedger. The dashboard aggregates real-time metrics across all household accounts and renders five glowing KPI cards: "
            "(1) Remaining Balance (₹73,200.00), (2) Total Income (₹1,00,000.00), (3) Total Expense (₹26,800.00), (4) To Receive via Udhar (₹10,000.00), and "
            "(5) To Pay via Udhar (₹5,000.00). Beneath the metrics grid, an interactive 'Recent Activities' table displays the latest inflows and outflows with "
            "distinct colored badges (Green for Income, Coral for Expense), providing immediate transparency."
        ),
        (
            "report_assets/screenshots/06_income_list.png",
            "9.6",
            "Income Management Ledger & Export Hub",
            "/Income/Index",
            "Displays the exhaustive history of all earnings credited to the household. The data grid presents Transaction Date, Earning Member Name, "
            "Source (e.g., Tech Solutions Salary, Design Consulting), Credited Amount in green monospace font, and detailed remarks. The top action bar "
            "includes an instant full-text search filter, a quick 'Add Income' shortcut, and single-click buttons for 'Export CSV' and 'Export PDF'."
        ),
        (
            "report_assets/screenshots/07_income_create.png",
            "9.7",
            "Add New Income Record Form",
            "/Income/Create",
            "A streamlined data entry form for recording new revenues. Household members select their name from a dynamic family dropdown, input the exact "
            "amount in INR, specify the revenue source (Salary, Investment, Bonus, Freelance), pick the transaction date, and provide contextual notes. "
            "Client-side unobtrusive validation prevents empty or negative value submissions."
        ),
        (
            "report_assets/screenshots/08_expense_list.png",
            "9.8",
            "Expense Management & Expenditure Ledger",
            "/Expense/Index",
            "The central expenditure ledger detailing all household outflows. Each entry exhibits the transaction date, responsible family member, "
            "classified category (Groceries, Utilities, Education, Entertainment), debit amount in coral red, and itemized description. Action buttons "
            "allow authorized members to edit records or remove erroneous entries, with immediate recalculation of the master balance."
        ),
        (
            "report_assets/screenshots/09_expense_create.png",
            "9.9",
            "Add New Household Expense Form",
            "/Expense/Create",
            "The recording interface for household expenses. Incorporates dynamic dropdown pickers populated directly from the family's registered "
            "member directory and active categories. Captures precise financial debits, purchase dates, and comprehensive receipt descriptions."
        ),
        (
            "report_assets/screenshots/10_category_list.png",
            "9.10",
            "Financial Categories Management Console",
            "/Category/Index",
            "Manages the household's custom categorization schema. Displays active categories partitioned into Income and Expense classifications, "
            "accompanied by personalized color indicators (e.g., Cyan for Salary, Coral for Utilities, Purple for Education) and custom vector icons. "
            "Allows administrators to modify classification names or delete obsolete tags."
        ),
        (
            "report_assets/screenshots/11_category_create.png",
            "9.11",
            "Create Custom Financial Category Form",
            "/Category/Create",
            "Enables users to expand their financial taxonomy. The form accepts a category title, transaction type selector (Income vs. Expense), "
            "a visual color picker for chart representation, and an icon selector. This flexibility allows each family to tailor tracking to their unique lifestyle."
        ),
        (
            "report_assets/screenshots/12_budget_list.png",
            "9.12",
            "Monthly Budget Allocation & Spending Limits",
            "/Budget/Index",
            "The fiscal discipline center of the application. Lists defined category expenditure thresholds for the active billing cycle (e.g., Groceries: "
            "₹10,000.00, Utilities: ₹5,000.00, Education: ₹15,000.00). Provides instant comparison against actual outlays to alert users before budget overruns occur."
        ),
        (
            "report_assets/screenshots/13_budget_create.png",
            "9.13",
            "Define New Category Budget Limit Form",
            "/Budget/Create",
            "Allows administrators to establish strict monthly ceilings for specific expenditure categories. Accepts category selection, maximum spending threshold, "
            "and billing month specification in YYYY-MM format."
        ),
        (
            "report_assets/screenshots/14_recurring_income_list.png",
            "9.14",
            "Recurring Income Streams Management Console",
            "/RecurringIncome/Index",
            "Automates routine incoming cash flows. Displays scheduled earnings (such as monthly company salaries and recurring rental yields) with their "
            "designated frequency, execution day-of-month, amount, and active automation status switch."
        ),
        (
            "report_assets/screenshots/15_recurring_income_create.png",
            "9.15",
            "Setup Automated Recurring Income Form",
            "/RecurringIncome/Create",
            "Configuration portal for recurring revenues. Captures member attribution, income stream title, recurring amount, payment cycle frequency (Monthly, "
            "Quarterly, Annually), and the day of the month when funds are credited."
        ),
        (
            "report_assets/screenshots/16_recurring_expense_list.png",
            "9.16",
            "Recurring Expenses & Subscriptions Manager",
            "/RecurringExpense/Index",
            "Tracks non-negotiable scheduled outflows such as broadband subscriptions, electricity bills, and insurance premiums. Ensures recurring domestic "
            "obligations are factored into forward-looking monthly budget allocations."
        ),
        (
            "report_assets/screenshots/17_recurring_expense_create.png",
            "9.17",
            "Setup Automated Recurring Expense Form",
            "/RecurringExpense/Create",
            "Data entry screen for scheduling automated bills and subscriptions. Binds the recurring outflow to a designated category and sets the execution "
            "calendar day to prevent billing oversights."
        ),
        (
            "report_assets/screenshots/18_savings_goal_list.png",
            "9.18",
            "Savings Goals & Milestone Accumulation Tracker",
            "/SavingsGoal/Index",
            "A visual wealth-building console. Displays active savings initiatives as interactive cards (e.g., Emergency Reserve Fund: 63.3% progress, ₹95,000 "
            "saved of ₹1,50,000; Home Renovation: 30% progress, ₹60,000 saved of ₹2,00,000). Features gradient progress bars, remaining target amounts, target "
            "deadlines, and a dedicated 'Add Amount' button for incremental deposits."
        ),
        (
            "report_assets/screenshots/19_savings_goal_create.png",
            "9.19",
            "Establish New Savings Goal Form",
            "/SavingsGoal/Create",
            "Creates new savings targets. Users define the milestone objective, target capital requirement, initial starting balance, target completion date, "
            "and motivational purpose."
        ),
        (
            "report_assets/screenshots/20_udhar_list.png",
            "9.20",
            "Udhar / Debt & Bilateral Loan Ledger",
            "/Udhar/Index",
            "A specialized ledger tracking informal domestic debt obligations. Clearly differentiates between 'Lene Hai' (Receivables owed to the family by "
            "external parties) and 'Dene Hai' (Payables owed by the family). Tracks borrower name, principal amount, paid recovery sum, remaining outstanding "
            "balance, and settlement status (Pending vs. Completed)."
        ),
        (
            "report_assets/screenshots/21_udhar_create.png",
            "9.21",
            "Record New Udhar / Loan Transaction Form",
            "/Udhar/Create",
            "Captures the specifics of newly issued or borrowed funds. Records party name, transacting family member, debt nature ('Lene Hai' vs 'Dene Hai'), "
            "monetary sum, transaction date, underlying loan reason, and optional receipt proof upload."
        ),
        (
            "report_assets/screenshots/22_reminder_list.png",
            "9.22",
            "Payment Due Date Reminders & Alerts Console",
            "/Reminder/Index",
            "An interactive calendar notification console tracking imminent domestic payment obligations (e.g., Torrent Power electricity due date, JioFiber "
            "broadband renewal). Prevents costly service disconnections and late penalty fees."
        ),
        (
            "report_assets/screenshots/23_reminder_create.png",
            "9.23",
            "Schedule Payment Reminder Form",
            "/Reminder/Create",
            "Form to register upcoming payment deadlines. Accepts an alert title, statutory due date, and detailed instructions (account numbers, payment URLs)."
        ),
        (
            "report_assets/screenshots/24_report_hub.png",
            "9.24",
            "Financial Reports Navigation Hub",
            "/Report/Index",
            "Central portal for generating business intelligence and financial audits. Offers quick selectors for generating detailed Monthly Breakdown Reports "
            "by Year/Month or comprehensive 12-Month Annual Financial Performance Statements."
        ),
        (
            "report_assets/screenshots/25_report_monthly.png",
            "9.25",
            "Comprehensive Monthly Financial Breakdown Report",
            "/Report/MonthlyReport?year=2026&month=10",
            "An analytical executive summary for a selected billing cycle (e.g., October 2026). Displays top-level KPI cards for Total Income (₹1,00,000.00), "
            "Total Expenses (₹26,800.00), and Net Balance (₹73,200.00). Presents a Category-Wise Expense table calculating exact expenditure percentages "
            "(Groceries 31.7%, Education 44.8%, Entertainment 13.1%, Utilities 10.4%) alongside recent itemized transactions."
        ),
        (
            "report_assets/screenshots/26_report_yearly.png",
            "9.26",
            "Annual Financial Performance & Cash Flow Report",
            "/Report/YearlyReport?year=2026",
            "Provides full-year macro financial analysis. Features an annual cash flow matrix summarizing monthly income, expenditures, and net surplus/deficit "
            "across all 12 calendar months, enabling long-term family wealth planning and tax preparation."
        ),
        (
            "report_assets/screenshots/27_member_list.png",
            "9.27",
            "Family Members Directory & Access Management",
            "/Member/Index",
            "Displays all registered household members enrolled under the family account (e.g., Harshiddh Rana - Head, Priya Rana - Wife, Aarav Rana - Son), "
            "their assigned roles, and registered mobile telephone numbers. Administrators can edit profile credentials or remove inactive accounts."
        ),
        (
            "report_assets/screenshots/28_member_create.png",
            "9.28",
            "Enroll New Family Member Form",
            "/Member/Create",
            "Administrative form for adding new members to the household ledger. Captures member full name, domestic relation, mobile contact, avatar photo, "
            "and private member password for independent login."
        ),
        (
            "report_assets/screenshots/29_backup_index.png",
            "9.29",
            "Database Backup, JSON Export & Disaster Recovery Console",
            "/Backup/Index",
            "The data safety and resilience console. Provides a prominent 'Download JSON Backup' button that serializes all 11 relational database tables into "
            "an indented JSON snapshot. Also contains a file upload input to import and restore previous backups, guaranteeing zero risk of permanent data loss."
        )
    ]

    for img_path, f_num, f_title, f_route, f_desc in screens_meta:
        add_screenshot_figure(img_path, f_num, f_title, f_route, f_desc)

    doc.add_page_break()

    # ==========================================
    # CHAPTER 10: LIMITATIONS
    # ==========================================
    add_h1("Chapter 10: Limitations of the System")
    add_p(
        "While the Family Finance Management System (HomeLedger) successfully satisfies its core functional objectives, several operational "
        "and technical boundaries exist within the current version:"
    )
    add_bullet("Absence of Direct Open Banking API Integration: The current version relies on user input for logging transactions rather than automatically scraping bank accounts. This design preserves user privacy and eliminates reliance on costly banking aggregators, but requires routine manual logging.")
    add_bullet("Single Default Currency: The application currently operates with Indian Rupees (₹) as the primary base currency. While suitable for domestic Indian households, multi-currency conversion for international travel or NRI family members is not dynamically supported.")
    add_bullet("Network / Intranet Dependency: As an ASP.NET Core web application, client devices require network connectivity to the hosting server to record transactions. An offline progressive web app (PWA) cache is not yet implemented.")
    add_bullet("Manual Receipt Attachment: Document proofs for Udhar and expenses require manual user upload rather than automated optical character recognition (OCR) parsing from physical receipt photographs.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 11: FUTURE ENHANCEMENTS
    # ==========================================
    add_h1("Chapter 11: Future Enhancements")
    add_p(
        "To build upon the successful foundation established in this version, several promising enhancements are planned for future iterations:"
    )
    add_bullet("Native Mobile Applications (Flutter / .NET MAUI): Developing cross-platform iOS and Android mobile companion apps with biometric login (fingerprint/Face ID) and push notifications for instant receipt logging on the go.")
    add_bullet("Account Aggregator & UPI Webhook Integration: Integrating with RBI-approved Account Aggregator frameworks to securely ingest verified bank statement feeds with explicit user consent.")
    add_bullet("AI-Driven Financial Advisor & Spending Forecasts: Incorporating machine learning models to analyze multi-month spending patterns, predict end-of-month cash balances, and suggest actionable cost reductions.")
    add_bullet("Intelligent OCR Receipt Scanner: Implementing Tesseract OCR or Azure Computer Vision to automatically extract merchant name, transaction date, and total amount from photographed shopping bills.")
    add_bullet("Automated WhatsApp & SMS Due Date Alerts: Connecting Twilio or WhatsApp Business API webhooks to dispatch automated due date reminders directly to family members' mobile phones.")

    doc.add_page_break()

    # ==========================================
    # CHAPTER 12: REFERENCES & BIBLIOGRAPHY
    # ==========================================
    add_h1("Chapter 12: References & Bibliography")

    add_h2("12.1 Academic Textbooks & Literature")
    add_bullet("Troelsen, Andrew, and Philip Japikse. Pro C# 10 with .NET 6 / .NET 10: Foundational Principles and Practices in Programming. Apress, 2022.")
    add_bullet("Freeman, Adam. Pro ASP.NET Core 6: Developing Real-World Web Applications in .NET. Apress, 2022.")
    add_bullet("Silberschatz, Abraham, Henry F. Korth, and S. Sudarshan. Database System Concepts. 7th ed., McGraw-Hill Education, 2019.")
    add_bullet("Pressman, Roger S., and Bruce R. Maxim. Software Engineering: A Practitioner's Approach. 9th ed., McGraw-Hill, 2020.")

    add_h2("12.2 Technical Documentation & Specifications")
    add_bullet("Microsoft Corporation. 'ASP.NET Core MVC Documentation.' Microsoft Learn, https://learn.microsoft.com/aspnet/core/mvc/")
    add_bullet("Pomelo Foundation. 'Pomelo.EntityFrameworkCore.MySql Driver Specification.' GitHub, https://github.com/PomeloFoundation/Pomelo.EntityFrameworkCore.MySql")
    add_bullet("QuestPDF Documentation. 'QuestPDF: Open-Source .NET Library for PDF Generation.' https://www.questpdf.com/")
    add_bullet("Bootstrap Core Team. 'Bootstrap 5 Responsive Grid & Components.' https://getbootstrap.com/docs/5.3/")
    add_bullet("MySQL AB & Oracle Corporation. 'MySQL 8.0 Reference Manual.' https://dev.mysql.com/doc/refman/8.0/en/")

    # Save document
    output_path = r"c:\Users\Rana Harshiddh\Desktop\Family-Finance-Management-main\Family_Finance_Management_Project_Report.docx"
    doc.save(output_path)
    print(f"Report saved successfully to: {output_path}")

if __name__ == "__main__":
    create_report()
