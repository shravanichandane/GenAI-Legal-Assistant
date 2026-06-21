// src/lib/api.ts
const BASE_URL = process.env.NEXT_PUBLIC_API_URL || "https://genai-legal-assistant.onrender.com/api/v1";

export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
    this.name = "ApiError";
  }
}

async function fetchWithAuth(endpoint: string, options: RequestInit = {}) {
  const headers: Record<string, string> = {
    ...(options.headers as Record<string, string> || {}),
  };

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
    credentials: "include",
  });

  if (!response.ok) {
    // Global 401 handling: redirect to login
    if (response.status === 401 && typeof window !== "undefined") {
      window.location.href = "/login";
      return;
    }

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
    const response = await fetch(`${BASE_URL}/auth/login`, {
      method: "POST",
      body: formData,
      credentials: "include",
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
      credentials: "include",
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

  logout: async () => {
    const response = await fetch(`${BASE_URL}/auth/logout`, {
      method: "POST",
      credentials: "include",
    });

    if (!response.ok) {
      throw new ApiError(response.status, "Logout failed");
    }
    return response.json();
  },

  // Contracts
  uploadContract: async (formData: FormData) => {
    const response = await fetch(`${BASE_URL}/contracts/upload`, {
      method: "POST",
      body: formData,
      credentials: "include",
    });

    if (!response.ok) throw new ApiError(response.status, "Upload failed");
    return response.json();
  },

  getContractStatus: (id: string) => fetchWithAuth(`/contracts/${id}/status`),

  getContractRisks: (id: string) => fetchWithAuth(`/contracts/${id}/risks`),

  getContractRiskScore: (id: string) => fetchWithAuth(`/contracts/${id}/risk-score`),

  getContractContent: (id: string) => fetchWithAuth(`/contracts/${id}/content`),

  getContractPdfUrl: (id: string) => `${BASE_URL}/contracts/${id}/pdf`,

  reviewAction: async (contractId: string, action: string) => {
    return fetchWithAuth(`/contracts/${contractId}/action`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ action }),
    });
  },

  submitTelemetry: async (contractId: string, payload: { clause_id: string; clause_type: string; ai_suggested_text: string; lawyer_final_text: string }) => {
    return fetchWithAuth(`/contracts/${contractId}/telemetry`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });
  },

  getContracts: () => fetchWithAuth(`/contracts/`),

  // Playbooks
  getPlaybookRules: () => fetchWithAuth(`/playbooks/rules`),

  createPlaybookRule: (data: { clause_type: string, rule_description: string, is_mandatory?: boolean }) =>
    fetchWithAuth(`/playbooks/rules`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),

  updatePlaybookRule: (id: string, data: any) =>
    fetchWithAuth(`/playbooks/rules/${id}`, {
      method: "PUT",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    }),

  deletePlaybookRule: (id: string) =>
    fetchWithAuth(`/playbooks/rules/${id}`, {
      method: "DELETE",
    }),
};
