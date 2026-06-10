export type PageAction = {
  label: string;
  href: string;
  variant: "primary" | "secondary";
};

export type MetricItem = {
  label: string;
  value: string;
  description: string;
};

export async function fetchCropAnalysis(irrigation: number, shift: number) {
  try {
    const response = await fetch('http://127.0.0.1:8000/api/analyze', {
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
    
    if (!response.ok) throw new Error('Server error');
    return await response.json();
  } catch (error) {
    console.error("Error connecting to backend:", error);
    return null;
  }
}