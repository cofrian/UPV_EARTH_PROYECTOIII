const publicBase = process.env.NEXT_PUBLIC_API_BASE_URL || "/api/v1";
const internalBase = process.env.API_BASE_URL_INTERNAL || "http://127.0.0.1:8000/api/v1";

function resolveBase(): string {
  const isServer = typeof window === "undefined";
  if (isServer && publicBase.startsWith("/")) {
    return internalBase;
  }
  return publicBase;
}

export async function apiGet<T>(path: string): Promise<T> {
  const response = await fetch(`${resolveBase()}${path}`, { cache: "no-store" });
  if (!response.ok) {
    throw new Error(`API error ${response.status}`);
  }
  return response.json() as Promise<T>;
}

export async function apiUploadPdf(file: File): Promise<{ job_id: string; status: string; message: string }> {
  const form = new FormData();
  form.append("file", file);

  const response = await fetch(`${resolveBase()}/uploads/pdf`, {
    method: "POST",
    body: form,
  });

  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err?.detail || "No se pudo subir el PDF");
  }

  return response.json();
}
