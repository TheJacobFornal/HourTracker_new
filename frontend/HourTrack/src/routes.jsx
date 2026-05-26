import List from "./Pages/Gallery/Gallery";
import Project from "./Pages/project/ProjectPage";
import Zestawienie from "./Pages/Zestawienie/Zestawienie";
import ListIcon from "./assets/home.png";

const HomeIcon = () => (
  <img src={ListIcon} alt="Home" style={{ width: "26px", height: "26px", opacity: 0.85 }} />
);

const GeneratorIcon = () => (
  <svg width="26" height="26" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
    <rect x="3" y="3" width="18" height="18" rx="3" stroke="rgba(255,255,255,0.85)" strokeWidth="1.6" />
    <path d="M7 8h10M7 12h7M7 16h5" stroke="rgba(255,255,255,0.85)" strokeWidth="1.6" strokeLinecap="round" />
    <circle cx="18" cy="16" r="3" fill="#ff2d78" />
    <path d="M17 16l.8.8 1.6-1.6" stroke="#fff" strokeWidth="1.2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);

export const routes = [
  {
    path: "/",
    element: <List />,
    label: "Lista projektów",
    icon: HomeIcon,
  },
  { path: "/projects/:projectId", element: <Project /> },
  {
    path: "/zestawienie",
    element: <Zestawienie />,
    label: "Generator zestawienia aktywności",
    icon: GeneratorIcon,
  },
];
