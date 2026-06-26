const EvidenceBadge = ({ verdict }) => {
  const colors = {
    consistent: "bg-green-600",
    inconsistent: "bg-red-600",
    insufficient_data: "bg-yellow-500 text-black",
  };

  return (
    <span
      className={`rounded-full px-3 py-1 text-sm font-semibold ${
        colors[verdict] || "bg-slate-600"
      }`}
    >
      {verdict || "Unknown"}
    </span>
  );
};

export default EvidenceBadge;