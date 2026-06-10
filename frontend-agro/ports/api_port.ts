import { SimulationResult, AnalyticsData, TrendData, HistoryItem, ROIData } from '../domain/entities';

export interface CropAnalysisApiPort {
  
  fetchCropAnalysis(irrigation: number, shift: number): Promise<SimulationResult | null>;

  
  fetchDashboardAnalytics(region?: string): Promise<AnalyticsData | null>;

  
  fetchTrends(region?: string, days?: number): Promise<TrendData | null>;

  
  fetchHistory(region?: string, limit?: number): Promise<HistoryItem[]>;

  
  fetchROI(region?: string): Promise<ROIData | null>;
}
