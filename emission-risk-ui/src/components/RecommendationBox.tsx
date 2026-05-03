interface RecommendationBoxProps {
  recommendation: string;
  riskLevel: string;
}

const RecommendationBox = ({ recommendation, riskLevel }: RecommendationBoxProps) => {
  const getBoxStyle = () => {
    switch (riskLevel.toUpperCase()) {
      case 'LOW':
        return 'bg-[#F0FDF4] border-[#16A34A] text-[#16A34A]';
      case 'MEDIUM':
        return 'bg-[#FFFBEB] border-[#D97706] text-[#D97706]';
      case 'HIGH':
        return 'bg-[#FEF2F2] border-[#DC2626] text-[#DC2626]';
      default:
        return 'bg-gray-50 border-gray-300 text-gray-700';
    }
  };

  const getIcon = () => {
    switch (riskLevel.toUpperCase()) {
      case 'LOW': 
        return <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center text-green-600 font-bold">S</div>;
      case 'MEDIUM': 
        return <div className="w-12 h-12 rounded-full bg-yellow-100 flex items-center justify-center text-yellow-600 font-bold">!</div>;
      case 'HIGH': 
        return <div className="w-12 h-12 rounded-full bg-red-100 flex items-center justify-center text-red-600 font-bold">!!</div>;
      default: 
        return <div className="w-12 h-12 rounded-full bg-gray-100 flex items-center justify-center text-gray-600 font-bold">i</div>;
    }
  };

  return (
    <div className={`mt-12 ${getBoxStyle()} rounded-2xl p-10 border-l-8 border-y border-r shadow-sm`}>
      <div className="flex items-start gap-6">
        <div className="shrink-0">{getIcon()}</div>
        <div>
          <h3 className="text-xl font-black mb-3 uppercase tracking-wide text-gray-900">
            Action Required
          </h3>
          <p className="text-2xl font-medium text-gray-900 leading-relaxed">
            {recommendation}
          </p>
        </div>
      </div>
    </div>
  );
};

export default RecommendationBox;
