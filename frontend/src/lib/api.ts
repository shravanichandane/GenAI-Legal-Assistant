// src/lib/api.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://genai-legal-assistant.onrender.com/api/v1";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  // Try to get token from localStorage for MVP
  // In a real app, this might be in an HttpOnly cookie or secure state
  const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
  
  const headers = {
    ...options.headers,
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let errorMessage = "API request failed";
    try {
      const errorData = await response.json();
      errorMessage = errorData.detail || errorMessage;
    } catch (e) {
      // Ignored
    }
    throw new ApiError(response.status, errorMessage);
  }

  return response.json();
}

export const api = {
  // Auth
  login: async (formData: FormData) => {
    // OAuth2 uses form-urlencoded
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      body: formData,
    });
    
    if (!response.ok) {
      throw new ApiError(response.status, "Login failed");
    }
    return response.json();
  },
  register: async (data: { email: string; password: string }) => {
    const response = await fetch(`${BASE_URL}/auth/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    });
    
    if (!response.ok) {
      let errorMessage = "Registration failed";
      try {
        const errorData = await response.json();
        errorMessage = errorData.detail || errorMessage;
      } catch (e) {}
      throw new ApiError(response.status, errorMessage);
    }
    return response.json();
  },
  
  getMe: () => fetchWithAuth("/auth/me"),
  
  // Contracts
  uploadContract: async (formData: FormData) => {
    const token = typeof window !== "undefined" ? localStorage.getItem("access_token") : null;
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    
    const response = await fetch(`${BASE_URL}/contracts/upload`, {
      method: "POST",
      body: formData,
      headers,
    });
    
    if (!response.ok) throw new ApiError(response.status, "Upload failed");
    return response.json();
  },
  
  getContractStatus: (id: string) => fetchWithAuth(`/contracts/${id}/status`),
  
  getContractRisks: (id: string) => fetchWithAuth(`/contracts/${id}/risks`),
  
  getContractRiskScore: (id: string) => fetchWithAuth(`/contracts/${id}/risk-score`),
  
  reviewAction: (id: string, action: string) => 
    fetchWithAuth(`/contracts/${id}/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action }),
    }),
};
