#!/usr/bin/env python3
"""
Traveloka 이메일을 시간순으로 정렬된 PDF로 변환
"""

import json
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.lib import colors
import os
import re

def load_emails_from_json(json_file):
    """JSON 파일에서 이메일 로드"""
    try:
        with open(json_file, 'r', encoding='utf-8') as f:
            emails = json.load(f)
        
        print(f"이메일 로드 완료: {len(emails)}개")
        return emails
    except Exception as e:
        print(f"JSON 파일 로드 오류: {e}")
        return []

def parse_email_date_for_sorting(date_str):
    """정렬을 위한 날짜 파싱"""
    if not date_str:
        return datetime.min
    
    try:
        # 다양한 날짜 형식 처리
        date_str_clean = re.sub(r'\([^)]*\)', '', date_str).strip()
        
        date_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%a, %d %b %Y %H:%M:%S %z",
            "%d %b %Y %H:%M:%S %z",
            "%Y/%m/%d %H:%M:%S"
        ]
        
        for fmt in date_formats:
            try:
                return datetime.strptime(date_str_clean, fmt)
            except:
                continue
        
        # 실패 시 현재 시간 반환
        return datetime.now()
    except:
        return datetime.now()

def sort_emails_by_date(emails):
    """이메일을 날짜순으로 정렬"""
    for email in emails:
        email['parsed_date'] = parse_email_date_for_sorting(email.get('date', ''))
    
    # 날짜순 정렬 (오래된 것부터)
    sorted_emails = sorted(emails, key=lambda x: x['parsed_date'])
    
    # 파싱된 날짜 제거
    for email in sorted_emails:
        email.pop('parsed_date', None)
    
    return sorted_emails

def clean_email_text(text):
    """이메일 텍스트 정리"""
    if not text:
        return ""
    
    # 여러 공백을 하나로
    text = re.sub(r'\s+', ' ', text)
    
    # 특수 문자 처리
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    
    return text.strip()

def create_email_pdf(emails, output_path="traveloka_emails_timeline.pdf"):
    """
    이메일을 시간순으로 정렬된 PDF로 생성
    
    Args:
        emails: 이메일 리스트
        output_path: 출력 PDF 경로
    """
    
    if not emails:
        print("이메일이 없습니다.")
        return None
    
    # 이메일 정렬
    sorted_emails = sort_emails_by_date(emails)
    
    print(f"PDF 생성 중: {output_path}")
    print(f"총 이메일: {len(sorted_emails)}개")
    
    # PDF 문서 생성
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=20*mm,
        leftMargin=20*mm,
        topMargin=20*mm,
        bottomMargin=20*mm
    )
    
    # 스타일 정의
    styles = getSampleStyleSheet()
    
    # 커스텀 스타일
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        spaceAfter=12,
        textColor=colors.HexColor('#1a237e'),
        alignment=1  # 가운데 정렬
    )
    
    subtitle_style = ParagraphStyle(
        'SubtitleStyle',
        parent=styles['Heading2'],
        fontSize=14,
        spaceAfter=18,
        textColor=colors.HexColor('#283593')
    )
    
    date_style = ParagraphStyle(
        'DateStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#546e7a'),
        spaceAfter=6
    )
    
    header_style = ParagraphStyle(
        'HeaderStyle',
        parent=styles['Heading3'],
        fontSize=12,
        textColor=colors.HexColor('#1565c0'),
        spaceAfter=8,
        spaceBefore=12
    )
    
    sender_style = ParagraphStyle(
        'SenderStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#2e7d32'),
        spaceAfter=4
    )
    
    receiver_style = ParagraphStyle(
        'ReceiverStyle',
        parent=styles['Normal'],
        fontSize=11,
        textColor=colors.HexColor('#c62828'),
        spaceAfter=4
    )
    
    subject_style = ParagraphStyle(
        'SubjectStyle',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.black,
        spaceAfter=8,
        backColor=colors.HexColor('#f5f5f5'),
        borderPadding=6,
        borderColor=colors.HexColor('#e0e0e0'),
        borderWidth=1
    )
    
    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontSize=10,
        textColor=colors.HexColor('#424242'),
        spaceAfter=16,
        leading=13
    )
    
    timeline_style = ParagraphStyle(
        'TimelineStyle',
        parent=styles['Normal'],
        fontSize=9,
        textColor=colors.HexColor('#757575'),
        leftIndent=10,
        spaceAfter=4
    )
    
    story = []
    
    # 표지 페이지
    story.append(Spacer(1, 2*inch))
    
    title = Paragraph("Traveloka 지원팀 이메일 기록", title_style)
    story.append(title)
    
    story.append(Spacer(1, 0.5*inch))
    
    # 요약 정보
    summary_text = f"""
    <b>생성일:</b> {datetime.now().strftime('%Y년 %m월 %d일 %H:%M')}<br/>
    <b>총 이메일 수:</b> {len(sorted_emails)}개<br/>
    <b>기간:</b> {sorted_emails[0].get('date', '알 수 없음')} ~ {sorted_emails[-1].get('date', '알 수 없음')}<br/>
    <b>발신자:</b> Traveloka Support &lt;cs@traveloka.com&gt;
    """
    
    summary = Paragraph(summary_text, styles['Normal'])
    story.append(summary)
    
    story.append(PageBreak())
    
    # 목차 페이지
    toc_title = Paragraph("목차", subtitle_style)
    story.append(toc_title)
    story.append(Spacer(1, 0.3*inch))
    
    # 타임라인 목차
    timeline_items = []
    for i, email in enumerate(sorted_emails, 1):
        direction = "➡️ 발신" if email.get('direction') == 'sent' else "⬅️ 수신"
        timeline_items.append([
            str(i),
            email.get('date', '')[:16],
            direction,
            email.get('subject', '제목 없음')[:40] + ('...' if len(email.get('subject', '')) > 40 else '')
        ])
    
    # 목차 테이블
    toc_table = Table(timeline_items, colWidths=[20*mm, 40*mm, 25*mm, 100*mm])
    toc_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e3f2fd')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor('#0d47a1')),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e0e0e0')),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    
    story.append(toc_table)
    story.append(PageBreak())
    
    # 이메일 상세 페이지
    for i, email in enumerate(sorted_emails, 1):
        # 이메일 헤더
        email_header = Paragraph(f"이메일 #{i}", header_style)
        story.append(email_header)
        
        # 날짜
        date_text = f"<b>날짜:</b> {email.get('date', '알 수 없음')}"
        date_para = Paragraph(date_text, date_style)
        story.append(date_para)
        
        # 발신/수신 표시
        direction = email.get('direction', 'received')
        if direction == 'sent':
            sender_text = f"<b>발신:</b> {email.get('from', '알 수 없음')}"
            sender_para = Paragraph(sender_text, sender_style)
            story.append(sender_para)
            
            receiver_text = f"<b>수신:</b> {email.get('to', '알 수 없음')}"
            receiver_para = Paragraph(receiver_text, receiver_style)
            story.append(receiver_para)
        else:
            sender_text = f"<b>발신:</b> {email.get('from', '알 수 없음')}"
            sender_para = Paragraph(sender_text, sender_style)
            story.append(sender_para)
            
            receiver_text = f"<b>수신:</b> {email.get('to', '알 수 없음')}"
            receiver_para = Paragraph(receiver_text, receiver_style)
            story.append(receiver_para)
        
        # 제목
        subject_text = f"<b>제목:</b> {clean_email_text(email.get('subject', '제목 없음'))}"
        subject_para = Paragraph(subject_text, subject_style)
        story.append(subject_para)
        
        story.append(Spacer(1, 0.1*inch))
        
        # 본문
        body_text = clean_email_text(email.get('body', '내용 없음'))
        
        # 본문이 너무 길면 나눔
        if len(body_text) > 3000:
            body_preview = body_text[:3000] + "...\n\n[본문이 너무 길어 생략되었습니다. 전체 내용은 원본 이메일을 참조하세요.]"
            body_para = Paragraph(f"<b>내용:</b><br/>{body_preview}", body_style)
        else:
            body_para = Paragraph(f"<b>내용:</b><br/>{body_text}", body_style)
        
        story.append(body_para)
        
        # 구분선 및 페이지 구분
        story.append(Spacer(1, 0.2*inch))
        
        if i < len(sorted_emails):
            # 마지막 이메일이 아니면 페이지 구분
            story.append(Paragraph("_" * 80, styles['Normal']))
            story.append(PageBreak())
        else:
            # 마지막 이메일
            story.append(Paragraph("_" * 80, styles['Normal']))
    
    # 부록: 통계 페이지
    story.append(PageBreak())
    
    stats_title = Paragraph("이메일 통계", subtitle_style)
    story.append(stats_title)
    story.append(Spacer(1, 0.3*inch))
    
    # 통계 계산
    received_count = len([e for e in sorted_emails if e.get('direction') != 'sent'])
    sent_count = len([e for e in sorted_emails if e.get('direction') == 'sent'])
    
    # 날짜별 통계
    date_counts = {}
    for email in sorted_emails:
        date = email.get('date', '')[:10]  # YYYY-MM-DD 부분만
        if date:
            date_counts[date] = date_counts.get(date, 0) + 1
    
    # 통계 텍스트
    stats_text = f"""
    <b>전체 통계</b><br/>
    • 총 이메일 수: {len(sorted_emails)}개<br/>
    • 수신 이메일: {received_count}개<br/>
    • 발신 이메일: {sent_count}개<br/>
    <br/>
    <b>기간</b><br/>
    • 시작: {sorted_emails[0].get('date', '알 수 없음')}<br/>
    • 종료: {sorted_emails[-1].get('date', '알 수 없음')}<br/>
    <br/>
    <b>날짜별 이메일 수</b><br/>
    """
    
    for date, count in sorted(date_counts.items()):
        stats_text += f"• {date}: {count}개<br/>"
    
    stats_para = Paragraph(stats_text, styles['Normal'])
    story.append(stats_para)
    
    # PDF 생성
    try:
        doc.build(story)
        print(f"✅ PDF 생성 완료: {output_path}")
        
        # 파일 크기 확인
        file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
        print(f"📏 파일 크기: {file_size:.2f} MB")
        print(f"📄 총 페이지: 약 {len(sorted_emails) * 1.5 + 3:.0f} 페이지")
        
        return output_path
    except Exception as e:
        print(f"❌ PDF 생성 오류: {e}")
        return None

def main():
    """메인 함수"""
    
    # 입력 파일 확인
    input_files = [
        "traveloka_emails.json",
        "sample_traveloka_emails.json"
    ]
    
    json_file = None
    for file in input_files:
        if os.path.exists(file):
            json_file = file
            break
    
    if not json_file:
        print("이메일 JSON 파일을 찾을 수 없습니다.")
        print("먼저 fetch_traveloka_emails.py를 실행해주세요.")
        return
    
    print(f"이메일 파일 로드: {json_file}")
    
    # 이메일 로드
    emails = load_emails_from_json(json_file)
    
    if not emails:
        print("이메일이 없습니다.")
        return
    
    # 출력 파일명 생성
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_pdf = f"traveloka_emails_timeline_{timestamp}.pdf"
    
    # PDF 생성
    pdf_path = create_email_pdf(emails, output_pdf)
    
    if pdf_path:
        print("\n" + "="*60)
        print("✅ 완료!")
        print("="*60)
        print(f"PDF 파일: {os.path.abspath(pdf_path)}")
        print(f"이메일 수: {len(emails)}개")
        
        # 파일 열기 (macOS)
        try:
            import subprocess
            subprocess.run(['open', pdf_path])
            print("PDF 파일을 열었습니다.")
        except:
            print(f"파일을 수동으로 열어주세요: {pdf_path}")
    
    return pdf_path

if __name__ == "__main__":
    main()