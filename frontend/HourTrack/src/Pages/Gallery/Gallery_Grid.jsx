// Gallery_Grid.jsx
import React from "react";
import ProjectCard from "./ProjectCard";

export default function GalleryGrid({ projects, filters }) {
  return (
    <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
      {projects.map((p) => (
        <ProjectCard
          key={p.id}
          id={p.id}
          hours={p.hours}
          user={p.user}
          dateRange={p.dateRange}
          filters={filters}
        />
      ))}
    </div>
  );
}
