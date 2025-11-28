export type HelloResponse = {
  message: string
}

export const api = {
  getHello: async (): Promise<HelloResponse> => {
    const r = await fetch("http://localhost:8000/api/hello")
    return r.json() as Promise<HelloResponse>
  }
}