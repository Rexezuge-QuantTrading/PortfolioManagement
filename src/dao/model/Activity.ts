interface Activity {
  ts: number; // Unix Timestamp, Hash Key
  portfolioId: number;
  symbol: string; // Sory Key
  quantity: number;
  avgCostBasis: number; // Retain 8 decimal places
}

export type { Activity };
