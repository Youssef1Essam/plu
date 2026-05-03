import { useState } from 'react';
import InputSection from './components/InputSection';
import ResultCard from './components/ResultCard';
import { analyzeScenario, analyzeCustom, analyzeEgypt } from './services/api';
import type { RiskAssessmentResponse } from './services/api';
import logo from './assets/logo.png';

function App() {
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<RiskAssessmentResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [selectedCityContext, setSelectedCityContext] = useState<string | null>(null);
  const [language, setLanguage] = useState<'en' | 'ar'>('en');

  const handleAnalyze = async (data: any, mode: 'scenario' | 'custom' | 'city' | 'demo') => {
    setLoading(true);
    setError(null);
    setResult(null);
    
    // Clear context unless we are specifically running a Cairo city
    if (mode === 'city' && data.is_cairo_preset) {
      setSelectedCityContext(data.city_name);
    } else if (mode === 'demo') {
      setSelectedCityContext('Helwan');
    } else {
      setSelectedCityContext(null);
    }

    try {
      let response: RiskAssessmentResponse;
      
      if (mode === 'city' || mode === 'demo') {
        response = await analyzeEgypt({ city_name: data.city_name, location_type: data.location_type || 'industrial' });
      } else if (mode === 'scenario') {
        response = await analyzeScenario(data);
      } else {
        response = await analyzeCustom(data);
      }
      
      setResult(response);
      
      // Smooth scroll to result
      setTimeout(() => {
        document.getElementById('result-section')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    } catch (err: any) {
      setError(
        err.response?.data?.detail || 
        err.message || 
        'Failed to analyze risk. Please check if the backend is running on http://localhost:8000'
      );
    } finally {
      setLoading(false);
    }
  };

  const runDemo = () => {
    handleAnalyze({ city_name: 'Helwan', location_type: 'industrial' }, 'demo');
  };

  return (
    <div className={`min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4 ${language === 'ar' ? 'font-arabic' : ''}`} dir={language === 'ar' ? 'rtl' : 'ltr'}>
      <div className="max-w-5xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12 relative">
          <div className="absolute right-0 top-0 flex gap-2">
            <button 
              onClick={() => setLanguage(language === 'en' ? 'ar' : 'en')}
              className="bg-white border border-gray-200 text-gray-700 px-4 py-2 rounded-lg font-bold shadow-sm hover:bg-gray-50 transition-all text-sm"
            >
              {language === 'en' ? 'العربية' : 'English'}
            </button>
            <button 
              onClick={runDemo}
              className="bg-gradient-to-r from-red-600 to-red-700 text-white px-4 py-2 rounded-lg font-bold shadow-md hover:shadow-lg transform hover:-translate-y-0.5 transition-all text-sm"
            >
              {language === 'en' ? 'Cairo Demo' : 'عرض تجريبي بالقاهرة'}
            </button>
          </div>
          
          <div className="flex flex-col items-center justify-center gap-4 mb-4">
            <img src={logo} alt="Plu Logo" className="w-20 h-20 object-contain drop-shadow-md" />
            <h1 className="text-6xl font-black text-gray-900 tracking-tighter">
              {language === 'en' ? 'Plu' : 'بلو'}
            </h1>
          </div>
          
          <p className="text-xl text-gray-600 font-medium">
            {language === 'en' ? "Built for Cairo. Works anywhere." : "بُني للقاهرة. يعمل في أي مكان."}
          </p>
          <div className="mt-4 inline-block bg-blue-100 text-blue-800 px-4 py-2 rounded-full text-sm font-semibold">
            {language === 'en' ? 'Gaussian Plume Risk Intelligence' : 'ذكاء مخاطر الانبعاثات (غاوس)'}
          </div>
        </header>

        {/* Input Section */}
        <InputSection onAnalyze={handleAnalyze} loading={loading} language={language} />

        {/* Error Message */}
        {error && (
          <div className="mt-8 bg-red-50 border-2 border-red-300 rounded-lg p-6">
            <div className="flex items-start gap-3">
              <div className="w-8 h-8 rounded-full bg-red-100 flex items-center justify-center text-red-600 font-bold shrink-0">!</div>
              <div>
                <h3 className="text-lg font-bold text-red-900 mb-1">{language === 'en' ? 'Error' : 'خطأ'}</h3>
                <p className="text-red-800">{error}</p>
              </div>
            </div>
          </div>
        )}

        {/* Result Section */}
        {result && (
          <div id="result-section" className="mt-12">
            <ResultCard result={result} cairoContext={selectedCityContext} language={language} />
          </div>
        )}

        {/* Footer */}
        <footer className="mt-16 text-center text-gray-500 text-sm">
          <p>
            {language === 'en' ? 'Plu v1.0.0 | Built for Cairo. Works anywhere.' : 'بلو v1.0.0 | بُني للقاهرة. يعمل في أي مكان.'}
          </p>
          <p className="mt-2">
            {language === 'en' 
              ? 'Scientifically validated Gaussian Plume atmospheric dispersion modeling' 
              : 'نمذجة تشتت الغلاف الجوي غاوس المحقق علمياً'}
          </p>
        </footer>
      </div>
    </div>
  );
}

export default App;
