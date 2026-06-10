'use client';
import React from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { ROIData } from '../../domain/entities';

export const ROIChart = ({ roi }: { roi: ROIData }) => {
  if (!roi) return null;
  // Transform ROIData object into chart‑friendly array (low, medium, high investments)
  const chartData = [
    { investment: 'Low', value: roi.low_investment.avg_roi },
    { investment: 'Medium', value: roi.medium_investment.avg_roi },
    { investment: 'High', value: roi.high_investment.avg_roi },
  ];

  return (
    <div className="rounded-2xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-4 shadow-md border border-zinc-100 dark:border-zinc-900/50">
      <h3 className="mb-2 text-lg font-semibold text-primary-800 dark:text-primary-200">ROI Analysis</h3>
      <ResponsiveContainer width="100%" height={300}>
        <BarChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-zinc-200 dark:stroke-zinc-700" />
          <XAxis dataKey="investment" stroke="currentColor" />
          <YAxis stroke="currentColor" />
          <Tooltip />
          <Bar dataKey="value" fill="hsl(46,96%,47%)" />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};
