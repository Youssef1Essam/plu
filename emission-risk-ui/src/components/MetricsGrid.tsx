interface MetricsGridProps {
  impactDistance: number;
  impactWidth?: number;
  timeToImpact?: number;
  peakDistance?: number;
  peakConcentration: number;
}

const MetricsGrid = ({
  impactDistance,
  timeToImpact,
  peakConcentration
}: MetricsGridProps) => {
  const formatDistance = (meters: number) => {
    if (meters >= 1000) {
      return `≈ ${(meters / 1000).toFixed(1)} km`;
    }
    return `≈ ${meters.toFixed(0)} m`;
  };

  const formatTime = (minutes: number) => {
    return `≈ ${Math.round(minutes)} minutes`;
  };

  return (
    <div className="w-full">
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8 mb-10">
        <div className="text-center bg-gray-50 rounded-2xl p-8 border border-gray-200">
          <div className="text-6xl font-black text-[#111827] mb-3">
            {formatDistance(impactDistance)}
          </div>
          <div className="text-lg font-bold text-gray-500 uppercase tracking-wider">
            Downwind impact distance
          </div>
        </div>

        {timeToImpact !== undefined ? (
          <div className="text-center bg-gray-50 rounded-2xl p-8 border border-gray-200">
            <div className="text-6xl font-black text-[#111827] mb-3">
              {formatTime(timeToImpact)}
            </div>
            <div className="text-lg font-bold text-gray-500 uppercase tracking-wider">
              Estimated arrival time
            </div>
          </div>
        ) : (
          <div className="text-center bg-gray-50 rounded-2xl p-8 border border-gray-200">
            <div className="text-6xl font-black text-[#111827] mb-3">
              {peakConcentration.toExponential(2)}
            </div>
            <div className="text-lg font-bold text-gray-500 uppercase tracking-wider">
              Peak Concentration (µg/m³)
            </div>
          </div>
        )}
      </div>

      {/* Visual Bar */}
      <div className="max-w-3xl mx-auto px-4">
        <div className="relative h-6 bg-gray-100 rounded-full w-full overflow-hidden border border-gray-200 shadow-inner">
          <div className="absolute top-0 left-0 h-full bg-[#2563EB] w-full origin-left animate-[scaleX_1s_ease-out_forwards]">
             <div className="absolute inset-0 bg-white/20" style={{ backgroundImage: 'repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(255,255,255,0.2) 10px, rgba(255,255,255,0.2) 20px)' }}></div>
          </div>
        </div>
        <div className="flex justify-between mt-4 text-sm font-bold text-gray-500 uppercase tracking-widest">
          <span className="flex items-center gap-2">Emission Source</span>
          <span className="flex items-center gap-2">Distance: {formatDistance(impactDistance).replace('≈ ', '')}</span>
        </div>
      </div>
      <style>{`
        @keyframes scaleX {
          from { transform: scaleX(0); }
          to { transform: scaleX(1); }
        }
      `}</style>
    </div>
  );
};

export default MetricsGrid;
