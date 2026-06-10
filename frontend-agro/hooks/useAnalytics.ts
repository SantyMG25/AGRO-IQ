/* hooks/useAnalytics.ts */
import { useEffect, useState } from 'react';
import { AnalyticsData, TrendData, HistoryItem, ROIData } from '../domain/entities';
import { HttpCropAnalysisApiAdapter } from '../adapters/outbound/http_api';

const apiService = new HttpCropAnalysisApiAdapter();

export const useAnalytics = (region?: string) => {
  const [analytics, setAnalytics] = useState<AnalyticsData | null>(null);
  const [trends, setTrends] = useState<TrendData | null>(null);
  const [history, setHistory] = useState<HistoryItem[]>([]);
  const [roi, setROI] = useState<ROIData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchAnalytics = async () => {
      try {
        setLoading(true);
        const [analyticsData, trendsData, historyData, roiData] = await Promise.all([
          apiService.fetchDashboardAnalytics(region),
          apiService.fetchTrends(region, 30),
          apiService.fetchHistory(region, 50),
          apiService.fetchROI(region),
        ]);
        setAnalytics(analyticsData);
        setTrends(trendsData);
        setHistory(historyData);
        setROI(roiData);
      } catch (err) {
        setError(`Failed to load analytics: ${err}`);
      } finally {
        setLoading(false);
      }
    };
    fetchAnalytics();
  }, [region]);

  return { analytics, trends, history, roi, loading, error };
};
