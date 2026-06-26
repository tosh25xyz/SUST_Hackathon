const StatusBar = () => {
  return (
    <div className="flex items-center gap-2">
      <span className="h-3 w-3 rounded-full bg-green-500"></span>

      <span className="text-sm text-slate-300">
        API Online
      </span>
    </div>
  );
};

export default StatusBar;