import React from "react";

interface DeleteProps {
  className?: any;
  onClick: () => void;
}

const Delete: React.FC<DeleteProps> = (props) => {
  return (
    <div
      className={props.className}
      style={{
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
      }}
      onClick={props.onClick}
    >
      <svg
        viewBox="0 0 100 100"
        y="0"
        x="0"
        xmlns="http://www.w3.org/2000/svg"
        id="圖層_1"
        version="1.1"
      >
        <path
          fill="#e15b64"
          d="M84.627 26H31.933a8.834 8.834 0 0 0-6.129 2.456L7.816 45.626a6.07 6.07 0 0 0-1.894 4.355 6.062 6.062 0 0 0 1.792 4.396l17.021 17.021A8.816 8.816 0 0 0 31.012 74h53.615c5.211 0 9.451-4.24 9.451-9.451V35.451c0-5.211-4.24-9.451-9.451-9.451z"
        ></path>

        <path
          fill="#fff"
          d="M71.743 50l6.879-6.88a3.003 3.003 0 0 0 0-4.243 3.003 3.003 0 0 0-4.243 0l-6.879 6.88-6.879-6.88c-1.134-1.134-3.111-1.134-4.243 0a3.003 3.003 0 0 0 0 4.243L63.257 50l-6.879 6.88a3.003 3.003 0 0 0 0 4.243 3.003 3.003 0 0 0 4.243 0l6.879-6.88 6.879 6.88c.567.567 1.32.879 2.122.879s1.555-.312 2.121-.879a3.003 3.003 0 0 0 0-4.243L71.743 50z"
        ></path>
      </svg>
    </div>
  );
};

export default Delete;
