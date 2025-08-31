import React from "react";
import { NavLink, Outlet } from "react-router-dom";
import { routes } from "../routes";

const MainLayout = () => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <nav
        style={{
          width: "80px",
          background: "#1a90ffff",
          color: "#fff",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          paddingTop: "20px",
        }}
      >
        {routes.map(({ path, icon, label }) => (
          <NavLink
            key={path}
            to={path}
            title={label}
            style={({ isActive }) => ({
              margin: "20px 0",
              display: "block",
              padding: "10px",
              borderRadius: "8px",
              backgroundColor: isActive ? "#4fd1c5" : "transparent",
            })}
          >
            <img
              src={icon}
              alt={label}
              style={{ width: "32px", height: "32px" }}
            />
          </NavLink>
        ))}
      </nav>

      {/* Main Content */}
      <main
        style={{
          flex: 1,
          padding: 0,
          display: "flex",

          justifyContent: "center",
          maxWidth: "100%",
          paddingLeft: "200px",
          paddingTop: "50px",
        }}
      >
        <div style={{ width: "100%" }}>
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default MainLayout;
