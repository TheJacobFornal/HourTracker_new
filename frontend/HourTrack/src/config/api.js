const DEV_HOST = "127.0.0.1:8000";
const PROD_HOST = "10.1.69.13:8000";

const resolveDefaultHost = (host) => {
  if (typeof window !== "undefined" && window.location?.protocol === "https:") {
    return `https://${host}`;
  }
  return `http://${host}`;
};

const DEFAULT_DEV_HOST = resolveDefaultHost(DEV_HOST);
const DEFAULT_PROD_HOST = resolveDefaultHost(PROD_HOST);

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ??
  (import.meta.env.PROD ? DEFAULT_PROD_HOST : DEFAULT_DEV_HOST);

export const API_ENDPOINTS = {
  projectActivities: `${API_BASE_URL}/api/project/activities_details`,
  projectHeader: `${API_BASE_URL}/api/project/header_info`,
  projectsSearch: `${API_BASE_URL}/api/projects/search`,
  leaders: `${API_BASE_URL}/get/leaders`,
};

export { API_BASE_URL };
