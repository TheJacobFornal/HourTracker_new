const DEFAULT_DEV_HOST = "http://127.0.0.1:8000";
const DEFAULT_PROD_HOST = "http://192.200.69.80:8000";

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
