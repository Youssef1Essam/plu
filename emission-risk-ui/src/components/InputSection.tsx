import { useState } from 'react';

interface InputSectionProps {
  onAnalyze: (data: any, mode: 'scenario' | 'custom' | 'city' | 'demo') => void;
  loading: boolean;
  language: 'en' | 'ar';
}

const InputSection = ({ onAnalyze, loading, language }: InputSectionProps) => {
  const [mode, setMode] = useState<'scenario' | 'custom' | 'city'>('city');
  
  // City mode state
  const [cityName, setCityName] = useState('Helwan');
  const [isCairoPreset, setIsCairoPreset] = useState(true);

  // Scenario mode state
  const [scenario, setScenario] = useState('power_plant');
  const [locationType, setLocationType] = useState('industrial');
  
  // Custom mode state
  const [customData, setCustomData] = useState({
    emission_rate: 100,
    wind_speed: 5,
    stack_height: 150,
    exit_velocity: 25,
    stack_diameter: 4,
    stack_temperature: 450,
    ambient_temperature: 293,
    stability_class: 'D',
    location_type: 'industrial',
  });

  const handleAnalyze = () => {
    if (mode === 'city') {
      onAnalyze({ city_name: cityName, location_type: locationType, is_cairo_preset: isCairoPreset }, 'city');
    } else if (mode === 'scenario') {
      onAnalyze({ scenario, location_type: locationType }, 'scenario');
    } else {
      onAnalyze(customData, 'custom');
    }
  };

  const handleCustomChange = (field: string, value: string | number) => {
    setCustomData(prev => ({ ...prev, [field]: value }));
  };

  const handleCitySelect = (city: string) => {
    setCityName(city);
    setIsCairoPreset(true);
  };

  return (
    <div className="bg-white rounded-xl shadow-lg p-8 border border-gray-200">
      {/* Mode Toggle */}
      <div className="flex flex-col md:flex-row gap-4 mb-8">
        <button
          onClick={() => setMode('city')}
          className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${
            mode === 'city'
              ? 'bg-blue-600 text-white shadow-md'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {language === 'en' ? 'City Analysis' : 'تحليل المدينة'}
        </button>
        <button
          onClick={() => setMode('scenario')}
          className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${
            mode === 'scenario'
              ? 'bg-blue-600 text-white shadow-md'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {language === 'en' ? 'Standard Facilities' : 'المنشآت القياسية'}
        </button>
        <button
          onClick={() => setMode('custom')}
          className={`flex-1 py-3 px-6 rounded-lg font-semibold transition-all ${
            mode === 'custom'
              ? 'bg-blue-600 text-white shadow-md'
              : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
          }`}
        >
          {language === 'en' ? 'Custom Parameters' : 'معايير مخصصة'}
        </button>
      </div>

      {/* City Mode */}
      {mode === 'city' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              {language === 'en' ? 'Cairo Industrial Zones (Quick Select)' : 'مناطق القاهرة الصناعية (اختيار سريع)'}
            </label>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {[
                { name: 'Helwan', labelEn: 'Helwan', labelAr: 'حلوان', subEn: 'Iron & Steel', subAr: 'الحديد والصلب' },
                { name: 'Shubra El-Kheima', labelEn: 'Shubra', labelAr: 'شبرا', subEn: 'Mixed Ind.', subAr: 'صناعات مختلطة' },
                { name: 'El-Obour', labelEn: 'Obour', labelAr: 'العبور', subEn: 'Ind. Zone', subAr: 'منطقة صناعية' },
                { name: '6th of October', labelEn: '6th October', labelAr: '6 أكتوبر', subEn: 'Ind. City', subAr: 'مدينة صناعية' },
                { name: '10th of Ramadan', labelEn: '10th Ramadan', labelAr: 'العاشر من رمضان', subEn: 'Ind. Zone', subAr: 'منطقة صناعية' },
              ].map(city => (
                <button
                  key={city.name}
                  onClick={() => handleCitySelect(city.name)}
                  className={`py-3 px-2 rounded-xl font-bold border-2 transition-all flex flex-col items-center justify-center text-center ${
                    cityName === city.name && isCairoPreset
                      ? 'border-[#2563EB] bg-blue-50 text-[#2563EB] shadow-sm'
                      : 'border-gray-200 bg-white text-gray-600 hover:border-blue-300 hover:bg-gray-50'
                  }`}
                >
                  <span className="text-sm">{language === 'en' ? city.labelEn : city.labelAr}</span>
                  <span className="text-[10px] font-normal opacity-70 mt-1">{language === 'en' ? city.subEn : city.subAr}</span>
                </button>
              ))}
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {language === 'en' ? 'Or analyze any global city' : 'أو حلل أي مدينة عالمية'}
            </label>
            <input
              type="text"
              placeholder="e.g. London, Tokyo, Mumbai..."
              value={isCairoPreset ? '' : cityName}
              onChange={(e) => {
                setCityName(e.target.value);
                setIsCairoPreset(false);
              }}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {language === 'en' ? 'Context Type' : 'نوع المنطقة'}
            </label>
            <select
              value={locationType}
              onChange={(e) => setLocationType(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="industrial">Industrial</option>
              <option value="urban">Urban</option>
              <option value="rural">Rural</option>
            </select>
          </div>
        </div>
      )}

      {/* Scenario Mode */}
      {mode === 'scenario' && (
        <div className="space-y-6">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-3">
              {language === 'en' ? 'Emission Source' : 'مصدر الانبعاث'}
            </label>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              <button
                onClick={() => setScenario('power_plant')}
                className={`py-3 px-4 rounded-xl font-bold border-2 transition-all ${
                  scenario === 'power_plant'
                    ? 'border-[#2563EB] bg-blue-50 text-[#2563EB] shadow-sm'
                    : 'border-gray-200 bg-white text-gray-600 hover:border-blue-300 hover:bg-gray-50'
                }`}
              >
                {language === 'en' ? 'Power Plant' : 'محطة كهرباء'}
              </button>
              <button
                onClick={() => setScenario('factory')}
                className={`py-3 px-4 rounded-xl font-bold border-2 transition-all ${
                  scenario === 'factory'
                    ? 'border-[#2563EB] bg-blue-50 text-[#2563EB] shadow-sm'
                    : 'border-gray-200 bg-white text-gray-600 hover:border-blue-300 hover:bg-gray-50'
                }`}
              >
                {language === 'en' ? 'Factory' : 'مصنع'}
              </button>
              <button
                onClick={() => setScenario('waste_burning')}
                className={`py-3 px-4 rounded-xl font-bold border-2 transition-all ${
                  scenario === 'waste_burning'
                    ? 'border-[#2563EB] bg-blue-50 text-[#2563EB] shadow-sm'
                    : 'border-gray-200 bg-white text-gray-600 hover:border-blue-300 hover:bg-gray-50'
                }`}
              >
                {language === 'en' ? 'Waste Burning' : 'حرق مخلفات'}
              </button>
            </div>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              {language === 'en' ? 'Location Type' : 'نوع الموقع'}
            </label>
            <select
              value={locationType}
              onChange={(e) => setLocationType(e.target.value)}
              className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="industrial">{language === 'en' ? 'Industrial' : 'صناعي'}</option>
              <option value="urban">{language === 'en' ? 'Urban' : 'حضري'}</option>
              <option value="rural">{language === 'en' ? 'Rural' : 'ريفي'}</option>
            </select>
          </div>
        </div>
      )}

      {/* Custom Mode */}
      {mode === 'custom' && (
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Emission Rate (g/s)
            </label>
            <input
              type="number"
              value={customData.emission_rate}
              onChange={(e) => handleCustomChange('emission_rate', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Wind Speed (m/s)
            </label>
            <input
              type="number"
              value={customData.wind_speed}
              onChange={(e) => handleCustomChange('wind_speed', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Stack Height (m)
            </label>
            <input
              type="number"
              value={customData.stack_height}
              onChange={(e) => handleCustomChange('stack_height', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Exit Velocity (m/s)
            </label>
            <input
              type="number"
              value={customData.exit_velocity}
              onChange={(e) => handleCustomChange('exit_velocity', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Stack Diameter (m)
            </label>
            <input
              type="number"
              value={customData.stack_diameter}
              onChange={(e) => handleCustomChange('stack_diameter', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Stack Temperature (K)
            </label>
            <input
              type="number"
              value={customData.stack_temperature}
              onChange={(e) => handleCustomChange('stack_temperature', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Ambient Temperature (K)
            </label>
            <input
              type="number"
              value={customData.ambient_temperature}
              onChange={(e) => handleCustomChange('ambient_temperature', parseFloat(e.target.value))}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Stability Class
            </label>
            <select
              value={customData.stability_class}
              onChange={(e) => handleCustomChange('stability_class', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="A">A - Very Unstable</option>
              <option value="B">B - Unstable</option>
              <option value="C">C - Slightly Unstable</option>
              <option value="D">D - Neutral</option>
              <option value="E">E - Slightly Stable</option>
              <option value="F">F - Very Stable</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-semibold text-gray-700 mb-2">
              Location Type
            </label>
            <select
              value={customData.location_type}
              onChange={(e) => handleCustomChange('location_type', e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              <option value="industrial">Industrial</option>
              <option value="urban">Urban</option>
              <option value="rural">Rural</option>
            </select>
          </div>
        </div>
      )}

      {/* Analyze Button */}
      <button
        onClick={handleAnalyze}
        disabled={loading}
        className={`w-full mt-8 py-4 px-6 rounded-lg font-bold text-lg transition-all ${
          loading
            ? 'bg-gray-400 cursor-not-allowed'
            : 'bg-blue-600 hover:bg-blue-700 text-white shadow-lg hover:shadow-xl transform hover:-translate-y-0.5'
        }`}
      >
        {loading ? (
          <span className="flex items-center justify-center gap-2">
            <svg className="animate-spin h-5 w-5" viewBox="0 0 24 24">
              <circle
                className="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                strokeWidth="4"
                fill="none"
              />
              <path
                className="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              />
            </svg>
            {language === 'en' ? 'Analyzing...' : 'جاري التحليل...'}
          </span>
        ) : (
          language === 'en' ? 'Analyze Risk' : 'تحليل المخاطر'
        )}
      </button>
    </div>
  );
};

export default InputSection;
