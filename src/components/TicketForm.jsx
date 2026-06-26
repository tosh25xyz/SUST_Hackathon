import { useState } from "react";

const TicketForm = () => {
  const [transactions, setTransactions] = useState([]);

  const addTransaction = () => {
    if (transactions.length >= 5) return;

    setTransactions([
      ...transactions,
      {
        transaction_id: "",
        timestamp: "",
        type: "",
        amount: "",
        counterparty: "",
        status: "",
      },
    ]);
  };

  return (
    <div className="rounded-xl border border-slate-700 bg-[#16213e] p-6 shadow-lg">
      <div className="mb-6 flex items-center justify-between">
        <h2 className="text-2xl font-bold text-white">
          Ticket Information
        </h2>

        <button
          type="button"
          className="rounded-lg bg-emerald-600 px-4 py-2 text-sm font-semibold text-white hover:bg-emerald-700"
        >
          Load Sample
        </button>
      </div>

      <div className="space-y-6">

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Ticket ID
          </label>

          <input
            type="text"
            placeholder="Enter Ticket ID"
            className="w-full rounded-lg border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
          />
        </div>

        <div>
          <label className="mb-2 block text-sm font-medium text-slate-300">
            Customer Complaint
          </label>

          <textarea
            rows="6"
            placeholder="Describe the customer's complaint..."
            className="w-full resize-none rounded-lg border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
          />
        </div>
                <div className="grid gap-6 md:grid-cols-2">
          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Language
            </label>

            <select className="w-full rounded-lg border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500">
              <option value="">Select Language</option>
              <option value="en">English</option>
              <option value="bn">Bangla</option>
              <option value="mixed">Mixed</option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Channel
            </label>

            <select className="w-full rounded-lg border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500">
              <option value="">Select Channel</option>
              <option value="in_app_chat">In-App Chat</option>
              <option value="call_center">Call Center</option>
              <option value="email">Email</option>
              <option value="merchant_portal">Merchant Portal</option>
              <option value="field_agent">Field Agent</option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              User Type
            </label>

            <select className="w-full rounded-lg border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500">
              <option value="">Select User Type</option>
              <option value="customer">Customer</option>
              <option value="merchant">Merchant</option>
              <option value="agent">Agent</option>
              <option value="unknown">Unknown</option>
            </select>
          </div>

          <div>
            <label className="mb-2 block text-sm font-medium text-slate-300">
              Campaign Context
            </label>

            <input
              type="text"
              placeholder="Enter campaign context (optional)"
              className="w-full rounded-lg border border-slate-600 bg-slate-800 px-4 py-3 text-white outline-none focus:border-blue-500"
            />
          </div>
        </div>

        <div>
          <h3 className="text-xl font-semibold text-white">
            Transaction History
          </h3>

          <p className="mt-1 text-sm text-slate-400">
            Add up to 5 recent transactions.
          </p>

          <button
            type="button"
            onClick={addTransaction}
            className="mt-4 rounded-lg bg-blue-600 px-4 py-2 font-medium text-white hover:bg-blue-700"
          >
            + Add Transaction
          </button>
                    <div className="mt-6 space-y-4">
            {transactions.map((transaction, index) => (
              <div
                key={index}
                className="rounded-lg border border-slate-700 bg-slate-800 p-4"
              >
                <div className="mb-4 flex items-center justify-between">
                  <p className="font-semibold text-white">
                    Transaction #{index + 1}
                  </p>

                  <button
                    type="button"
                    className="rounded bg-red-600 px-3 py-1 text-sm text-white hover:bg-red-700"
                  >
                    ✕
                  </button>
                </div>

                <div className="space-y-3">
                  <input
                    type="text"
                    placeholder="Transaction ID"
                    className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white"
                  />

                  <input
                    type="datetime-local"
                    className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white"
                  />

                  <input
                    type="number"
                    placeholder="Amount"
                    className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white"
                  />

                  <select className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white">
                    <option value="">Select Type</option>
                    <option value="transfer">Transfer</option>
                    <option value="payment">Payment</option>
                    <option value="cash_in">Cash In</option>
                    <option value="cash_out">Cash Out</option>
                    <option value="settlement">Settlement</option>
                    <option value="refund">Refund</option>
                  </select>

                  <input
                    type="text"
                    placeholder="Counterparty"
                    className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white"
                  />

                  <select className="w-full rounded-lg border border-slate-600 bg-slate-900 px-4 py-3 text-white">
                    <option value="">Select Status</option>
                    <option value="completed">Completed</option>
                    <option value="failed">Failed</option>
                    <option value="pending">Pending</option>
                    <option value="reversed">Reversed</option>
                  </select>
                </div>
              </div>
            ))}
          </div>
        </div>
                <button
          type="submit"
          className="mt-8 w-full rounded-lg bg-emerald-600 px-6 py-3 text-lg font-semibold text-white hover:bg-emerald-700"
        >
          Analyze Ticket
        </button>

      </div>
    </div>
  );
};

export default TicketForm;