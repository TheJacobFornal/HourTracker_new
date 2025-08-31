import List from "./Pages/Gallery/Gallery";
import Project from "./Pages/project/ProjectPage";
import ListIcon from "./assets/home.png";
import MenuIcon from "./assets/menu.png";

export const routes = [
  {
    path: "/",
    element: <List />,
    label: "List",
    icon: ListIcon,
  },
  { path: "/projects/:projectId", element: <Project /> },
];
