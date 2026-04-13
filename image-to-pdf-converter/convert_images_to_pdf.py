#!/usr/bin/env python3
"""
PNG 이미지들을 하나의 PDF로 변환하고 각 페이지 상단에 파일명 추가
"""

import os
import sys
from PIL import Image, ImageDraw, ImageFont
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.utils import ImageReader
import tempfile

def add_text_to_image(image_path, text, output_path):
    """이미지 상단에 텍스트 추가"""
    try:
        # 이미지 열기
        img = Image.open(image_path)
        
        # 이미지 모드 확인 및 변환 (RGBA 지원)
        if img.mode == 'RGBA':
            # RGBA를 RGB로 변환 (흰색 배경)
            background = Image.new('RGB', img.size, (255, 255, 255))
            background.paste(img, mask=img.split()[3])
            img = background
        elif img.mode != 'RGB':
            img = img.convert('RGB')
        
        # 텍스트 추가를 위한 새로운 이미지 생성
        # 상단에 텍스트 공간 추가 (100픽셀)
        text_height = 100
        new_height = img.height + text_height
        new_img = Image.new('RGB', (img.width, new_height), (255, 255, 255))
        
        # 원본 이미지 붙이기 (텍스트 공간 아래)
        new_img.paste(img, (0, text_height))
        
        # 텍스트 추가
        draw = ImageDraw.Draw(new_img)
        
        # 폰트 시도 (시스템 폰트)
        try:
            # macOS 기본 한글 폰트
            font_paths = [
                "/System/Library/Fonts/AppleSDGothicNeo.ttc",  # macOS
                "/System/Library/Fonts/PingFang.ttc",  # macOS 중국어 폰트 (한글 지원)
                "/Library/Fonts/AppleGothic.ttf",  # macOS
            ]
            
            font = None
            for font_path in font_paths:
                if os.path.exists(font_path):
                    try:
                        font = ImageFont.truetype(font_path, 24)
                        break
                    except:
                        continue
            
            if font is None:
                # 폰트를 찾지 못한 경우 기본 폰트 사용
                font = ImageFont.load_default()
        except:
            font = ImageFont.load_default()
        
        # 텍스트 위치 계산 (중앙 정렬)
        text_width = draw.textlength(text, font=font)
        text_x = (img.width - text_width) // 2
        text_y = (text_height - 30) // 2  # 수직 중앙
        
        # 텍스트 그리기 (검은색)
        draw.text((text_x, text_y), text, fill=(0, 0, 0), font=font)
        
        # 결과 저장
        new_img.save(output_path, 'PNG')
        return output_path
        
    except Exception as e:
        print(f"이미지 처리 중 오류 ({image_path}): {e}")
        return image_path  # 오류 시 원본 이미지 반환

def images_to_pdf(image_paths, output_pdf, add_filenames=True):
    """이미지들을 PDF로 변환"""
    try:
        # PDF 생성
        c = canvas.Canvas(output_pdf, pagesize=A4)
        
        for i, img_path in enumerate(image_paths):
            print(f"처리 중: {os.path.basename(img_path)} ({i+1}/{len(image_paths)})")
            
            try:
                # 이미지 열기
                img = Image.open(img_path)
                
                # 파일명 추출 (확장자 제외)
                filename = os.path.splitext(os.path.basename(img_path))[0]
                
                if add_filenames:
                    # 임시 파일에 텍스트 추가된 이미지 저장
                    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                        temp_img_path = tmp.name
                    
                    # 이미지에 텍스트 추가
                    processed_img_path = add_text_to_image(img_path, filename, temp_img_path)
                    
                    # 처리된 이미지로 PDF 페이지 추가
                    img_for_pdf = Image.open(processed_img_path)
                else:
                    img_for_pdf = img
                
                # 이미지 크기 조정 (A4 페이지에 맞게)
                page_width, page_height = A4
                img_width, img_height = img_for_pdf.size
                
                # 비율 유지하며 크기 조정
                scale = min(page_width / img_width, page_height / img_height) * 0.9
                new_width = img_width * scale
                new_height = img_height * scale
                
                # 페이지 중앙에 이미지 배치
                x = (page_width - new_width) / 2
                y = (page_height - new_height) / 2
                
                # 임시 파일로 저장 (reportlab이 PIL 이미지를 직접 지원하지 않음)
                with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as tmp:
                    temp_path = tmp.name
                    img_for_pdf.save(temp_path, 'PNG')
                
                # PDF 페이지에 이미지 추가
                c.drawImage(temp_path, x, y, new_width, new_height)
                
                # 임시 파일 삭제
                try:
                    os.unlink(temp_path)
                    if add_filenames:
                        os.unlink(processed_img_path)
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
        print(f"\nPDF 생성 완료: {output_pdf}")
        print(f"총 {len(image_paths)}개 이미지 처리됨")
        
    except Exception as e:
        print(f"PDF 생성 중 오류: {e}")
        raise

def main():
    """메인 함수"""
    # 입력 폴더 경로
    input_folder = "/Users/hongmin/Downloads/6_트레블로카 수수료 산정 관련 메일.png_260413"
    
    # 출력 PDF 경로
    output_pdf = "/Users/hongmin/Downloads/트레블로카_수수료_산정_관련_문서.pdf"
    
    # 폴더 존재 확인
    if not os.path.exists(input_folder):
        print(f"폴더를 찾을 수 없습니다: {input_folder}")
        sys.exit(1)
    
    # PNG 파일 목록 가져오기
    image_files = []
    for file in os.listdir(input_folder):
        if file.lower().endswith('.png'):
            image_files.append(os.path.join(input_folder, file))
    
    # 파일명으로 정렬
    image_files.sort()
    
    if not image_files:
        print("PNG 파일을 찾을 수 없습니다.")
        sys.exit(1)
    
    print(f"찾은 PNG 파일: {len(image_files)}개")
    for img in image_files:
        print(f"  - {os.path.basename(img)}")
    
    # PDF 생성
    try:
        images_to_pdf(image_files, output_pdf, add_filenames=True)
        print(f"\n✅ PDF 생성 완료!")
        print(f"📄 파일 위치: {output_pdf}")
        print(f"📊 총 페이지: {len(image_files)}")
        
        # 파일 크기 표시
        if os.path.exists(output_pdf):
            size = os.path.getsize(output_pdf) / (1024 * 1024)  # MB로 변환
            print(f"📏 파일 크기: {size:.2f} MB")
            
    except Exception as e:
        print(f"❌ PDF 생성 실패: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()