import RiskBadge from './RiskBadge';
import MetricsGrid from './MetricsGrid';
import ExplanationSection from './ExplanationSection';
import RecommendationBox from './RecommendationBox';
import WarningsList from './WarningsList';
import ConfidenceBar from './ConfidenceBar';
import PopulationRiskBanner from './PopulationRiskBanner';
import type { RiskAssessmentResponse } from '../services/api';

interface ResultCardProps {
  result: RiskAssessmentResponse;
  cairoContext?: string | null;
  language: 'en' | 'ar';
}

const ResultCard = ({ result, cairoContext, language }: ResultCardProps) => {
  // Generate insight line logic
  const getInsight = () => {
    const isHigh = result.risk_level.toUpperCase() === 'HIGH';
    const isMed = result.risk_level.toUpperCase() === 'MEDIUM';
    const urgent = result.time_to_impact_minutes && result.time_to_impact_minutes < 30;

    if (language === 'ar') {
      if (isHigh) return urgent ? "قد تصل الانبعاثات للمناطق المجاورة خلال دقائق." : "تم رصد ظروف جوية خطيرة. مطلوب اتخاذ إجراء فوري.";
      if (isMed) return "التشتت المحدود قد يسبب تراكم الملوثات بالقرب من الأرض.";
      return "الظروف مواتية للتشتت. التأثير المتوقع ضئيل جداً.";
    }
    
    if (isHigh) return urgent ? "Pollution may reach nearby areas within minutes." : "Severe atmospheric conditions detected. Immediate action required.";
    if (isMed) return "Limited dispersion may cause accumulation near ground.";
    return "Conditions are favorable for dispersion. Negligible impact expected.";
  };

  const insightLine = getInsight();

  return (
    <div className="bg-white rounded-3xl shadow-2xl p-8 md:p-16 border border-gray-100 transition-all duration-400 ease-out animate-[fadeScale_400ms_ease-out_forwards] w-full">
      <style>{`
        @keyframes fadeScale {
          from { opacity: 0; transform: scale(0.95); }
          to { opacity: 1; transform: scale(1); }
        }
      `}</style>

      {/* Hero Section */}
      <div className="flex flex-col items-center justify-center text-center mb-16 relative">
        {/* AI Attribution Badge */}
        {result.ai_used && (
          <div className="absolute -top-10 left-1/2 -translate-x-1/2 bg-blue-600 text-white px-4 py-1.5 rounded-full text-[10px] font-black uppercase tracking-widest shadow-lg flex items-center gap-2 border-2 border-white">
            <span className="animate-pulse w-2 h-2 bg-blue-200 rounded-full"></span>
            {language === 'en' ? 'Powered by Gemma 4 AI' : 'مدعوم بذكاء Gemma 4'}
          </div>
        )}
        
        <RiskBadge riskLevel={result.risk_level} />
        <p className="text-2xl md:text-3xl font-bold text-gray-800 tracking-tight mt-8">
          {insightLine}
        </p>
      </div>

      {cairoContext && (
        <div className="max-w-4xl mx-auto mb-12 bg-gradient-to-r from-red-50 to-orange-50 border border-red-200 rounded-2xl p-6 shadow-sm">
          <div className="flex items-start gap-4">
            <div className="w-12 h-12 rounded-xl bg-red-100 flex items-center justify-center text-red-600 font-black text-xl shrink-0">EG</div>
            <div>
              <h3 className="text-xl font-black text-red-900 mb-2">
                {language === 'en' ? `Cairo Context: ${cairoContext}` : `سياق القاهرة: ${cairoContext}`}
              </h3>
              <p className="text-red-800 font-medium">
                {language === 'en' 
                  ? "Cairo ranks among the world's most polluted cities. This area has significant industrial concentration."
                  : "تعد القاهرة من أكثر مدن العالم تلوثاً. تحتوي هذه المنطقة على تركيز صناعي كبير."}
                <br/><span className="text-sm mt-1 block opacity-80">
                  {language === 'en' ? 'Reference: WHO Guidelines & Egypt Vision 2030 Air Quality Targets.' : 'المرجع: إرشادات منظمة الصحة العالمية وأهداف رؤية مصر 2030 لجودة الهواء.'}
                </span>
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="max-w-4xl mx-auto space-y-12">
        <MetricsGrid
          impactDistance={result.impact_distance_meters}
          timeToImpact={result.time_to_impact_minutes}
          peakDistance={result.peak_distance_meters}
          peakConcentration={result.peak_concentration}
        />

        {/* Health Impact Zones */}
        {result.health_zones && result.health_zones.length > 0 && (
          <div className="mt-12">
            <h3 className="text-2xl font-black text-gray-900 mb-6">
              {language === 'en' ? 'Health Impact Zones' : 'نطاقات التأثير الصحي'}
            </h3>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {result.health_zones.map((zone, idx) => (
                <div key={idx} className={`rounded-xl p-5 border-l-8 ${
                  zone.color_code === 'red' ? 'border-red-500 bg-red-50' :
                  zone.color_code === 'orange' ? 'border-orange-500 bg-orange-50' :
                  zone.color_code === 'yellow' ? 'border-yellow-500 bg-yellow-50' :
                  'border-green-500 bg-green-50'
                }`}>
                  <div className="flex justify-between items-center mb-3">
                    <span className="font-black text-lg text-gray-900">{zone.zone_name}</span>
                    <span className="font-bold font-mono text-gray-600 bg-white px-2 py-1 rounded">{zone.distance_range}</span>
                  </div>
                  <div className="space-y-2 text-sm">
                    <p><span className="font-bold text-gray-900">{language === 'en' ? 'Vulnerable:' : 'الفئات الضعيفة:'}</span> {zone.vulnerable_groups.join(', ')}</p>
                    <p>{language === 'en' ? zone.warning_english : zone.warning_arabic}</p>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <RecommendationBox
          recommendation={result.recommendation}
          riskLevel={result.risk_level}
        />

        <div className="bg-gray-50 rounded-2xl p-8 border border-gray-200 mt-12">
          <h3 className="text-lg font-bold text-gray-900 mb-4">
            {language === 'en' ? 'Detailed Explanation' : 'شرح تفصيلي'}
            {result.ai_used && <span className="ml-2 text-[10px] text-blue-600 uppercase">AI Generated</span>}
          </h3>
          <ExplanationSection explanation={result.explanation} />
        </div>

        <ConfidenceBar confidence={result.confidence} />
        
        {result.population_risk && (
          <PopulationRiskBanner populationRisk={result.population_risk} />
        )}
        
        {result.warnings && result.warnings.length > 0 && (
          <WarningsList warnings={result.warnings} />
        )}

        {/* Uncertainty Range (if available) */}
        {result.uncertainty_range && (
          <div className="mt-6 bg-gray-50 rounded-xl p-6 border border-gray-200">
            <h4 className="text-sm font-bold text-gray-700 mb-2 uppercase tracking-wide">
              Concentration Uncertainty Range
            </h4>
            <p className="text-base font-medium text-gray-600">
              Min: {((result.uncertainty_range as any).min_concentration ?? (result.uncertainty_range as any).min ?? 0).toExponential(2)} µg/m³ | Max:{' '}
              {((result.uncertainty_range as any).max_concentration ?? (result.uncertainty_range as any).max ?? 0).toExponential(2)} µg/m³
            </p>
          </div>
        )}

        {/* Audit Footer */}
        <div className="mt-8 pt-6 border-t border-gray-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex flex-col">
            <span className="text-[10px] uppercase tracking-[0.2em] font-black text-gray-400 mb-1">{language === 'en' ? 'Assessment ID' : 'معرف التقييم'}</span>
            <span className="text-xs font-mono font-bold text-gray-600 bg-gray-100 px-2 py-1 rounded">{result.assessment_id}</span>
          </div>
          <div className="flex flex-col md:items-end">
            <span className="text-[10px] uppercase tracking-[0.2em] font-black text-gray-400 mb-1">{language === 'en' ? 'Generated At' : 'تم الإنشاء في'}</span>
            <span className="text-xs font-bold text-gray-500">{new Date(result.timestamp).toLocaleString(language === 'en' ? 'en-US' : 'ar-EG')}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ResultCard;
