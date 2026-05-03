interface ExplanationSectionProps {
  explanation: string;
}

const ExplanationSection = ({ explanation }: ExplanationSectionProps) => {
  return (
    <div className="mt-8 bg-blue-50 rounded-lg p-6 border border-blue-200">
      <div className="flex items-start gap-3">
        <div className="w-8 h-8 rounded-full bg-blue-100 flex items-center justify-center text-blue-600 font-bold shrink-0">AI</div>
        <div>
          <h3 className="text-lg font-bold text-gray-900 mb-2">Analysis</h3>
          <p className="text-gray-700 leading-relaxed">{explanation}</p>
        </div>
      </div>
    </div>
  );
};

export default ExplanationSection;
