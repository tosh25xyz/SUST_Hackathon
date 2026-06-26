const SafetyAlert = ({ show }) => {
  if (!show) return null;

  return (
    <div className="mt-4 rounded-lg border border-red-600 bg-red-900/30 p-4">
      <p className="font-semibold text-red-400">
        🚨 HUMAN REVIEW REQUIRED
      </p>
    </div>
  );
};

export default SafetyAlert;