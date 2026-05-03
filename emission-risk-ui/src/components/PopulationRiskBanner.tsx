interface PopulationRiskBannerProps {
  populationRisk?: string;
}

const PopulationRiskBanner = ({ populationRisk }: PopulationRiskBannerProps) => {
  if (!populationRisk) {
    return null;
  }

  return (
    <div className="mt-6 bg-purple-50 rounded-lg p-6 border-2 border-purple-300">
      <div className="flex items-center gap-3">
        <div className="w-8 h-8 rounded-full bg-purple-100 flex items-center justify-center text-purple-600 font-bold shrink-0">P</div>
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-1">Population Risk</h3>
          <p className="text-gray-800 font-medium">{populationRisk}</p>
        </div>
      </div>
    </div>
  );
};

export default PopulationRiskBanner;
