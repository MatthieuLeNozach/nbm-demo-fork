import React from "react";

const Annotation: React.FC = () => {
  return (
    <svg
      width="40"
      height="40"
      viewBox="0 0 40 40"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <rect x="0.5" width="40" height="40" rx="4" fill="#072136" />
      <path
        d="M11.5 24.75V28.5H15.25L26.31 17.44L22.56 13.69L11.5 24.75ZM29.21 14.54C29.6 14.15 29.6 13.52 29.21 13.13L26.87 10.79C26.48 10.4 25.85 10.4 25.46 10.79L23.63 12.62L27.38 16.37L29.21 14.54Z"
        fill="white"
      />
    </svg>
  );
};

export default Annotation;
