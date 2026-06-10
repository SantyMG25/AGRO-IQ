'use client';

import { useState } from 'react';
import { useAnalytics } from '../hooks/useAnalytics';
import { LoadingSpinner } from './common/LoadingSpinner';
import { ErrorBanner } from './common/ErrorBanner';
import { AnalyticsHeader } from './AnalyticsDashboard/AnalyticsHeader';
import { AnalyticsMetrics } from './AnalyticsDashboard/AnalyticsMetrics';
import { RiskDistribution } from './AnalyticsDashboard/RiskDistribution';
import { TrendChart } from './AnalyticsDashboard/TrendChart';
import { CorrelationPlot } from './AnalyticsDashboard/CorrelationPlot';
import { ROIChart } from './AnalyticsDashboard/ROIChart';
import { SimulationTable } from './AnalyticsDashboard/SimulationTable';
import NavTab from './NavTab';

export type ChartViewType = 'trends' | 'correlation' | 'roi';

export default function AnalyticsDashboard({ region }: { region?: string }) {
  const { analytics, trends, history, roi, loading, error } = useAnalytics(region);
  const [chartView, setChartView] = useState<ChartViewType>('trends');


  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorBanner message={error} />;

  const correlationData = history.slice(0, 20).map(item => ({
    irrigation: item.irrigation_investment,
    resilience: item.resilience_score,
    yield: item.projected_yield,
    risk: item.risk_level,
  }));

  return (
    <div className="w-full space-y-8 bg-white/80 dark:bg-zinc-950/70 backdrop-blur-md p-6 rounded-3xl border border-zinc-100 dark:border-zinc-900/50 shadow-md">
      <AnalyticsHeader analytics={analytics} region={region} />
      <AnalyticsMetrics analytics={analytics} />
      <RiskDistribution analytics={analytics} />

      <NavTab chartView={chartView} setChartView={setChartView} />

      {/* Renderizado Condicional de Gráficos */}
      {chartView === 'trends' && trends?.dates && trends.dates.length > 0 && (
        <TrendChart trends={trends} />
      )}

      {chartView === 'correlation' && correlationData.length > 0 && <CorrelationPlot data={correlationData} />}

      {chartView === 'roi' && roi && <ROIChart roi={roi} />}

      {history.length > 0 && (
        <SimulationTable history={history} />
      )}
    </div>
  );
}