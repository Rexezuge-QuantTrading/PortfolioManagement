interface Portfolio {
  id: number; // Hash Key
  symbol: string; // Sory Key
  quantity: number;
  avgCostBasis: number; // Retain 8 decimal places
  lock: number; // Unix Timestamp
  createdAt: number; // Unix Timestamp
  updatedAt: number; // Unix Timestamp
}

export type { Portfolio };
