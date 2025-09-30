// Gallery_Grid.jsx
import React from "react";
import ProjectCard from "./ProjectCard";

export default function GalleryGrid({
  projects,
  filters,
  totalCount,
  onPageChange,
}) {
  const totalPages = Math.ceil((totalCount || 0) / (filters.page_size || 50));
  const currentPage = filters.page || 1;

  return (
    <>
      <div className="w-full flex flex-col items-center">
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-7 justify-items-center place-items-center">
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
      </div>
      {/* Pagination controls */}
      <div
        className="flex flex-col items-center my-6"
        style={{ padding: "20px" }}
      >
        {totalPages > 1 && (
          <div className="flex items-center gap-4 bg-white rounded-lg shadow px-6 py-3">
            <button
              className="px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 hover:bg-gray-200 transition disabled:opacity-50"
              disabled={currentPage <= 1}
              onClick={() => onPageChange && onPageChange(currentPage - 1)}
            >
              Previous
            </button>
            <span className="text-lg font-semibold text-gray-700">
              Page {currentPage} of {totalPages || 1}
            </span>
            <button
              className="px-4 py-2 border border-gray-300 rounded-lg bg-gray-100 hover:bg-gray-200 transition disabled:opacity-50"
              disabled={currentPage >= totalPages}
              onClick={() => onPageChange && onPageChange(currentPage + 1)}
            >
              Next
            </button>
          </div>
        )}
      </div>
    </>
  );
}
