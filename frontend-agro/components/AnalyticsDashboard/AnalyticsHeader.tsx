/* components/AnalyticsDashboard/AnalyticsHeader.tsx */
import React from 'react';
import { AnalyticsData } from '../../domain/entities';

interface AnalyticsHeaderProps {
  analytics: AnalyticsData | null;
  region?: string;
}

export const AnalyticsHeader: React.FC<AnalyticsHeaderProps> = ({ analytics, region }) => (
  <div className="flex items-center justify-between border-b border-zinc-100 dark:border-zinc-900/40 pb-4">
    <div>
      <h2 className="text-2xl font-bold text-zinc-900 dark:text-zinc-50 tracking-tight">
        Analytics Historical Summary
      </h2>
      <p className="text-xs text-zinc-500 dark:text-zinc-400 mt-1.5 font-medium">
        {analytics?.latest_simulation &&
          `Database Sync Status: Active (Last run: ${new Date(analytics.latest_simulation).toLocaleDateString()})`}
      </p>
    </div>
  </div>
);
