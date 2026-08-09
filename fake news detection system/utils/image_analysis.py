"""
Image Analysis Utilities for Fake News Detection
Handles OCR, metadata extraction, and tampering detection
"""

import os
import io
from PIL import Image
from PIL.ExifTags import TAGS
import numpy as np
from datetime import datetime

# Optional imports with fallbacks
try:
    import piexif
    PIEXIF_AVAILABLE = True
except ImportError:
    PIEXIF_AVAILABLE = False
    piexif = None

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    cv2 = None

# Tesseract OCR
try:
    import pytesseract
    # Set tesseract path for Windows (adjust if needed)
    pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    PYTESSERACT_AVAILABLE = True
except ImportError:
    pytesseract = None
    PYTESSERACT_AVAILABLE = False


class ImageAnalyzer:
    """Analyzes images for text extraction and metadata"""
    
    def __init__(self):
        self.supported_formats = ['JPEG', 'JPG', 'PNG', 'WEBP', 'BMP']
        
        # Fake news visual indicators (common patterns)
        self.fake_indicators = [
            'breaking', 'shocking', 'urgent', 'alert', 'exclusive',
            'miracle', 'secret', 'banned', 'exposed', 'truth',
            'doctors hate', 'one weird trick', 'you won\'t believe',
            'click here', 'share now', 'viral', 'hoax'
        ]
    
    def analyze_visual_content(self, image_path_or_bytes):
        """
        Analyze visual content of image for fake news indicators
        Uses color analysis, text patterns, and composition
        
        Args:
            image_path_or_bytes: Path to image file or bytes object
            
        Returns:
            dict: Visual analysis results with fake/real prediction
        """
        try:
            # Load image
            if isinstance(image_path_or_bytes, (str, bytes, io.BytesIO)):
                image = Image.open(image_path_or_bytes)
            else:
                image = image_path_or_bytes
            
            suspicious_score = 0
            indicators = []
            
            # Convert to RGB for analysis
            rgb_image = image.convert('RGB')
            img_array = np.array(rgb_image)
            
            # 1. OCR Text Analysis (MOST IMPORTANT - actual content)
            has_strong_fake_signals = False
            if PYTESSERACT_AVAILABLE:
                try:
                    text = pytesseract.image_to_string(image, lang='eng').lower()
                    
                    # Check for fake news keywords
                    found_keywords = []
                    for indicator in self.fake_indicators:
                        if indicator.lower() in text:
                            found_keywords.append(indicator.upper())
                    
                    # Score based on number of keywords
                    if len(found_keywords) >= 3:
                        suspicious_score += 60
                        indicators.append(f"Multiple sensational keywords: {', '.join(found_keywords[:3])}")
                        has_strong_fake_signals = True
                    elif len(found_keywords) == 2:
                        suspicious_score += 35
                        indicators.append(f"Sensational keywords: {', '.join(found_keywords)}")
                        has_strong_fake_signals = True
                    elif len(found_keywords) == 1:
                        suspicious_score += 15
                        indicators.append(f"Found keyword: '{found_keywords[0]}'")
                    
                    # Check for ALL CAPS SHOUTING (clickbait)
                    words = [w for w in text.split() if len(w) > 3]
                    if len(words) > 5:
                        caps_count = sum(1 for w in words if w.isupper())
                        if caps_count / len(words) > 0.5:  # 50%+ in caps
                            suspicious_score += 20
                            indicators.append("Heavy use of ALL CAPS (clickbait)")
                        
                except:
                    pass  # OCR optional
            
            # 2. Visual checks - ONLY if text analysis is inconclusive
            if not has_strong_fake_signals:
                # Check for EXTREME red saturation (not just normal red)
                red_channel = img_array[:, :, 0]
                green_channel = img_array[:, :, 1]
                blue_channel = img_array[:, :, 2]
                
                avg_red = np.mean(red_channel)
                avg_green = np.mean(green_channel)
                avg_blue = np.mean(blue_channel)
                
                # Red must be SIGNIFICANTLY higher than other colors
                if avg_red > 180 and (avg_red - avg_green) > 60 and (avg_red - avg_blue) > 60:
                    suspicious_score += 20
                    indicators.append("Extreme red saturation (sensational design)")
                
                # 3. Low quality viral meme pattern
                width, height = image.size
                total_pixels = width * height
                
                # Specific low-res social media dimensions (viral meme pattern)
                is_low_res = total_pixels < 150000  # Very low
                common_widths = [1080, 1170, 1284, 750, 828]
                is_screenshot = width in common_widths or height in common_widths
                
                if is_low_res and is_screenshot:
                    suspicious_score += 20
                    indicators.append("Low-quality viral screenshot pattern")
                
                # 4. Very simple color palette (pure graphic, not photo)
                unique_colors = len(np.unique(img_array.reshape(-1, img_array.shape[2]), axis=0))
                if unique_colors < 500:  # Very limited
                    suspicious_score += 15
                    indicators.append("Minimal color palette (graphic/meme, not photo)")
            
            # Balanced threshold - catches fake news but doesn't over-flag
            if suspicious_score >= 35:  # Moderate threshold
                prediction = "FAKE"
                confidence = min(55 + suspicious_score * 0.8, 95)
                message = "Image shows indicators of fake/sensational content"
            else:
                prediction = "REAL"
                confidence = max(88 - suspicious_score * 1.2, 65)
                message = "Image appears to be legitimate content"
            
            # If no indicators, show positive message
            if not indicators:
                indicators = ["No fake news indicators detected"]
            
            return {
                'prediction': prediction,
                'confidence': f'{confidence:.1f}%',
                'message': message,
                'suspicious_score': suspicious_score,
                'indicators': indicators,
                'analysis_type': 'visual_content'
            }
            
        except Exception as e:
            return {
                'prediction': 'UNKNOWN',
                'confidence': '0%',
                'message': f'Could not analyze visual content: {str(e)}',
                'suspicious_score': 0,
                'indicators': [],
                'analysis_type': 'visual_content'
            }
    
    def extract_text_from_image(self, image_path_or_bytes):
        """
        Extract text from image using OCR (Optical Character Recognition)
        
        Args:
            image_path_or_bytes: Path to image file or bytes object
            
        Returns:
            str: Extracted text from image
        """
        try:
            # Load image
            if isinstance(image_path_or_bytes, (str, bytes, io.BytesIO)):
                image = Image.open(image_path_or_bytes)
            else:
                image = image_path_or_bytes
            
            # Convert to RGB if necessary
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Check if pytesseract is available
            if not PYTESSERACT_AVAILABLE or pytesseract is None:
                return "OCR not available - Please install Tesseract OCR from https://github.com/UB-Mannheim/tesseract/wiki"
            
            # Perform OCR
            try:
                text = pytesseract.image_to_string(image, lang='eng')
                return text.strip() if text.strip() else "No text detected in image"
            except Exception as e:
                # Tesseract might not be installed
                return f"OCR failed - Please install Tesseract OCR: {str(e)}"
                
        except Exception as e:
            return f"Error extracting text: {str(e)}"
    
    def extract_metadata(self, image_path_or_bytes):
        """
        Extract EXIF metadata from image
        
        Args:
            image_path_or_bytes: Path to image file or bytes object
            
        Returns:
            dict: Metadata information
        """
        try:
            # Load image
            if isinstance(image_path_or_bytes, (str, bytes, io.BytesIO)):
                image = Image.open(image_path_or_bytes)
            else:
                image = image_path_or_bytes
            
            metadata = {
                'Format': image.format,
                'Size': f"{image.size[0]} x {image.size[1]}",
                'Mode': image.mode,
                'File Size': self._get_file_size(image_path_or_bytes)
            }
            
            # Extract EXIF data
            try:
                exif_data = image._getexif()
                if exif_data:
                    for tag_id, value in exif_data.items():
                        tag = TAGS.get(tag_id, tag_id)
                        # Convert bytes to string if needed
                        if isinstance(value, bytes):
                            try:
                                value = value.decode()
                            except:
                                value = str(value)
                        
                        # Add important metadata fields
                        if tag in ['Make', 'Model', 'DateTime', 'Software', 'Artist', 
                                   'DateTimeOriginal', 'DateTimeDigitized', 'GPSInfo']:
                            metadata[tag] = str(value)[:100]  # Limit length
            except Exception as e:
                metadata['EXIF Error'] = f"No EXIF data or error: {str(e)}"
            
            return metadata
            
        except Exception as e:
            return {'error': f"Error extracting metadata: {str(e)}"}
    
    def _get_file_size(self, image_source):
        """Get file size in human-readable format"""
        try:
            if isinstance(image_source, str):
                size = os.path.getsize(image_source)
            elif isinstance(image_source, io.BytesIO):
                size = len(image_source.getvalue())
            else:
                return "Unknown"
            
            # Convert to KB or MB
            if size < 1024:
                return f"{size} bytes"
            elif size < 1024 * 1024:
                return f"{size / 1024:.2f} KB"
            else:
                return f"{size / (1024 * 1024):.2f} MB"
        except:
            return "Unknown"
    
    def detect_tampering(self, image_path_or_bytes):
        """
        Detect possible image tampering using various techniques
        Smart detection that handles screenshots and PNG files appropriately
        
        Args:
            image_path_or_bytes: Path to image file or bytes object
            
        Returns:
            dict: Tampering detection results
        """
        try:
            # Load image
            if isinstance(image_path_or_bytes, (str, bytes, io.BytesIO)):
                image = Image.open(image_path_or_bytes)
            else:
                image = image_path_or_bytes
            
            warnings = []
            info_notes = []
            is_suspicious = False
            
            # Get basic image info
            width, height = image.size
            image_format = image.format
            is_png = image_format == 'PNG'
            is_small = width < 500 or height < 500
            
            # Check 1: Missing EXIF data - but be smart about it
            try:
                exif_data = image._getexif()
                if not exif_data or len(exif_data) == 0:
                    if is_png:
                        # PNG files rarely have EXIF, this is normal
                        info_notes.append("PNG files typically don't contain camera EXIF data (normal)")
                    elif is_small:
                        # Small images are likely screenshots or cropped
                        info_notes.append("Small image size suggests screenshot or social media image (normal)")
                    else:
                        # Large JPEG without EXIF is suspicious
                        warnings.append("No EXIF metadata found - may indicate editing or metadata stripping")
                        is_suspicious = True
            except:
                # Can't read EXIF - only suspicious for JPEG files
                if not is_png:
                    info_notes.append("Unable to read EXIF data")
            
            # Get metadata for further checks
            metadata = self.extract_metadata(image_path_or_bytes)
            
            # Check 2: Check for editing software signatures
            if 'Software' in metadata:
                software = metadata['Software'].lower()
                editing_tools = ['photoshop', 'gimp', 'paint.net', 'canva', 'pixlr', 'affinity']
                for tool in editing_tools:
                    if tool in software:
                        warnings.append(f"Image edited with {tool} - indicates post-processing")
                        is_suspicious = True
            
            # Check 3: Check for date inconsistencies
            if 'DateTime' in metadata and 'DateTimeOriginal' in metadata:
                if metadata['DateTime'] != metadata['DateTimeOriginal']:
                    warnings.append("Date modified differs from original date - image was edited")
                    is_suspicious = True
            
            # Check 4: Error Level Analysis (ELA) - only for JPEG
            if not is_png:  # ELA only works well with JPEG
                try:
                    ela_result = self._perform_basic_ela(image)
                    if ela_result['suspicious']:
                        warnings.append(f"ELA analysis: {ela_result['message']}")
                        is_suspicious = True
                except Exception as e:
                    pass  # ELA is optional
            
            # Check 5: Resolution and quality checks - only flag if suspicious
            if is_small and not is_png:
                # Small JPEG might be compressed/resized
                info_notes.append("Low resolution - may be compressed or cropped version")
            
            # Determine final status
            if is_png and is_small and not warnings:
                # Screenshot or PNG graphic - not suspicious
                status_message = "Likely a screenshot or graphic image (no tampering detected)"
                is_suspicious = False
            elif warnings:
                status_message = "Suspicious - Possible tampering detected"
            else:
                status_message = "No obvious tampering detected"
            
            return {
                'is_suspicious': is_suspicious,
                'warnings': warnings,
                'info_notes': info_notes,
                'status_message': status_message,
                'confidence': 'High' if len(warnings) > 2 else 'Medium' if len(warnings) > 0 else 'Low'
            }
            
        except Exception as e:
            return {
                'is_suspicious': False,
                'warnings': [f"Error during tampering detection: {str(e)}"],
                'info_notes': [],
                'status_message': 'Analysis error',
                'confidence': 'Unknown'
            }
    
    def _perform_basic_ela(self, image):
        """
        Perform basic Error Level Analysis
        Compares original with re-compressed version to detect edits
        """
        try:
            # Check if CV2 is available
            if not CV2_AVAILABLE or cv2 is None:
                return {'suspicious': False, 'message': 'ELA analysis not available (opencv not installed)'}
            
            # Convert PIL image to numpy array
            img_array = np.array(image.convert('RGB'))
            
            # Save image at quality 90% and reload
            temp_buffer = io.BytesIO()
            image.save(temp_buffer, format='JPEG', quality=90)
            temp_buffer.seek(0)
            compressed_image = Image.open(temp_buffer)
            compressed_array = np.array(compressed_image.convert('RGB'))
            
            # Calculate difference
            diff = cv2.absdiff(img_array, compressed_array)
            diff_gray = cv2.cvtColor(diff, cv2.COLOR_RGB2GRAY)
            
            # Calculate statistics
            mean_diff = np.mean(diff_gray)
            max_diff = np.max(diff_gray)
            
            # Threshold for suspicion (these are heuristic values)
            if max_diff > 50 and mean_diff > 10:
                return {
                    'suspicious': True,
                    'message': f'Uneven compression levels detected (max diff: {max_diff:.1f})'
                }
            
            return {'suspicious': False, 'message': 'Compression levels appear normal'}
            
        except Exception as e:
            return {'suspicious': False, 'message': f'ELA check skipped: {str(e)}'}


def analyze_image_file(file_data, analysis_type='metadata'):
    """
    Main function to analyze an uploaded image
    
    Args:
        file_data: File data (bytes or file object)
        analysis_type: 'metadata' - includes visual content analysis
        
    Returns:
        dict: Analysis results with metadata, tampering detection, and fake news prediction
    """
    analyzer = ImageAnalyzer()
    results = {
        'success': True,
        'analysis_type': analysis_type
    }
    
    try:
        # Create BytesIO object from file data
        if hasattr(file_data, 'read'):
            image_bytes = io.BytesIO(file_data.read())
        else:
            image_bytes = io.BytesIO(file_data)
        
        # Visual Content Analysis (FAKE/REAL prediction)
        image_bytes.seek(0)
        visual_analysis = analyzer.analyze_visual_content(image_bytes)
        results['visual_analysis'] = visual_analysis
        
        # Metadata Extraction
        image_bytes.seek(0)
        metadata = analyzer.extract_metadata(image_bytes)
        results['metadata'] = metadata
        
        # Tampering Detection
        image_bytes.seek(0)
        tampering_check = analyzer.detect_tampering(image_bytes)
        results['tampering_check'] = tampering_check
        
        return results
        
    except Exception as e:
        return {
            'success': False,
            'error': f"Error analyzing image: {str(e)}"
        }
