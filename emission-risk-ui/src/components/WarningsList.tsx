interface WarningsListProps {
  warnings: string[];
}

const WarningsList = ({ warnings }: WarningsListProps) => {
  if (!warnings || warnings.length === 0) {
    return null;
  }

  return (
    <div className="mt-6 bg-orange-50 rounded-lg p-6 border-2 border-orange-300">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-orange-100 flex items-center justify-center text-orange-600 font-bold shrink-0">!</div>
        <div className="flex-1">
          <h3 className="text-lg font-bold text-gray-900 mb-3">Warnings</h3>
          <ul className="space-y-2">
            {warnings.map((warning, index) => (
              <li key={index} className="flex items-start gap-2">
                <span className="text-orange-600 font-bold">•</span>
                <span className="text-gray-800">{warning}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
};

export default WarningsList;
