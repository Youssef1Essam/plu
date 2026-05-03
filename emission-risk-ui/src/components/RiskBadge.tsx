interface RiskBadgeProps {
  riskLevel: string;
}

const RiskBadge = ({ riskLevel }: RiskBadgeProps) => {
  const getBadgeStyle = () => {
    switch (riskLevel.toUpperCase()) {
      case 'LOW':
        return 'bg-[#F0FDF4] text-[#16A34A] border-[#16A34A]/30';
      case 'MEDIUM':
        return 'bg-[#FFFBEB] text-[#D97706] border-[#D97706]/30';
      case 'HIGH':
        return 'bg-[#FEF2F2] text-[#DC2626] border-[#DC2626]/30';
      default:
        return 'bg-gray-50 text-gray-500 border-gray-200';
    }
  };

  const isHigh = riskLevel.toUpperCase() === 'HIGH';

  return (
    <div className={`inline-block border-4 rounded-3xl px-12 py-10 shadow-lg ${getBadgeStyle()} ${isHigh ? 'animate-pulse' : ''}`}>
      <div className="text-8xl md:text-[9rem] font-black tracking-tighter leading-none">
        {riskLevel.toUpperCase()} RISK
      </div>
    </div>
  );
};

export default RiskBadge;
