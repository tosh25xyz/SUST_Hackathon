import EvidenceBadge from "./EvidenceBadge";
import SafetyAlert from "./SafetyAlert";

const ResultCard = () => {
  return (
    <div className="rounded-xl border border-slate-700 bg-[#16213e] p-6 shadow-lg">
      <h2 className="text-2xl font-bold text-white">
        Analysis Result
      </h2>

      <div className="mt-6 flex items-center justify-between">
        <div>
          <p className="text-sm text-slate-400">
            Ticket ID
          </p>

          <h3 className="text-lg font-bold text-white">
            TKT-001
          </h3>
        </div>

        <span className="rounded-full bg-orange-600 px-3 py-1 text-sm font-semibold text-white">
          HIGH
        </span>
      </div>

      <SafetyAlert show={true} />

      <div className="mt-6 rounded-lg border border-slate-700 bg-slate-800 p-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-white">
            Evidence Verdict
          </h3>

          <EvidenceBadge verdict="consistent" />
        </div>
      </div>
    </div>
  );
};

export default ResultCard;