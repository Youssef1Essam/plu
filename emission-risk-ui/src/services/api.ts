import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export interface ScenarioRequest {
  scenario: string;
  location_type: string;
}

export interface CustomRequest {
  emission_rate: number;
  wind_speed: number;
  stack_height: number;
  exit_velocity: number;
  stack_diameter: number;
  stack_temperature: number;
  ambient_temperature: number;
  stability_class: string;
  location_type: string;
}

export interface HealthZone {
  zone_name: string;
  distance_range: string;
  color_code: string;
  pollutants: string[];
  vulnerable_groups: string[];
  warning_english: string;
  warning_arabic: string;
}

export interface EgyptPredictRequest {
  city_name: string;
  location_type: string;
}

export interface RiskAssessmentResponse {
  risk_level: string;
  peak_concentration: number;
  impact_distance_meters: number;
  effective_height: number;
  explanation: string;
  recommendation: string;
  confidence: number;
  warnings: string[];
  impact_width_meters?: number;
  time_to_impact_minutes?: number;
  peak_distance_meters?: number;
  population_risk?: string;
  assessment_id: string;
  timestamp: string;
  ai_used?: boolean;
  health_zones?: HealthZone[];
  uncertainty_range?: {
    min_concentration: number;
    max_concentration: number;
    min?: number;
    max?: number;
  };
}

export const analyzeScenario = async (data: ScenarioRequest): Promise<RiskAssessmentResponse> => {
  const response = await axios.post(`${API_BASE_URL}/predict-scenario`, data);
  return response.data;
};

export const analyzeCustom = async (data: CustomRequest): Promise<RiskAssessmentResponse> => {
  const response = await axios.post(`${API_BASE_URL}/predict`, data);
  return response.data;
};

export const analyzeEgypt = async (data: EgyptPredictRequest): Promise<RiskAssessmentResponse> => {
  const response = await axios.post(`${API_BASE_URL}/predict-egypt`, data);
  return response.data;
};
