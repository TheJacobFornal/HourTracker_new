// Filtr_Search.jsx
import React from "react";

const ProjectSearch = ({ value = "", onChange, onSubmit }) => {
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit?.(value);
  };

  return (
    <>
      <style>{`
        .search-btn {
          background-color: #47CDFA;
        }
        .search-btn:hover {
          background-color: #2FC9F7;
        }
        .search-input {
          padding-left: 10px;
        }

      `}</style>

      <form
        onSubmit={handleSubmit}
        className="flex items-center gap-2 flex-1 min-w-[240px]"
      >
        <input
          type="text"
          placeholder="Search projects..."
          value={value}
          onChange={(e) => onChange?.(e.target.value)}
          className="search-input flex-1 rounded-md border border-gray-400 min-h-[40px] text-[16px] pl-[10px] pr-3 py-2"
        />
        <button
          type="submit"
          className="search-btn inline-flex items-center justify-center px-4 py-2 rounded-md text-black text-center"
        >
          Search
        </button>
      </form>
    </>
  );
};

export default ProjectSearch;
