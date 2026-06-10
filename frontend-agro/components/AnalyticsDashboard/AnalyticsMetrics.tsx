/* components/AnalyticsDashboard/AnalyticsMetrics.tsx */
import React from 'react';
import { MetricCard } from '../common/MetricCard';
import { BarChart3, Activity, Zap, TrendingUp } from 'lucide-react';
import { AnalyticsData } from '../../domain/entities';

interface AnalyticsMetricsProps {
  analytics: AnalyticsData | null;
}

export const AnalyticsMetrics: React.FC<AnalyticsMetricsProps> = ({ analytics }) => {
  if (!analytics) return null;
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
      <MetricCard
        title="Total Runs"
        value={analytics.total_simulations}
        subtitle="Scenario comparisons saved"
        icon={BarChart3}
      />
      <MetricCard
        title="Avg Resilience"
        value={analytics.avg_resilience.toFixed(0)}
        subtitle="/100"
        icon={Activity}
      />
      <MetricCard
        title="Food Security Index"
        value={`${analytics.avg_food_security.toFixed(0)}%`}
        subtitle="Regional coverage target"
        icon={Zap}
      />
      <MetricCard
        title="Avg Yield Rate"
        value={analytics.avg_projected_yield.toFixed(2)}
        subtitle="T/HA"
        icon={TrendingUp}
      />
    </div>
  );
};
