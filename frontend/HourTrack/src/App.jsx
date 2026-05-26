import React, { useEffect } from "react";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import Router from "./Router";

// Vite env vars must be read from import.meta.env
const VITE_API_BASE_URL = import.meta.env.VITE_API_BASE_URL;

// Create a React Query Client
const queryClient = new QueryClient();

const VersionLogger = () => {
  useEffect(() => {
    if (!VITE_API_BASE_URL) {
      console.warn("VITE_API_BASE_URL is not defined");
      return;
    }

    fetch(`${VITE_API_BASE_URL}/version`)
      .then((res) => res.json())
      .then((data) => {
        console.log("Backend version:", data.version);
        console.log("Release date:", data.data_realse);
      })
      .catch((err) => console.error("Version error:", err));
  }, []);

  return null;
};

const App = () => {
  console.log("APP version:", "4.1.0", "last update 2026-02-02");
  console.log("API Frontend Base URL:", VITE_API_BASE_URL);

  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <Router />
        <VersionLogger />
      </BrowserRouter>
    </QueryClientProvider>
  );
};

export default App;
