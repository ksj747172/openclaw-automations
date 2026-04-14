#!/usr/bin/env python3
"""
네이버 메일에서 Traveloka 지원팀 이메일 가져오기
"""

import imaplib
import email
import os
import sys
from email.header import decode_header
from datetime import datetime
import html
import re

def decode_email_header(header):
    """이메일 헤더 디코딩"""
    if not header:
        return ""
    
    try:
        decoded_parts = decode_header(header)
        decoded_str = ""
        
        for part, encoding in decoded_parts:
            if isinstance(part, bytes):
                if encoding:
                    decoded_str += part.decode(encoding)
                else:
                    # 인코딩 정보가 없으면 UTF-8 시도
                    try:
                        decoded_str += part.decode('utf-8')
                    except:
                        decoded_str += part.decode('latin-1', errors='ignore')
            else:
                decoded_str += str(part)
        
        return decoded_str
    except Exception as e:
        print(f"헤더 디코딩 오류: {e}")
        return str(header) if header else ""

def extract_email_body(msg):
    """이메일 본문 추출"""
    body = ""
    
    if msg.is_multipart():
        for part in msg.walk():
            content_type = part.get_content_type()
            content_disposition = str(part.get("Content-Disposition", ""))
            
            # 첨부파일이 아닌 텍스트 부분만 추출
            if "attachment" not in content_disposition:
                if content_type == "text/plain":
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            body += payload.decode('utf-8', errors='ignore')
                    except:
                        pass
                elif content_type == "text/html":
                    try:
                        payload = part.get_payload(decode=True)
                        if payload:
                            # HTML 태그 제거
                            html_content = payload.decode('utf-8', errors='ignore')
                            # 간단한 HTML 태그 제거
                            clean_text = re.sub(r'<[^>]+>', ' ', html_content)
                            clean_text = re.sub(r'\s+', ' ', clean_text)
                            body += clean_text.strip()
                    except:
                        pass
    else:
        # 단일 파트 메시지
        content_type = msg.get_content_type()
        try:
            payload = msg.get_payload(decode=True)
            if payload:
                if content_type == "text/html":
                    html_content = payload.decode('utf-8', errors='ignore')
                    clean_text = re.sub(r'<[^>]+>', ' ', html_content)
                    clean_text = re.sub(r'\s+', ' ', clean_text)
                    body = clean_text.strip()
                else:
                    body = payload.decode('utf-8', errors='ignore')
        except:
            body = msg.get_payload()
    
    return body.strip()

def parse_email_date(date_str):
    """이메일 날짜 파싱"""
    if not date_str:
        return ""
    
    # 다양한 날짜 형식 처리
    try:
        # 간단한 파싱 시도
        date_str = date_str.replace("(KST)", "").replace("(GMT+9)", "").strip()
        
        # 일반적인 이메일 날짜 형식
        date_formats = [
            "%a, %d %b %Y %H:%M:%S %z",
            "%d %b %Y %H:%M:%S %z",
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S"
        ]
        
        for fmt in date_formats:
            try:
                dt = datetime.strptime(date_str, fmt)
                return dt.strftime("%Y-%m-%d %H:%M:%S")
            except:
                continue
        
        # 실패 시 원본 반환
        return date_str[:50]  # 너무 길면 자름
    except:
        return date_str[:50] if date_str else ""

def fetch_naver_emails(email_user, email_pass, sender_filter="cs@traveloka.com", limit=100):
    """
    네이버 메일에서 이메일 가져오기
    
    Args:
        email_user: 네이버 이메일 주소
        email_pass: 비밀번호
        sender_filter: 발신자 필터 (기본: cs@traveloka.com)
        limit: 최대 가져올 이메일 수
    
    Returns:
        이메일 딕셔너리 리스트
    """
    
    print(f"네이버 메일 연결 중: {email_user}")
    print(f"발신자 필터: {sender_filter}")
    
    emails = []
    
    try:
        # IMAP 연결
        mail = imaplib.IMAP4_SSL("imap.naver.com", 993)
        mail.login(email_user, email_pass)
        
        print("로그인 성공")
        
        # 받은편지함 선택
        mail.select("inbox")
        print("받은편지함 선택 완료")
        
        # 발신자 검색
        print(f"'{sender_filter}' 발신자 검색 중...")
        status, messages = mail.search(None, f'FROM "{sender_filter}"')
        
        if status != "OK":
            print("검색 실패")
            mail.logout()
            return emails
        
        email_ids = messages[0].split()
        print(f"발견된 이메일: {len(email_ids)}개")
        
        # 최신 이메일부터 제한된 수만큼 처리
        email_ids = email_ids[-limit:] if len(email_ids) > limit else email_ids
        
        for i, email_id in enumerate(email_ids, 1):
            try:
                print(f"처리 중 [{i}/{len(email_ids)}]: {email_id.decode()}")
                
                # 이메일 가져오기
                status, msg_data = mail.fetch(email_id, "(RFC822)")
                
                if status != "OK":
                    print(f"  ⚠️ 이메일 가져오기 실패: {email_id}")
                    continue
                
                # 메시지 파싱
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        
                        # 메타데이터 추출
                        subject = decode_email_header(msg.get("Subject", ""))
                        from_ = decode_email_header(msg.get("From", ""))
                        to = decode_email_header(msg.get("To", ""))
                        date_str = msg.get("Date", "")
                        date_parsed = parse_email_date(date_str)
                        
                        # 본문 추출
                        body = extract_email_body(msg)
                        
                        # 이메일 ID
                        message_id = msg.get("Message-ID", f"unknown_{email_id.decode()}")
                        
                        emails.append({
                            "id": email_id.decode(),
                            "message_id": message_id,
                            "subject": subject,
                            "from": from_,
                            "to": to,
                            "date_raw": date_str,
                            "date": date_parsed,
                            "body": body,
                            "body_preview": body[:300] + "..." if len(body) > 300 else body
                        })
                        
                        break  # 첫 번째 유효한 응답만 처리
                
            except Exception as e:
                print(f"  ❌ 이메일 처리 오류 ({email_id}): {e}")
                continue
        
        # 보낸편지함도 검색 (발신 이메일)
        print("\n보낸편지함 검색 중...")
        mail.select("[Gmail]/Sent Mail")  # Gmail 레이블, 네이버는 다를 수 있음
        
        status, sent_messages = mail.search(None, f'TO "{sender_filter}"')
        
        if status == "OK":
            sent_ids = sent_messages[0].split()
            print(f"발신 이메일 발견: {len(sent_ids)}개")
            
            sent_ids = sent_ids[-limit:] if len(sent_ids) > limit else sent_ids
            
            for i, email_id in enumerate(sent_ids, 1):
                try:
                    print(f"발신 처리 중 [{i}/{len(sent_ids)}]: {email_id.decode()}")
                    
                    status, msg_data = mail.fetch(email_id, "(RFC822)")
                    
                    if status == "OK":
                        for response_part in msg_data:
                            if isinstance(response_part, tuple):
                                msg = email.message_from_bytes(response_part[1])
                                
                                subject = decode_email_header(msg.get("Subject", ""))
                                from_ = decode_email_header(msg.get("From", ""))
                                to = decode_email_header(msg.get("To", ""))
                                date_str = msg.get("Date", "")
                                date_parsed = parse_email_date(date_str)
                                
                                body = extract_email_body(msg)
                                message_id = msg.get("Message-ID", f"sent_{email_id.decode()}")
                                
                                emails.append({
                                    "id": email_id.decode(),
                                    "message_id": message_id,
                                    "subject": subject,
                                    "from": from_,
                                    "to": to,
                                    "date_raw": date_str,
                                    "date": date_parsed,
                                    "body": body,
                                    "body_preview": body[:300] + "..." if len(body) > 300 else body,
                                    "direction": "sent"  # 발신 표시
                                })
                                
                                break
                
                except Exception as e:
                    print(f"  ❌ 발신 이메일 처리 오류: {e}")
                    continue
        
        mail.close()
        mail.logout()
        print("연결 종료")
        
    except imaplib.IMAP4.error as e:
        print(f"IMAP 오류: {e}")
        print("네이버 메일 IMAP 설정을 확인해주세요.")
        print("1. 네이버 메일 설정 → POP3/IMAP 설정 → IMAP/SMTP 사용 활성화")
        print("2. 앱 비밀번호가 필요할 수 있습니다.")
    except Exception as e:
        print(f"예상치 못한 오류: {e}")
    
    return emails

def save_emails_to_json(emails, output_file="traveloka_emails.json"):
    """이메일을 JSON 파일로 저장"""
    import json
    
    # datetime 객체를 문자열로 변환
    def serialize_email(email):
        serialized = email.copy()
        # 모든 값을 문자열로 변환
        for key, value in serialized.items():
            if not isinstance(value, (str, int, float, bool, type(None))):
                serialized[key] = str(value)
        return serialized
    
    serialized_emails = [serialize_email(email) for email in emails]
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(serialized_emails, f, ensure_ascii=False, indent=2)
    
    print(f"이메일 저장 완료: {output_file} ({len(emails)}개)")
    return output_file

def main():
    """메인 함수"""
    
    # 환경 변수에서 자격 증명 가져오기
    email_user = os.getenv("NAVER_EMAIL")
    email_pass = os.getenv("NAVER_PASSWORD")
    
    if not email_user or not email_pass:
        print("환경 변수를 설정해주세요:")
        print("export NAVER_EMAIL='your_id@naver.com'")
        print("export NAVER_PASSWORD='your_password'")
        print("\n또는 스크립트 내에서 직접 설정:")
        print("email_user = 'your_id@naver.com'")
        print("email_pass = 'your_password'")
        
        # 테스트를 위한 샘플 데이터
        print("\n⚠️ 테스트 모드로 실행합니다 (실제 이메일 대신 샘플 데이터)")
        
        # 샘플 이메일 데이터
        sample_emails = [
            {
                "id": "1",
                "message_id": "sample1@traveloka.com",
                "subject": "항공권 변경 확인 요청",
                "from": "Traveloka Support <cs@traveloka.com>",
                "to": "홍민 김 <your_id@naver.com>",
                "date": "2026-04-13 14:30:00",
                "date_raw": "Mon, 13 Apr 2026 14:30:00 +0900",
                "body": "안녕하세요, 항공권 변경 요청이 접수되었습니다. 확인 후 연락드리겠습니다.",
                "body_preview": "안녕하세요, 항공권 변경 요청이 접수되었습니다...",
                "direction": "received"
            },
            {
                "id": "2",
                "message_id": "sample2@traveloka.com",
                "subject": "수수료 관련 문의 답변",
                "from": "홍민 김 <your_id@naver.com>",
                "to": "Traveloka Support <cs@traveloka.com>",
                "date": "2026-04-12 11:20:00",
                "date_raw": "Sun, 12 Apr 2026 11:20:00 +0900",
                "body": "안녕하세요, 수수료 관련하여 문의드립니다. 자세한 내용은 첨부파일 참조 부탁드립니다.",
                "body_preview": "안녕하세요, 수수료 관련하여 문의드립니다...",
                "direction": "sent"
            }
        ]
        
        # 샘플 데이터 저장
        save_emails_to_json(sample_emails, "sample_traveloka_emails.json")
        
        return sample_emails
    
    # 실제 이메일 가져오기
    print("실제 네이버 메일에서 이메일 가져오는 중...")
    emails = fetch_naver_emails(email_user, email_pass, "cs@traveloka.com", limit=50)
    
    if emails:
        # 이메일 저장
        output_file = save_emails_to_json(emails)
        
        # 요약 출력
        print("\n" + "="*60)
        print("이메일 요약:")
        print("="*60)
        
        received = [e for e in emails if e.get('direction') != 'sent']
        sent = [e for e in emails if e.get('direction') == 'sent']
        
        print(f"수신 이메일: {len(received)}개")
        print(f"발신 이메일: {len(sent)}개")
        print(f"총 이메일: {len(emails)}개")
        
        if received:
            print("\n최근 수신 이메일:")
            for email in received[-3:]:  # 최근 3개
                print(f"  • {email['date']}: {email['subject'][:50]}...")
        
        if sent:
            print("\n최근 발신 이메일:")
            for email in sent[-3:]:  # 최근 3개
                print(f"  • {email['date']}: {email['subject'][:50]}...")
        
        print("\n다음 단계: emails_to_pdf.py로 PDF 생성")
        
    else:
        print("이메일을 찾을 수 없습니다.")
        print("다음 사항을 확인해주세요:")
        print("1. 네이버 메일 IMAP 설정 활성화")
        print("2. cs@traveloka.com으로 이메일이 있는지 확인")
        print("3. 비밀번호가 정확한지 확인")
    
    return emails

if __name__ == "__main__":
    emails = main()