'use client';
import React from 'react';
import { ScatterChart, Scatter, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';
interface CorrelationData {
  irrigation: number;
  resilience: number;
  yield: number;
  risk: string;
}

export const CorrelationPlot = ({ data }: { data: CorrelationData[] }) => {
  if (!data || data.length === 0) return null;
  return (
    <div className="rounded-2xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-4 shadow-md border border-zinc-100 dark:border-zinc-900/50">
      <h3 className="mb-2 text-lg font-semibold text-primary-800 dark:text-primary-200">Risk Correlation Plot</h3>
      <ResponsiveContainer width="100%" height={300}>
        <ScatterChart>
          <CartesianGrid strokeDasharray="3 3" className="stroke-zinc-200 dark:stroke-zinc-700" />
          <XAxis dataKey="irrigation" stroke="currentColor" />
          <YAxis dataKey="resilience" stroke="currentColor" />
          <Tooltip />
          <Scatter data={data} fill="hsl(161,94%,30%)" />
        </ScatterChart>
      </ResponsiveContainer>
    </div>
  );
};
