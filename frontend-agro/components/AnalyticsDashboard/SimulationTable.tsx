'use client';
import React from 'react';
interface SimulationHistory {
  irrigation_investment: number;
  resilience_score: number;
  projected_yield: number;
  risk_level: string;
}

export const SimulationTable = ({ history }: { history: SimulationHistory[] }) => {
  if (!history || history.length === 0) return null;
  return (
    <div className="overflow-x-auto rounded-2xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-4 shadow-md border border-zinc-100 dark:border-zinc-900/50">
      <h3 className="mb-2 text-lg font-semibold text-primary-800 dark:text-primary-200">Historical Simulations</h3>
      <table className="w-full table-auto text-sm">
        <thead className="bg-zinc-100 dark:bg-zinc-800/30">
          <tr>
            <th className="p-2 text-left font-medium">Irrigation</th>
            <th className="p-2 text-left font-medium">Resilience</th>
            <th className="p-2 text-left font-medium">Yield</th>
            <th className="p-2 text-left font-medium">Risk</th>
          </tr>
        </thead>
        <tbody>
          {history.map((item, idx) => (
            <tr key={idx} className={idx % 2 === 0 ? 'bg-zinc-50 dark:bg-zinc-900/20' : 'bg-white dark:bg-zinc-950/30'}>
              <td className="p-2">{item.irrigation_investment}</td>
              <td className="p-2">{item.resilience_score}</td>
              <td className="p-2">{item.projected_yield}</td>
              <td className="p-2">{item.risk_level}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
