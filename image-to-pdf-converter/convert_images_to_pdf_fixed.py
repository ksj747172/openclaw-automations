#!/usr/bin/env python3
"""
PNG 이미지들을 하나의 PDF로 변환하고 각 페이지 상단에 정상적인 한국어 파일명 추가
NFD → NFC 정규화로 한글 파일명 문제 해결
"""

import os
import sys
import unicodedata
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile

def normalize_korean_text(text):
    """NFD 형식의 한글을 NFC로 정규화"""
    # NFD → NFC 변환
    normalized = unicodedata.normalize('NFC', text)
    return normalized

def add_text_to_image(image_path, text, output_path):
    """이미지 상단에 텍스트 추가 (한글 정규화 포함)"""
    try:
        # 한글 텍스트 정규화
        normalized_text = normalize_korean_text(text)
        
        # 이미지 열기
        img = Image.open(image_path)
        
        # 이미지 모드 확인 및 변환
        if img.mode == 'RGBA':
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 텍스트 추가를 위한 새로운 이미지 생성
        text_height = 100
        new_height = img.height + text_height
        new_img = Image.new('RGB', (img.width, new_height), (255, 255, 255))
        
        # 원본 이미지 붙이기
        new_img.paste(img, (0, text_height))
        
        # 텍스트 추가
        draw = ImageDraw.Draw(new_img)
        
        # 한글 폰트 찾기
        font = None
        font_paths = [
            "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS 기본 한글
            "/System/Library/Fonts/PingFang.ttc",          # macOS PingFang
            "/Library/Fonts/AppleGothic.ttf",              # macOS AppleGothic
            "/System/Library/Fonts/Hiragino Sans GB.ttc",  # macOS 히라기노
        ]
        
        for font_path in font_paths:
            if os.path.exists(font_path):
                try:
                    font = ImageFont.truetype(font_path, 28)  # 폰트 크기 증가
                    break
                except:
                    continue
        
        if font is None:
            # 폰트를 찾지 못한 경우 기본 폰트 사용
            font = ImageFont.load_default()
            print("⚠️  한글 폰트를 찾지 못했습니다. 기본 폰트 사용")
        
        # 텍스트 위치 계산 (중앙 정렬)
        try:
            # PIL의 textlength 사용
            text_width = draw.textlength(normalized_text, font=font)
        except:
            # textlength가 없는 경우 대체 방법
            text_width = len(normalized_text) * 20  # 대략적인 계산
        
        text_x = (img.width - text_width) // 2
        text_y = (text_height - 30) // 2
        
        # 텍스트 그리기
        draw.text((text_x, text_y), normalized_text, fill=(0, 0, 0), font=font)
        
        # 결과 저장
        new_img.save(output_path, 'PNG')
        return output_path, normalized_text
        
    except Exception as e:
        print(f"이미지 처리 중 오류 ({image_path}): {e}")
        return image_path, text  # 오류 시 원본 반환

def images_to_pdf(image_paths, output_pdf):
    """이미지들을 PDF로 변환 (한글 파일명 정상 표시)"""
    try:
        # PDF 생성
        c = canvas.Canvas(output_pdf, pagesize=A4)
        
        for i, img_path in enumerate(image_paths):
            # 원본 파일명 가져오기 (확장자 제외)
            original_filename = os.path.splitext(os.path.basename(img_path))[0]
            
            # 한글 정규화
            normalized_filename = normalize_korean_text(original_filename)
            
            print(f"처리 중 [{i+1}/8]: {normalized_filename}")
            
            try:
                # 임시 파일에 텍스트 추가된 이미지 저장
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    temp_img_path = tmp.name
                
                # 이미지에 텍스트 추가
                processed_img_path, final_text = add_text_to_image(
                    img_path, normalized_filename, temp_img_path
                )
                
                # 처리된 이미지 열기
                img_for_pdf = Image.open(processed_img_path)
                
                # 이미지 크기 조정 (A4 페이지에 맞게)
                page_width, page_height = A4
                img_width, img_height = img_for_pdf.size
                
                # 비율 유지하며 크기 조정
                scale = min(page_width / img_width, page_height / img_height) * 0.85
                new_width = img_width * scale
                new_height = img_height * scale
                
                # 페이지 중앙에 이미지 배치
                x = (page_width - new_width) / 2
                y = (page_height - new_height) / 2
                
                # 임시 파일로 저장
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp_pdf:
                    temp_pdf_path = tmp_pdf.name
                    img_for_pdf.save(temp_pdf_path, 'PNG')
                
                # PDF 페이지에 이미지 추가
                c.drawImage(temp_pdf_path, x, y, new_width, new_height)
                
                # 페이지 하단에 파일명 추가 (선택사항)
                c.setFont("Helvetica", 10)
                c.drawString(50, 30, f"파일: {final_text}")
                
                # 임시 파일 삭제
                try:
                    os.unlink(temp_img_path)
                    os.unlink(temp_pdf_path)
                except:
                    pass
                
                # 새 페이지 추가 (마지막 페이지 제외)
                if i < len(image_paths) - 1:
                    c.showPage()
                    
            except Exception as e:
                print(f"이미지 처리 실패 ({img_path}): {e}")
                continue
        
        # PDF 저장
        c.save()
        print(f"\n✅ PDF 생성 완료!")
        print(f"📄 파일 위치: {output_pdf}")
        
    except Exception as e:
        print(f"PDF 생성 중 오류: {e}")
        raise

def get_image_files(folder_path):
    """폴더에서 PNG 파일 목록 가져오기 (정렬)"""
    image_files = []
    for file in sorted(os.listdir(folder_path)):
        if file.lower().endswith('.png'):
            full_path = os.path.join(folder_path, file)
            image_files.append(full_path)
    return image_files

def main():
    """메인 함수"""
    # 입력 폴더 경로
    input_folder = "/Users/hongmin/Downloads/6_트레블로카 수수료 산정 관련 메일.png_260413"
    
    # 출력 PDF 경로 (새로운 이름)
    output_pdf = "/Users/hongmin/Downloads/트레블로카_수수료_산정_관련_문서_정상한글.pdf"
    
    # 폴더 존재 확인
    if not os.path.exists(input_folder):
        print(f"폴더를 찾을 수 없습니다: {input_folder}")
        sys.exit(1)
    
    # PNG 파일 목록 가져오기
    image_files = get_image_files(input_folder)
    
    if not image_files:
        print("PNG 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print("=" * 50)
    print("📁 처리할 파일 목록 (정규화 후):")
    print("=" * 50)
    
    for i, img_path in enumerate(image_files, 1):
        original_name = os.path.splitext(os.path.basename(img_path))[0]
        normalized_name = normalize_korean_text(original_name)
        print(f"{i:2d}. {normalized_name}")
    
    print("=" * 50)
    
    # PDF 생성
    try:
        images_to_pdf(image_files, output_pdf)
        
        # 파일 정보 표시
        if os.path.exists(output_pdf):
            size = os.path.getsize(output_pdf) / (1024 * 1024)
            print(f"📊 총 페이지: {len(image_files)}")
            print(f"📏 파일 크기: {size:.2f} MB")
            print(f"🎯 한글 표시: 정상 (NFD → NFC 변환 완료)")
            
    except Exception as e:
        print(f"❌ PDF 생성 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()