import React from "react";
import { Routes, Route } from "react-router-dom";
import MainLayout from "./layouts/MainLayout";
import { routes } from "./routes";

const Router = () => (
  <Routes>
    <Route path="/" element={<MainLayout />}>
      {routes.map(({ path, element }) => (
        <Route
          key={path}
          path={path === "/" ? "" : path.slice(1)}
          element={element}
        />
      ))}
    </Route>
    <Route path="*" element={<div>404 Not Found</div>} />
  </Routes>
);

export default Router;
