import { CropAnalysisApiPort } from '../../ports/api_port';
import { SimulationResult, AnalyticsData, TrendData, HistoryItem, ROIData } from '../../domain/entities';

const BASE_URL = 'http://127.0.0.1:8000';

export class HttpCropAnalysisApiAdapter implements CropAnalysisApiPort {
  async fetchCropAnalysis(irrigation: number, shift: number): Promise<SimulationResult | null> {
    try {
      const response = await fetch(`${BASE_URL}/api/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          region: "Global Andean Region",
          crop_type: "Subsistence Corn",
          user_description: "Preventive food security monitoring by thermal anomalies.",
          variables: {
            irrigation_investment: irrigation,
            planting_window_shift: shift,
            fertilizer_subsidy: 50
          }
        })
      });
      
      if (!response.ok) throw new Error('Server error during analysis fetch');
      return await response.json();
    } catch (error) {
      console.error("HttpApiAdapter: Error connecting to backend /api/analyze:", error);
      return null;
    }
  }

  async fetchDashboardAnalytics(region?: string): Promise<AnalyticsData | null> {
    try {
      const url = `${BASE_URL}/api/analytics/dashboard${region ? `?region=${region}` : ''}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Server error fetching dashboard analytics');
      return await response.json();
    } catch (error) {
      console.error("HttpApiAdapter: Error fetching dashboard analytics:", error);
      return null;
    }
  }

  async fetchTrends(region?: string, days = 30): Promise<TrendData | null> {
    try {
      const url = `${BASE_URL}/api/analytics/trends?${region ? `region=${region}&` : ''}days=${days}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Server error fetching trends');
      return await response.json();
    } catch (error) {
      console.error("HttpApiAdapter: Error fetching trends:", error);
      return null;
    }
  }

  async fetchHistory(region?: string, limit = 50): Promise<HistoryItem[]> {
    try {
      const url = `${BASE_URL}/api/analytics/history?${region ? `region=${region}&` : ''}limit=${limit}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Server error fetching history');
      return await response.json();
    } catch (error) {
      console.error("HttpApiAdapter: Error fetching history:", error);
      return [];
    }
  }

  async fetchROI(region?: string): Promise<ROIData | null> {
    try {
      const url = `${BASE_URL}/api/analytics/roi${region ? `?region=${region}` : ''}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Server error fetching ROI');
      return await response.json();
    } catch (error) {
      console.error("HttpApiAdapter: Error fetching ROI:", error);
      return null;
    }
  }
}
