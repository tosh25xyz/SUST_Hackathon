import TicketForm from "../components/TicketForm";
import ResultCard from "../components/ResultCard";
import StatusBar from "../components/StatusBar";

const Home = () => {
  return (
    <main className="min-h-screen bg-slate-900 text-white">
      <div className="mx-auto max-w-7xl px-6 py-10">
        <div className="flex flex-col items-center">
          <h1 className="text-5xl font-bold text-emerald-400">
            QueueStorm Investigator
          </h1>

          <p className="mt-3 text-lg text-slate-400">
            AI Support Copilot — Internal Use Only
          </p>

          <div className="mt-4">
            <StatusBar />
          </div>
        </div>

        <div className="mt-10 grid gap-6 lg:grid-cols-2">
          <TicketForm />
          <ResultCard />
        </div>
      </div>
    </main>
  );
};

export default Home;