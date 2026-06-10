export interface MetricItem {
  label: string;
  value: string;
  description: string;
}

export interface DashboardMetrics {
  food_security_index: number;
  projected_yield_tons: number;
  economic_loss_prevented_usd: number;
  resilience_score: number;
}

export interface HistoricalChartItem {
  month: string;
  base_risk: number;
  mitigated_risk: number;
  agent_insight: string;
}

export interface ActionCard {
  id: string;
  title: string;
  description: string;
  agent_reasoning?: string;
  visual_indicator: string; 
  resilience_contribution?: string;
  executive_priority?: string;
  decision_triggers?: string[];
  agent_source?: string;
}

export interface ExecutiveSummary {
  scenario_viability: string;
  economic_projection: string;
  autonomous_prediction: string;
  agent_confidence?: number;
}

export interface FoundryIQMeta {
  status: string;
  confidence: number;
  source: string;
}

export interface FabricIQMeta {
  status: string;
  lakehouse: string;
  synced_records: number;
}

export interface MicrosoftIQMetadata {
  foundry_iq: FoundryIQMeta;
  fabric_iq: FabricIQMeta;
}

export interface SimulationResult {
  status: string;
  dashboard_metrics: DashboardMetrics;
  historical_chart_data: HistoricalChartItem[];
  action_cards: ActionCard[];
  executive_summary: ExecutiveSummary;
  microsoft_iq?: MicrosoftIQMetadata;
  message?: string;
}

export interface AnalyticsData {
  total_simulations: number;
  avg_resilience: number;
  avg_food_security: number;
  avg_projected_yield: number;
  risk_distribution: {
    low: number;
    medium: number;
    high: number;
  };
  latest_simulation: string | null;
}

export interface TrendData {
  dates: string[];
  resilience: number[];
  food_security: number[];
  yield: number[];
}

export interface HistoryItem {
  id: number;
  timestamp: string;
  region: string;
  crop_type: string;
  irrigation_investment: number;
  planting_window_shift: number;
  resilience_score: number;
  food_security_index: number;
  projected_yield: number;
  loss_mitigated: number;
  risk_level: string;
}

export interface BucketMetrics {
  count: number;
  avg_yield: number;
  avg_resilience: number;
  avg_food_security: number;
  avg_investment_cost: number;
  avg_roi: number;
}

export interface ROIData {
  low_investment: BucketMetrics;
  medium_investment: BucketMetrics;
  high_investment: BucketMetrics;
}
