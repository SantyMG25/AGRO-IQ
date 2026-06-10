/* components/AnalyticsDashboard/TrendChart.tsx */
'use client';

import React from 'react';
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from 'recharts';
import { TrendData } from '../../hooks/useAnalytics'; // adjust path if necessary

interface TrendChartProps {
  trends: TrendData;
}

export const TrendChart: React.FC<TrendChartProps> = ({ trends }) => {
  if (!trends || !trends.dates || trends.dates.length === 0) {
    return <p className="text-sm text-zinc-500 dark:text-zinc-400">No trend data available.</p>;
  }

  // Build chart data array
  const chartData = trends.dates.map((date, idx) => ({
    date,
    yield: trends.yields?.[idx] ?? null,
    rainfall: trends.rainfall?.[idx] ?? null,
    temperature: trends.temperature?.[idx] ?? null,
    // add other series if needed
  }));

  return (
    <div className="rounded-2xl bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-4 shadow-md border border-zinc-100 dark:border-zinc-900/50">
      <h3 className="mb-2 text-lg font-semibold text-primary-800 dark:text-primary-200">
        Performance Trends
      </h3>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
          <CartesianGrid strokeDasharray="3 3" className="stroke-zinc-200 dark:stroke-zinc-700" />
          <XAxis dataKey="date" stroke="currentColor" className="text-xs" />
          <YAxis stroke="currentColor" className="text-xs" />
          <Tooltip
            contentStyle={{
              backgroundColor: 'var(--color-bg-primary)',
              border: 'none',
              borderRadius: '0.5rem',
            }}
          />
          {/* Example series – you can add more based on available data */}
          {trends.yields && (
            <Line
              type="monotone"
              dataKey="yield"
              stroke="hsl(161, 94%, 30%)"
              strokeWidth={2}
              dot={false}
            />
          )}
          {trends.rainfall && (
            <Line
              type="monotone"
              dataKey="rainfall"
              stroke="hsl(210, 91%, 66%)"
              strokeWidth={2}
              dot={false}
            />
          )}
          {trends.temperature && (
            <Line
              type="monotone"
              dataKey="temperature"
              stroke="hsl(46, 96%, 47%)"
              strokeWidth={2}
              dot={false}
            />
          )}
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
};
