import numpy as np
from PIL import Image
import cv2
import io
import pytesseract
import os


class ImageProcessor:
    def __init__(self):
        pass
    
    # image preprocessing function
    def preprocess_image(self, image):

        try:
            # PIL Image to OpenCV format
            if isinstance(image, Image.Image):
                img_array = np.array(image)
                if len(img_array.shape) == 3:
                    img = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
                else:
                    img = img_array
            else:
                img = image

            # image resizing(이미지 크기 키우기)
            height, width = img.shape[:2]
            if height < 200 or width <200:
                scale = 2
                img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            
            # grayscale conversion
            if len(img.shape) == 3:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            else:
                gray = img
            
            # noise reduction
            denoised = cv2.medianBlur(img, 3)
            enhanced = cv2.convertScaleAbs(denoised, alpha=1.5, beta=10)

            return enhanced
     
        except Exception as e:
            print(f"Error processing image: {e}")
            return image
        
    # text from image extraction function
    def extract_text_image(self, image_file):
    
        try:
            # image loading
            if hasattr(image_file, 'read'):
                # flask file
                image_file.seek(0)
                image = Image.open(io.BytesIO(image_file.read()))
            else:
                image = Image.open(image_file)
            
            # image preprocessing
            processed = self.preprocess_image(image)
            
            # PSM mode
            psm_mode = [6,7,8,13]

            for psm in psm_mode:
                try:
                    text = pytesseract.image_to_string(
                        processed,
                        lang = 'kor+eng',
                        config=f'--psm {psm}'
                    ).strip()

                    # meaningful text extraction
                    if text and len(text) > 1 and not text.isdigit():
                        print(f"PSM {psm} extracted text: {text}")
                        return text
                except Exception:
                    continue
            
            # if failed to extract text with nominal PSM modes
            return pytesseract.image_to_string(processed, lang='kor+eng').strip()
        
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return None
    
    # image processing function
    def processing_image(self, image_file):

        try:
            # text extraction
            extracted_text = self.extract_text_image(image_file)

            if extracted_text:
                print(f"Extracted text: {extracted_text}")

                cleaned_text = extracted_text.replace('\n', ' ').replace('\r', '').strip()

                result = {
                    'success': True,
                    'extracted_text': extracted_text,
                    'cleaned_text': cleaned_text,
                    'query': cleaned_text
                }
            else:
                result = {
                    'success': False,
                    'message': '이미지에서 텍스트를 추출할 수 없습니다.',
                    'extracted_text': '',
                    'cleaned_text': '',
                    'query': ''
                }
            return result
        
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'extracted_text': '',
                'cleaned_text': '',
                'query': ''
            }
    
    # text cleaning function
    def clean_text(self, text):
        cleaned = ' '.join(text.split())

        # if the cleaned text is too short, return the original text
        if len(cleaned) < 2:
            return text
        
        return cleaned

# test function
def test_image_processor():
    processor = ImageProcessor()

    from PIL import Image, ImageDraw

    img = Image.new('RGB', (400, 150), color='white')
    draw = ImageDraw.Draw(img)

    # drug info text
    draw.text((20, 30), "타이레놀", fill='black')
    draw.text((20, 70), "TYLENOL", fill='black')

    # save the test image
    test_image_path = 'test_image.png'
    img.save(test_image_path)

    result = processor.processing_image(test_image_path)

    if result['success']:
        print("Test passed!")
        print(f"Extracted Text: {result['extracted_text']}")
    
    else:
        print("Test failed!")
        print(f"Error: {result['error']}")
    
    # clean up the test image
    if os.path.exists(test_image_path):
        os.remove(test_image_path)
    
    return processor

if __name__ == "__main__":
    test_image_processor()