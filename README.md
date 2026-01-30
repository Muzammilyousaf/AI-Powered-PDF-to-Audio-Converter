# 🤖 AI-Powered PDF to Audio Converter

An advanced web-based application that converts PDF documents into high-quality audio files using **AI-powered Google Text-to-Speech (gTTS)** neural networks. Built with Flask, this tool leverages cutting-edge artificial intelligence to transform written content into natural, human-like spoken audio with support for **40+ languages** and customizable voice tones.

## 🚀 Features

- **🤖 AI-Powered Text-to-Speech**: Uses Google's advanced neural network TTS for natural, human-like voice synthesis
- **🌍 40+ Languages Supported**: Extensive language support including English, Spanish, French, German, Italian, Portuguese, Russian, Chinese, Japanese, Korean, Arabic, Hindi, and many more
- **🎭 Voice Customization**: Choose from male, female, or child-friendly voice tones optimized for each language
- **📝 Language Matching**: Select the language that matches your PDF text for accurate pronunciation (see Important Note below)
- **📄 Intelligent PDF Processing**: Advanced text extraction with error handling and text normalization
- **🎵 High-Quality Audio Output**: Generates MP3 audio files with neural network-generated speech
- **📊 Long Document Support**: Automatically handles large documents by processing text in optimized chunks
- **💻 User-Friendly Interface**: Clean, responsive web interface with organized language selection
- **✅ File Size Validation**: Enforces 8 MB maximum file size limit for optimal performance
- **🎧 Real-Time Preview**: Listen to generated audio before downloading
- **🛡️ Robust Error Handling**: Comprehensive error handling for better user experience

## 📋 Prerequisites

Before you begin, ensure you have the following installed:

- Python 3.7 or higher
- pip (Python package manager)

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/pdf-to-audio-converter.git
   cd pdf-to-audio-converter
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # On Windows
   venv\Scripts\activate
   
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## 🎯 Usage

1. **Start the Flask application**
   ```bash
   python app.py
   ```

2. **Access the web interface**
   - Open your web browser and navigate to `http://localhost:5000`

3. **Convert a PDF to audio**
   - Click "Choose File" and select a PDF document (max 8 MB)
   - **Important**: Select the language that matches the language of text in your PDF (e.g., if PDF is in Hindi, select Hindi)
   - Choose a voice tone (Male, Female, or Kid)
   - Click "Convert to Audio"
   - Wait for the AI-powered conversion to complete
   - Preview the audio or download the MP3 file

   **Note**: gTTS reads text in the selected language but does NOT translate. For best results, match the language selection to your PDF's text language.

## 📁 Project Structure

```
pdf-to-audio-converter/
│
├── app.py                 # Main Flask application file
├── requirements.txt       # Python dependencies
├── README.md             # Project documentation
├── .gitignore            # Git ignore rules
├── .gitattributes        # Git attributes configuration
│
└── templates/
    ├── index.html        # Main upload and conversion interface
    └── result.html       # Audio preview and download page
│
└── uploads/              # Directory for uploaded PDFs and generated audio (created automatically)
```

## 🔧 Configuration

### Environment Variables

The application uses a secret key for Flask session management. For production deployments, set the `FLASK_SECRET_KEY` environment variable:

```bash
# On Windows
set FLASK_SECRET_KEY=your-secret-key-here

# On macOS/Linux
export FLASK_SECRET_KEY=your-secret-key-here
```

If not set, the application will use a default key (not recommended for production).

### File Upload Settings

- **Maximum file size**: 8 MB (configurable in `app.py`)
- **Supported format**: PDF files only
- **Output format**: MP3 audio files

## 🌍 Supported Languages (40+ Languages)

### Popular Languages
- **English** (en) - American, British, Australian variants
- **Spanish** (es) - Latin American, European, Mexican variants
- **French** (fr) - Canadian, France variants
- **German** (de)
- **Italian** (it)
- **Portuguese** (pt) - Brazilian, European variants

### Asian Languages
- **Chinese/Mandarin** (zh)
- **Japanese** (ja)
- **Korean** (ko)
- **Hindi** (hi)
- **Thai** (th)
- **Vietnamese** (vi)
- **Indonesian** (id)

### European Languages
- **Russian** (ru)
- **Dutch** (nl)
- **Polish** (pl)
- **Turkish** (tr)
- **Swedish** (sv)
- **Norwegian** (no)
- **Danish** (da)
- **Finnish** (fi)
- **Greek** (el)
- **Czech** (cs)
- **Romanian** (ro)
- **Hungarian** (hu)
- **Ukrainian** (uk)
- **Catalan** (ca)
- **Croatian** (hr)
- **Slovak** (sk)
- **Bulgarian** (bg)
- **Serbian** (sr)
- **Slovenian** (sl)

### Middle Eastern & Other Languages
- **Arabic** (ar)
- **Hebrew** (he)

**Note**: Each language supports Male, Female, and Kid voice tones. Voice characteristics are AI-optimized for each language and regional variant.

## 🧪 Technical Details

### AI Technology

This application leverages **Google's AI-powered Text-to-Speech** service, which uses:
- **Neural Network Models**: Advanced deep learning models for natural speech synthesis
- **WaveNet Technology**: High-quality voice generation with human-like intonation
- **Multi-Language AI**: Trained models for 40+ languages with regional accents

### Dependencies

- **Flask**: Web framework for building the application
- **gTTS (Google Text-to-Speech)**: AI-powered text-to-speech conversion library using neural networks
- **PyPDF2**: Advanced PDF text extraction library with intelligent parsing

### Key Functions

- `extract_text_from_pdf(pdf_path)`: AI-enhanced text extraction with intelligent error handling and text normalization
- `select_language_code(language, voice_tone)`: AI-optimized language mapping with intelligent voice selection for 40+ languages
- `convert_to_audio()`: Main conversion route handler with chunk processing for long documents
- `download()`: Handles audio file downloads

### AI Features

- **Intelligent Text Processing**: Advanced text cleaning and normalization
- **Smart Chunking**: Automatically handles documents exceeding TTS character limits
- **Optimized Voice Selection**: AI-optimized voice selection based on language and tone preferences
- **Error Recovery**: Robust error handling with graceful degradation

### API Routes

- `GET /`: Home page with upload form
- `POST /convert`: Processes PDF upload and generates audio
- `GET /result`: Displays conversion result with audio preview
- `GET /download`: Downloads the generated MP3 file

## ⚠️ Important: How Language Selection Works

### ⚠️ **gTTS Does NOT Translate Text**

**Critical Understanding**: Google Text-to-Speech (gTTS) **reads text in the specified language but does NOT translate it**. This is a text-to-speech service, not a translation service.

### How It Actually Works:

1. **If PDF text matches selected language** ✅
   - **Example**: PDF contains Hindi text → You select Hindi → Audio reads Hindi correctly
   - **Example**: PDF contains English text → You select English → Audio reads English correctly
   - **Result**: Perfect pronunciation in the native language

2. **If PDF text does NOT match selected language** ❌
   - **Example**: PDF contains English text → You select Hindi → Audio attempts to read English words with Hindi accent
   - **Example**: PDF contains Spanish text → You select French → Audio attempts to read Spanish words with French pronunciation
   - **Result**: Incorrect pronunciation, may sound garbled or nonsensical

### Real-World Examples:

| PDF Language | Selected Language | What Happens |
|--------------|-------------------|--------------|
| Hindi | Hindi | ✅ Reads Hindi text perfectly in Hindi |
| English | English | ✅ Reads English text perfectly in English |
| English | Hindi | ❌ Tries to read English words with Hindi accent (sounds wrong) |
| Spanish | French | ❌ Tries to read Spanish words with French pronunciation (sounds wrong) |
| German | Japanese | ❌ Tries to read German words with Japanese pronunciation (sounds wrong) |

### Best Practice:

**Always select the language that matches the language of text in your PDF document.**

- If your PDF is in Hindi → Select Hindi
- If your PDF is in English → Select English
- If your PDF is in Spanish → Select Spanish
- And so on...

### For Translation:

If you need to translate text before converting to audio, you would need:
1. A separate translation service (e.g., Google Translate API, DeepL)
2. Translate the extracted PDF text to your target language
3. Then convert the translated text to speech using gTTS

**This application focuses on text-to-speech conversion only, not translation.**

## ⚠️ Limitations & Important Notes

### What This Tool CAN Do:
✅ Convert text-based PDF files to audio  
✅ Support 40+ languages for reading text  
✅ Generate high-quality audio files (MP3 format)  
✅ Handle PDFs up to 8 MB in size  
✅ Process long documents automatically  

### What This Tool CANNOT Do:
❌ **Translate text** - It only reads text in the language you select, it does NOT translate from one language to another  
❌ **Read scanned PDFs** - Only works with PDFs that contain actual text (not images of text)  
❌ **Work offline** - Requires an active internet connection  
❌ **Read handwritten text** - Only works with typed/printed text in PDFs  
❌ **Process password-protected PDFs** - PDFs must be unlocked  
❌ **Extract text from images** - Cannot read text from pictures or scanned documents  

### Technical Limitations:
- **File Size**: Maximum 8 MB per PDF file
- **Internet Required**: Must be connected to the internet to use Google's TTS service
- **Text-Based PDFs Only**: Scanned PDFs or image-based PDFs will not work
- **Language Matching**: For best results, select the language that matches your PDF text
- **Processing Time**: Large documents may take longer to convert
- **Service Availability**: Depends on Google's TTS service being available

### Common Issues & Solutions:

**Problem**: "No text could be extracted from the PDF"  
**Solution**: Your PDF might be scanned/image-based. Try a PDF with selectable text.

**Problem**: Audio sounds wrong or garbled  
**Solution**: Make sure you selected the language that matches your PDF text (e.g., if PDF is in Hindi, select Hindi)

**Problem**: Conversion fails or times out  
**Solution**: Check your internet connection. The service requires internet to work.

**Problem**: File is too large  
**Solution**: PDF must be 8 MB or smaller. Try compressing your PDF or splitting it into smaller files.

**Problem**: Audio doesn't sound natural  
**Solution**: This is normal - computer-generated speech may not sound exactly like a human voice, but it should be clear and understandable.

## 🔒 Security Considerations

- **Production Deployment**: Change the default secret key before deploying
- **File Uploads**: Files are stored temporarily in the `uploads/` directory
- **Input Validation**: File size and type validation implemented
- **Error Handling**: Basic error handling for file operations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- [Flask](https://flask.palletsprojects.com/) - Web framework
- [gTTS](https://gtts.readthedocs.io/) - Google AI Text-to-Speech library (Neural TTS)
- [PyPDF2](https://pypdf2.readthedocs.io/) - PDF processing library
- **Google AI**: For providing advanced neural text-to-speech technology

## 📧 Support

For issues, questions, or contributions, please open an issue on the GitHub repository.

## 🔄 Version History

- **v2.0.0** (2024)
  - ✨ AI-powered enhancements
  - 🌍 Expanded to 40+ languages
  - 🧠 Intelligent text processing and chunking
  - 🎯 Optimized voice selection algorithm
  - 🛡️ Enhanced error handling
  - 📊 Long document support with automatic chunking

- **v1.0.0** (2024)
  - Initial release
  - PDF to audio conversion
  - Multi-language support (3 languages)
  - Voice tone customization
  - Web-based interface

---

## 🤖 AI Technology Note

This application uses **Google's AI-powered Text-to-Speech service**, which leverages advanced neural networks and machine learning models to generate natural, human-like speech. The service requires an active internet connection and is free to use, subject to Google's terms of service and rate limits.

### How the AI Works:
1. **Text Analysis**: The extracted PDF text is analyzed and normalized
2. **Neural Processing**: Google's AI models process the text using deep learning
3. **Voice Synthesis**: Neural networks generate natural speech with proper intonation in the selected language
4. **Audio Generation**: High-quality MP3 audio is created with human-like characteristics

The AI automatically selects optimal voice characteristics based on language and tone preferences.

### ⚠️ Important Reminder:

**gTTS is a Text-to-Speech service, NOT a Translation service.**

- It reads text in the language you specify
- It does NOT translate text from one language to another
- For best results, select the language that matches the language of text in your PDF
- If you need translation, use a translation service first, then convert the translated text to speech
