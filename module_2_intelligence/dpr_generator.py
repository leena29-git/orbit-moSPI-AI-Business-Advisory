import os
from typing import Dict, Any
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from .scheme_matcher import SchemeMatcher


class DPRGenerator:
    @staticmethod
    def generate_dpr_data(profile: Dict[str, Any], hldi_output: Dict[str, Any]) -> Dict[str, Any]:
        scheme_info = SchemeMatcher.match_scheme(profile)
        capital = float(profile.get("capital_available", 0))
        monthly_expense = float(profile.get("expenses", 0))
        total_project_cost = capital + (monthly_expense * 6)
        loan_requested = max(0.0, total_project_cost - capital)

        dpr_id = f"DPR_{profile.get('profile_id', 'TMP')}_{profile.get('district_id', 'GEN')}"

        return {
            "dpr_id": dpr_id,
            "profile_id": profile.get("profile_id"),
            "district_id": profile.get("district_id"),
            "block_id": profile.get("block_id"),
            "business_type": profile.get("business_type"),
            "trade_skill": profile.get("trade_skill", "General"),
            "matched_scheme": scheme_info["matched_scheme"],
            "scheme_details": scheme_info,
            "financial_breakdown": {
                "promoter_contribution": capital,
                "estimated_working_capital_6m": monthly_expense * 6,
                "total_project_cost": total_project_cost,
                "loan_required": loan_requested
            },
            "hldi_assessment": {
                "hldi_score": hldi_output.get("hldi_score"),
                "feasibility_summary": hldi_output.get("contributing_factors")
            },
            "status": "pending_review"
        }

    @staticmethod
    def export_dpr_pdf(dpr_data: Dict[str, Any], output_path: str) -> str:
        doc = SimpleDocTemplate(output_path, pagesize=letter, rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36)
        styles = getSampleStyleSheet()
        story = []

        title_style = ParagraphStyle(
            'TitleStyle',
            parent=styles['Heading1'],
            fontSize=16,
            textColor=colors.HexColor('#1E3A8A'),
            spaceAfter=10
        )

        story.append(Paragraph("DETAILED PROJECT REPORT (DPR) - PROPOSAL", title_style))
        story.append(Paragraph("<b>Under Ministry of Statistics & Programme Implementation (MoSPI) Advisory Framework</b>", styles['Normal']))
        story.append(Spacer(1, 15))

        summary_table_data = [
            ["DPR Reference ID:", dpr_data.get("dpr_id"), "Target Scheme:", dpr_data.get("matched_scheme")],
            ["Applicant Profile ID:", dpr_data.get("profile_id"), "Proposed Business:", dpr_data.get("business_type").title()],
            ["District / Block:", f"{dpr_data.get('district_id')} / {dpr_data.get('block_id')}", "HLDI Viability Score:", f"{dpr_data['hldi_assessment']['hldi_score']} / 100"]
        ]

        t1 = Table(summary_table_data, colWidths=[120, 150, 120, 150])
        t1.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F3F4F6')),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#111827')),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t1)
        story.append(Spacer(1, 15))

        fin = dpr_data["financial_breakdown"]
        story.append(Paragraph("<b>Financial Appraisal & Loan Structuring</b>", styles['Heading3']))
        fin_data = [
            ["Item Description", "Amount (INR)"],
            ["Promoter's Own Contribution (Capital Available)", f"₹ {fin['promoter_contribution']:,.2f}"],
            ["Estimated 6-Month Working Capital / Setup", f"₹ {fin['estimated_working_capital_6m']:,.2f}"],
            ["Total Project Cost", f"₹ {fin['total_project_cost']:,.2f}"],
            ["Net Loan Assistance Requested", f"₹ {fin['loan_required']:,.2f}"]
        ]
        t2 = Table(fin_data, colWidths=[340, 200])
        t2.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1E3A8A')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#D1D5DB')),
            ('PADDING', (0, 0), (-1, -1), 6),
        ]))
        story.append(t2)
        story.append(Spacer(1, 15))

        story.append(Paragraph("<b>MoSPI Grounded Feasibility Summary</b>", styles['Heading3']))
        story.append(Paragraph(dpr_data['hldi_assessment']['feasibility_summary'], styles['Normal']))
        story.append(Spacer(1, 15))

        sign_box = [
            ["Officer Recommendation:", "Status: [ PENDING VERIFICATION ]"],
            ["Verification Notes:", "Authorized Bank / Nodal Officer Signature: __________________"]
        ]
        t3 = Table(sign_box, colWidths=[270, 270])
        t3.setStyle(TableStyle([
            ('LINEABOVE', (0, 0), (-1, -1), 1, colors.HexColor('#9CA3AF')),
            ('PADDING', (0, 0), (-1, -1), 10),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
        ]))
        story.append(t3)

        doc.build(story)
        return output_path