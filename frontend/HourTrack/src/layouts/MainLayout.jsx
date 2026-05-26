import React from "react";
import { NavLink, Outlet } from "react-router-dom";
import { routes } from "../routes";

const MainLayout = () => {
  return (
    <div style={{ display: "flex", height: "100vh" }}>
      {/* Sidebar */}
      <nav
        style={{
          width: "64px",
          background: "#1a90ff",
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          paddingTop: "24px",
          position: "fixed",
          left: 0,
          top: 0,
          height: "100vh",
          zIndex: 1000,
          boxShadow: "2px 0 12px rgba(0,0,0,0.3)",
        }}
      >
        {routes
          .filter((r) => r.icon)
          .map(({ path, icon: Icon, label }) => (
            <NavLink
              key={path}
              to={path}
              title={label}
              style={({ isActive }) => ({
                margin: "8px 0",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                width: "44px",
                height: "44px",
                borderRadius: "10px",
                background: isActive
                  ? "linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.08))"
                  : "transparent",
                borderRadius: "14px",
                backdropFilter: isActive ? "blur(8px)" : "none",
                boxShadow: isActive
                  ? "0 4px 20px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.3)"
                  : "none",
                border: isActive ? "1px solid rgba(255,255,255,0.2)" : "1px solid transparent",
                transform: isActive ? "scale(1.08)" : "scale(1)",
                opacity: isActive ? 1 : 0.55,
                transition: "all 0.3s cubic-bezier(0.34,1.56,0.64,1)",
                textDecoration: "none",
              })}
            >
              {typeof Icon === "function"
                ? <Icon />
                : <img src={Icon} alt={label} style={{ width: "26px", height: "26px", opacity: 0.85 }} />
              }
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
          paddingLeft: "64px",
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
