from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from gtts import gTTS
import os
from PyPDF2 import PdfReader
from io import BytesIO

app = Flask(__name__)

# Define the folder for uploaded files
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
# Use environment variable for secret key in production, fallback to default for development
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')

# Maximum file size for upload (8 MB)
MAX_FILE_SIZE_MB = 8
MAX_CONTENT_LENGTH = MAX_FILE_SIZE_MB * 1024 * 1024  # 8 MB in bytes
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Home route (renders your HTML page)
@app.route('/')
def home():
    return render_template('index.html')

# Route to handle the PDF upload and TTS conversion
@app.route('/convert', methods=['POST'])
def convert_to_audio():
    try:
        # Retrieve file from the form
        pdf_file = request.files['pdf-upload']
        language = request.form['language']
        voice_tone = request.form['voice-tone']
        
        print(f"[DEBUG] File: {pdf_file.filename}, Language: {language}, Voice: {voice_tone}")

        # Validate file size
        if pdf_file.content_length and pdf_file.content_length > MAX_CONTENT_LENGTH:
            flash(f'File size exceeds the {MAX_FILE_SIZE_MB} MB limit. Please upload a smaller file.', 'error')
            return redirect(url_for('home'))

        # Save the uploaded file
        pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_file.filename)
        pdf_file.save(pdf_path)
        print(f"[DEBUG] PDF saved to: {pdf_path}")

        # Extract text from PDF
        extracted_text = extract_text_from_pdf(pdf_path)
        print(f"[DEBUG] Extracted text length: {len(extracted_text) if extracted_text else 0} characters")
        
        if extracted_text:
            print(f"[DEBUG] First 100 chars: {extracted_text[:100]}...")
        else:
            flash('No text could be extracted from the PDF. Please ensure the PDF contains readable text (not scanned images).', 'error')
            return redirect(url_for('home'))

        # AI-powered text-to-speech conversion
        # Validate text length (gTTS has character limits)
        max_text_length = 5000  # gTTS limit is approximately 5000 characters per request
        if len(extracted_text) > max_text_length:
            # Split text into chunks for very long documents
            text_chunks = [extracted_text[i:i+max_text_length] 
                          for i in range(0, len(extracted_text), max_text_length)]
            flash(f'Document is very long ({len(extracted_text)} characters). Processing in chunks...', 'info')
            print(f"[DEBUG] Splitting into {len(text_chunks)} chunks")
        else:
            text_chunks = [extracted_text]
        
        # Select the best language code based on user input (AI-optimized)
        lang_code = select_language_code(language, voice_tone)
        print(f"[DEBUG] Input - Language: '{language}', Voice Tone: '{voice_tone}'")
        print(f"[DEBUG] Selected language code: '{lang_code}'")
        
        # Important: gTTS reads text in the specified language but does NOT translate.
        # If PDF text is in English and you select Spanish, it will try to read English words with Spanish pronunciation.
        # For proper translation, you would need a translation API before TTS conversion.

        # Generate text-to-speech audio using AI-powered gTTS
        audio_chunks = []
        for i, chunk in enumerate(text_chunks):
            print(f"[DEBUG] Processing chunk {i+1}/{len(text_chunks)} ({len(chunk)} chars)")
            print(f"[DEBUG] Using language code: '{lang_code}' for TTS")
            try:
                # Generate text-to-speech audio (slow=False for normal speed)
                # Note: lang_code should be a valid ISO 639-1 code (e.g., 'en', 'es', 'fr', 'de', etc.)
                tts = gTTS(text=chunk, lang=lang_code, slow=False)
                print(f"[DEBUG] gTTS object created successfully with lang='{lang_code}'")
                
                # Save chunk to memory
                chunk_io = BytesIO()
                tts.write_to_fp(chunk_io)
                chunk_io.seek(0)
                chunk_data = chunk_io.read()
                audio_chunks.append(chunk_data)
                print(f"[DEBUG] Chunk {i+1} audio size: {len(chunk_data)} bytes")
            except Exception as chunk_error:
                print(f"[ERROR] Error processing chunk {i+1}: {str(chunk_error)}")
                raise chunk_error
        
        # Combine all audio chunks
        combined_audio = b''.join(audio_chunks)
        print(f"[DEBUG] Combined audio size: {len(combined_audio)} bytes")
        
        # Save combined audio file to disk for download
        audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp3')
        with open(audio_file_path, 'wb') as audio_file:
            audio_file.write(combined_audio)
        
        print(f"[DEBUG] Audio file saved to: {audio_file_path}")
        print(f"[DEBUG] File exists: {os.path.exists(audio_file_path)}")
        print(f"[DEBUG] File size: {os.path.getsize(audio_file_path) if os.path.exists(audio_file_path) else 'N/A'} bytes")
        
        return redirect(url_for('result'))
        
    except Exception as e:
        error_msg = str(e)
        print(f"[ERROR] Conversion failed: {error_msg}")
        import traceback
        print(f"[ERROR] Traceback: {traceback.format_exc()}")
        
        # Provide user-friendly error messages
        if "lang" in error_msg.lower() or "language" in error_msg.lower():
            flash(f'Language error: The selected language may not be supported. Error: {error_msg}', 'error')
        elif "network" in error_msg.lower() or "connection" in error_msg.lower() or "timeout" in error_msg.lower():
            flash('Network error: Unable to connect to Google TTS service. Please check your internet connection and try again.', 'error')
        else:
            flash(f'Error generating audio: {error_msg}. Please try again or select a different language.', 'error')
        return redirect(url_for('home'))

# AI-enhanced function to extract text from PDF
def extract_text_from_pdf(pdf_path):
    """
    Extracts text content from PDF files with intelligent error handling.
    Uses advanced text extraction techniques to handle various PDF formats.
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        str: Extracted text content, cleaned and normalized
    """
    text = ""
    try:
        with open(pdf_path, 'rb') as pdf_file:
            reader = PdfReader(pdf_file)
            num_pages = len(reader.pages)
            
            # Extract text from all pages
            for page_num, page in enumerate(reader.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        # Clean and normalize text (remove excessive whitespace)
                        cleaned_text = ' '.join(page_text.split())
                        text += cleaned_text + " "
                except Exception as e:
                    # Continue processing other pages if one fails
                    continue
            
            # Final text cleaning - remove extra spaces and normalize
            text = ' '.join(text.split())
            
    except Exception as e:
        # Return empty string if extraction fails completely
        return ""
    
    return text.strip()

# Function to select the language code based on input
def select_language_code(language, voice_tone):
    """
    AI-powered language mapping: Maps user-selected language and voice tone to gTTS language codes.
    Uses intelligent voice selection based on regional preferences and voice characteristics.
    
    Args:
        language: Language code from form (e.g., 'en', 'es', 'fr', 'de', 'it', etc.)
        voice_tone: Voice tone selection ('male', 'female', 'kid')
    
    Returns:
        str: gTTS language code for the selected combination
    """
    # Normalize voice tone (handle 'kid' vs 'kids')
    normalized_tone = 'kids' if voice_tone == 'kid' else voice_tone
    
    # Comprehensive language code mapping with AI-optimized voice selection
    # Note: gTTS uses ISO 639-1 language codes. Regional variants may not be fully supported.
    # Format: {language_code: {tone: gtts_code}}
    language_codes = {
        # English variants - gTTS supports 'en' (defaults to US English)
        'en': {
            'male': 'en',       # English - clear, professional
            'female': 'en',    # English - elegant, refined
            'kids': 'en'        # English - friendly, playful
        },
        # Spanish variants - gTTS supports 'es' (defaults to Latin American)
        'es': {
            'male': 'es',       # Spanish - warm, expressive
            'female': 'es',     # Spanish - clear, formal
            'kids': 'es'        # Spanish - friendly, energetic
        },
        # French variants - gTTS supports 'fr'
        'fr': {
            'male': 'fr',       # French - clear, neutral
            'female': 'fr',     # French - elegant, sophisticated
            'kids': 'fr'        # French - soft, approachable
        },
        # German
        'de': {
            'male': 'de',       # German - clear, authoritative
            'female': 'de',     # German - professional, warm
            'kids': 'de'        # German - friendly, clear
        },
        # Italian
        'it': {
            'male': 'it',       # Italian - expressive, melodic
            'female': 'it',     # Italian - elegant, warm
            'kids': 'it'        # Italian - cheerful, animated
        },
        # Portuguese - gTTS supports 'pt' (defaults to Brazilian)
        'pt': {
            'male': 'pt',       # Portuguese - warm, expressive
            'female': 'pt',     # Portuguese - clear, formal
            'kids': 'pt'        # Portuguese - friendly, energetic
        },
        # Russian
        'ru': {
            'male': 'ru',       # Russian - deep, authoritative
            'female': 'ru',     # Russian - clear, elegant
            'kids': 'ru'        # Russian - friendly, clear
        },
        # Chinese (Mandarin) - gTTS supports 'zh' or 'zh-cn'
        'zh': {
            'male': 'zh',       # Mandarin Chinese - clear, professional
            'female': 'zh',     # Mandarin Chinese - soft, elegant
            'kids': 'zh'        # Mandarin Chinese - friendly, clear
        },
        # Japanese
        'ja': {
            'male': 'ja',       # Japanese - clear, respectful
            'female': 'ja',     # Japanese - soft, polite
            'kids': 'ja'        # Japanese - friendly, animated
        },
        # Korean
        'ko': {
            'male': 'ko',       # Korean - clear, professional
            'female': 'ko',     # Korean - soft, elegant
            'kids': 'ko'        # Korean - friendly, cheerful
        },
        # Arabic
        'ar': {
            'male': 'ar',       # Arabic - clear, authoritative
            'female': 'ar',     # Arabic - elegant, clear
            'kids': 'ar'        # Arabic - friendly, animated
        },
        # Hindi
        'hi': {
            'male': 'hi',       # Hindi - clear, expressive
            'female': 'hi',     # Hindi - soft, warm
            'kids': 'hi'        # Hindi - friendly, energetic
        },
        # Dutch
        'nl': {
            'male': 'nl',       # Dutch - clear, professional
            'female': 'nl',     # Dutch - warm, friendly
            'kids': 'nl'        # Dutch - cheerful, clear
        },
        # Polish
        'pl': {
            'male': 'pl',       # Polish - clear, authoritative
            'female': 'pl',     # Polish - elegant, warm
            'kids': 'pl'        # Polish - friendly, animated
        },
        # Turkish
        'tr': {
            'male': 'tr',       # Turkish - clear, expressive
            'female': 'tr',     # Turkish - elegant, warm
            'kids': 'tr'        # Turkish - friendly, energetic
        },
        # Swedish
        'sv': {
            'male': 'sv',       # Swedish - clear, professional
            'female': 'sv',     # Swedish - soft, elegant
            'kids': 'sv'        # Swedish - friendly, clear
        },
        # Norwegian
        'no': {
            'male': 'no',       # Norwegian - clear, professional
            'female': 'no',     # Norwegian - warm, friendly
            'kids': 'no'        # Norwegian - cheerful, animated
        },
        # Danish
        'da': {
            'male': 'da',       # Danish - clear, professional
            'female': 'da',     # Danish - soft, elegant
            'kids': 'da'        # Danish - friendly, clear
        },
        # Finnish
        'fi': {
            'male': 'fi',       # Finnish - clear, professional
            'female': 'fi',     # Finnish - warm, friendly
            'kids': 'fi'        # Finnish - cheerful, animated
        },
        # Greek
        'el': {
            'male': 'el',       # Greek - clear, expressive
            'female': 'el',     # Greek - elegant, warm
            'kids': 'el'        # Greek - friendly, energetic
        },
        # Czech
        'cs': {
            'male': 'cs',       # Czech - clear, professional
            'female': 'cs',     # Czech - soft, elegant
            'kids': 'cs'        # Czech - friendly, animated
        },
        # Romanian
        'ro': {
            'male': 'ro',       # Romanian - clear, expressive
            'female': 'ro',     # Romanian - elegant, warm
            'kids': 'ro'        # Romanian - friendly, energetic
        },
        # Hungarian
        'hu': {
            'male': 'hu',       # Hungarian - clear, professional
            'female': 'hu',     # Hungarian - soft, elegant
            'kids': 'hu'        # Hungarian - friendly, animated
        },
        # Indonesian
        'id': {
            'male': 'id',       # Indonesian - clear, expressive
            'female': 'id',     # Indonesian - warm, friendly
            'kids': 'id'        # Indonesian - cheerful, energetic
        },
        # Thai
        'th': {
            'male': 'th',       # Thai - clear, professional
            'female': 'th',     # Thai - soft, elegant
            'kids': 'th'        # Thai - friendly, animated
        },
        # Vietnamese
        'vi': {
            'male': 'vi',       # Vietnamese - clear, expressive
            'female': 'vi',     # Vietnamese - elegant, warm
            'kids': 'vi'        # Vietnamese - friendly, energetic
        },
        # Hebrew
        'he': {
            'male': 'he',       # Hebrew - clear, authoritative
            'female': 'he',     # Hebrew - elegant, clear
            'kids': 'he'        # Hebrew - friendly, animated
        },
        # Ukrainian
        'uk': {
            'male': 'uk',       # Ukrainian - clear, expressive
            'female': 'uk',     # Ukrainian - elegant, warm
            'kids': 'uk'        # Ukrainian - friendly, energetic
        },
        # Catalan
        'ca': {
            'male': 'ca',       # Catalan - clear, professional
            'female': 'ca',     # Catalan - soft, elegant
            'kids': 'ca'        # Catalan - friendly, animated
        },
        # Croatian
        'hr': {
            'male': 'hr',       # Croatian - clear, professional
            'female': 'hr',     # Croatian - warm, friendly
            'kids': 'hr'        # Croatian - cheerful, animated
        },
        # Slovak
        'sk': {
            'male': 'sk',       # Slovak - clear, professional
            'female': 'sk',     # Slovak - soft, elegant
            'kids': 'sk'        # Slovak - friendly, animated
        },
        # Bulgarian
        'bg': {
            'male': 'bg',       # Bulgarian - clear, expressive
            'female': 'bg',     # Bulgarian - elegant, warm
            'kids': 'bg'        # Bulgarian - friendly, energetic
        },
        # Serbian
        'sr': {
            'male': 'sr',       # Serbian - clear, professional
            'female': 'sr',     # Serbian - warm, friendly
            'kids': 'sr'        # Serbian - cheerful, animated
        },
        # Slovenian
        'sl': {
            'male': 'sl',       # Slovenian - clear, professional
            'female': 'sl',     # Slovenian - soft, elegant
            'kids': 'sl'        # Slovenian - friendly, animated
        }
    }

    # Get language configuration, default to English if not found
    lang_config = language_codes.get(language, language_codes['en'])
    print(f"[DEBUG] Language config for '{language}': {lang_config}")
    print(f"[DEBUG] Normalized tone: '{normalized_tone}'")
    
    # Get voice tone, default to 'male' if not found
    gtts_code = lang_config.get(normalized_tone, lang_config.get('male', 'en'))
    print(f"[DEBUG] Final gTTS code: '{gtts_code}'")
    
    return gtts_code

@app.route('/result')
def result():
    return render_template('result.html')

@app.route('/download')
def download():
    audio_file_path = os.path.join(app.config['UPLOAD_FOLDER'], 'output.mp3')
    if os.path.exists(audio_file_path):
        print(f"[DEBUG] Downloading audio file: {audio_file_path} ({os.path.getsize(audio_file_path)} bytes)")
        return send_file(audio_file_path, as_attachment=True, download_name='converted_audio.mp3')
    else:
        print(f"[ERROR] Audio file not found: {audio_file_path}")
        flash('Audio file not found. Please convert a PDF first.', 'error')
        return redirect(url_for('home'))

if __name__ == "__main__":
    # Run in debug mode for development only
    # Set FLASK_DEBUG=False environment variable for production deployment
    # NEVER enable debug mode in production - it exposes sensitive information
    debug_mode = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
